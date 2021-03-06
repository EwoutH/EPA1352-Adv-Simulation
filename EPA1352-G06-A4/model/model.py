from mesa import Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace
from components import Source, Sink, SourceSink, Bridge, Link, Intersection
import pandas as pd
from collections import defaultdict
import networkx as nx
import math

# ---------------------------------------------------------------
def set_lat_lon_bound(lat_min, lat_max, lon_min, lon_max, edge_ratio=0.02):
    """
    Set the HTML continuous space canvas bounding box (for visualization)
    give the min and max latitudes and Longitudes in Decimal Degrees (DD)

    Add white borders at edges (default 2%) of the bounding box
    """

    lat_edge = (lat_max - lat_min) * edge_ratio
    lon_edge = (lon_max - lon_min) * edge_ratio

    x_max = lon_max + lon_edge
    y_max = lat_min - lat_edge
    x_min = lon_min - lon_edge
    y_min = lat_max + lat_edge
    return y_min, y_max, x_min, x_max


# ---------------------------------------------------------------
class BangladeshModel(Model):
    """
    The main (top-level) simulation model

    One tick represents one minute; this can be changed
    but the distance calculation need to be adapted accordingly

    Class Attributes:
    -----------------
    step_time: int
        step_time = 1 # 1 step is 1 min

    path_ids_dict: defaultdict
        Key: (origin, destination)
        Value: the shortest path (Infra component IDs) from an origin to a destination

        Only straight paths in the Demo are added into the dict;
        when there is a more complex network layout, the paths need to be managed differently

    sources: list
        all sources in the network

    sinks: list
        all sinks in the network

    """
    traffic_data = pd.read_csv("../data/traffic_per_road.csv")
    traffic_data.set_index("Road", inplace=True)
    traffic_fractions = traffic_data["Percentage of traffic"] / 100
    traffic_fractions = traffic_fractions.to_dict()

    step_time = 1
    file_name = '../data/df_road_N1andN2.csv'

    def __init__(self, scenario, seed=None, run_length=0, cooldown=0, traffic=traffic_fractions, x_max=500, y_max=500, x_min=0, y_min=0):
        self.schedule = BaseScheduler(self)
        self.running = True
        self.path_ids_dict = defaultdict(lambda: pd.Series())
        self.space = None
        self.generate_vehicles = True
        self.sources = []
        self.sinks = []
        self.SourceSinks = []
        self.scenario = scenario
        self.scenario_chances = {}
        self.seed = seed
        self.run_length = run_length + cooldown  # Cooldown happens after regular run length
        self.cooldown = cooldown
        self.traffic = traffic
        self.generation_frequency = 5
        self.arrived_car_dict = {'VehicleID': [], 'Travel_Time': [], 'Startpoint':[],'Endpoint':[]}
        self.G = nx.Graph()

        self.generate_model()

    def generate_model(self):
        """
        generate the simulation model according to the csv file component information

        Warning: the labels are the same as the csv column labels
        """

        df = pd.read_csv(self.file_name)

        # Define bright length bins and labels
        length_bins = [0, 10, 50, 200, math.inf]
        length_labels = ['S', 'M', 'L', 'XL']

        # Categorize bridges per length class
        df["length_class"] = pd.cut(df["length"], bins=length_bins, include_lowest=False, right=False, labels=length_labels)

        # a list of names of roads to be generated
        roads = df['road'].unique().tolist()

        # Read in the scenario table
        scenarios_df = pd.read_csv('../data/scenario_delays.csv', sep=';', index_col='Scenario')
        scenarios_df = scenarios_df / 100  # percent to fraction

        # Create scenario dictionary with break-down chance for each bridge type
        self.scenario_chances = scenarios_df.loc[[self.scenario]].to_dict(orient="records")[0]

        df_objects_all = []
        for road in roads:
            # Select all the objects on a particular road in the original order as in the cvs
            df_objects_on_road = df[df['road'] == road]

            if not df_objects_on_road.empty:
                df_objects_all.append(df_objects_on_road)

                """
                Set the path 
                1. get the serie of object IDs on a given road in the cvs in the original order
                2. add the (straight) path to the path_ids_dict
                3. put the path in reversed order and reindex
                4. add the path to the path_ids_dict so that the vehicles can drive backwards too
                """
                path_ids = df_objects_on_road['id']
                path_ids.reset_index(inplace=True, drop=True)
                self.path_ids_dict[path_ids[0], path_ids.iloc[-1]] = path_ids
                self.path_ids_dict[path_ids[0], None] = path_ids
                path_ids = path_ids[::-1]
                path_ids.reset_index(inplace=True, drop=True)
                self.path_ids_dict[path_ids[0], path_ids.iloc[-1]] = path_ids
                self.path_ids_dict[path_ids[0], None] = path_ids

                """
                Create NetworkX Graph road by road (path by path)
                """
                path_G = nx.path_graph(path_ids)
                self.G.add_nodes_from(path_G)
                self.G.add_edges_from(path_G.edges)

        # put back to df with selected roads so that min and max and be easily calculated
        df = pd.concat(df_objects_all)
        y_min, y_max, x_min, x_max = set_lat_lon_bound(
            df['lat'].min(),
            df['lat'].max(),
            df['lon'].min(),
            df['lon'].max(),
            0.05
        )

        # ContinuousSpace from the Mesa package;
        # not to be confused with the SimpleContinuousModule visualization
        self.space = ContinuousSpace(x_max, y_max, True, x_min, y_min)

        for df in df_objects_all:
            for _, row in df.iterrows():  # index, row in ...

                # create agents according to model_type
                model_type = row['model_type'].strip()
                agent = None

                name = row['name']
                if pd.isna(name):
                    name = ""
                else:
                    name = name.strip()

                if model_type == 'source':
                    agent = Source(row['id'], self, row['length'], name, row['road'])
                    self.sources.append(agent.unique_id)
                elif model_type == 'sink':
                    agent = Sink(row['id'], self, row['length'], name, row['road'])
                    self.sinks.append(agent.unique_id)
                elif model_type == 'sourcesink':
                    agent = SourceSink(row['id'], self, row['length'], name, row['road'])
                    self.sources.append(agent.unique_id)
                    self.sinks.append(agent.unique_id)
                    self.SourceSinks.append(agent)
                elif model_type == 'bridge':
                    agent = Bridge(row['id'], self, row['length'], name, row['road'], row['condition'], row['length_class'])
                elif model_type == 'link':
                    agent = Link(row['id'], self, row['length'], name, row['road'])
                elif model_type == 'intersection':
                    if not row['id'] in self.schedule._agents:
                        agent = Intersection(row['id'], self, row['length'], name, row['road'])

                if agent:
                    self.schedule.add(agent)
                    y = row['lat']
                    x = row['lon']
                    self.space.place_agent(agent, (x, y))
                    agent.pos = (x, y)

        source_dict = {}
        for s in self.SourceSinks:
            source_dict[s.unique_id] = [s.road_name, s.pos]
        source_df = pd.DataFrame.from_dict(source_dict, orient='index', columns=["Road", "Coordinates"])
        source_df.to_csv("../experiments/source_data.csv")

        for _ in range(self.run_length):
            self.step()
            if self.schedule.steps >= (self.run_length - self.cooldown):
                self.generate_vehicles = False

    def get_straight_route(self, source):
        return self.get_route(source, None)

    def get_random_route(self, source):
        """
        pick up a random route given an origin
        """
        while True:
            # different source and sink
            sink = self.random.choice(self.sinks)
            if sink is not source:
                break
        return self.get_route(source, sink)

    def get_route(self, source, sink):
        if (source, sink) in self.path_ids_dict:
            return self.path_ids_dict[source, sink]
        else:
            path_ids = pd.Series(nx.shortest_path(self.G, source, sink))
            self.path_ids_dict[source, sink] = path_ids
            return path_ids

    def step(self):
        """
        Advance the simulation by one step.
        """
        self.schedule.step()

# EOF -----------------------------------------------------------
