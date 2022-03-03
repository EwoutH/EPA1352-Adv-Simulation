import pandas as pd
import random
import numpy as np

# Read in the road and scenario table
df = pd.read_csv('data/simulation_file_N1.csv')
scenarios_df = pd.read_csv('data/scenario_delays.csv', sep=';', index_col='Scenario')

road_df = df.loc[df["model_type"] == "link"]
bridge_df = df.loc[df["model_type"] != "link"]
bridge_df = bridge_df.drop(df.tail(1).index)
bridge_df = bridge_df[["length", "condition", "length_class"]]

lengths = bridge_df["length"].to_dict()
conditions = bridge_df["condition"].to_dict()
length_classes = bridge_df["length_class"].to_dict()

road_length = road_df["length"].sum()
bridge_length = bridge_df["length"].sum()

delay_dict = {
    "XL": ("triangular", (60, 120, 240)),
    "L": ("uniform", (45, 90)),
    "M": ("uniform", (15, 60)),
    "S": ("uniform", (10, 20)),
}


class Minimal():
    def __init__(self, scenarios, n_trucks=100, speed=48, seed=None):
        self.rng = np.random.default_rng(None)

        self.scenarios = scenarios
        self.n_trucks = n_trucks
        self.speed = speed

        self.bridges_broken = {}
        self.bridges_whole = {}
        self.bridges_state = {}

    def break_bridges(self, scenario):
        scenario_chances = scenarios_df.loc[[scenario]].to_dict(orient="records")[0]

        for bridge, condition in conditions.items():
            broken_chance = scenario_chances[f"Cat{condition}"]
            self.bridges_state[bridge] = broken_chance > random.uniform(0, 1)

        self.bridges_broken = [k for (k, v) in self.bridges_state.items() if v]
        self.bridges_whole = [k for (k, v) in self.bridges_state.items() if not v]

    def run_truck(self):
        drive_time = (road_length + bridge_length) / (self.speed / 60 * 1000)

        delay = 0
        for bridge in self.bridges_broken:
            if delay_dict[length_classes[bridge]][0] == "triangular":
                delay += self.rng.triangular(*delay_dict[length_classes[bridge]][1])

            elif delay_dict[length_classes[bridge]][0] == "uniform":
                delay += self.rng.uniform(*delay_dict[length_classes[bridge]][1])

            else:
                print(f"Unknown input: {delay_dict[length_classes[bridge]][0]}")

        return delay

    def run_sim(self, iterations=1):
        results = {}
        for scenario in self.scenarios:
            results[scenario] = {}
            for i in range(iterations):
                self.break_bridges(scenario)
                results[scenario][i] = []
                for _ in range(self.n_trucks):
                    results[scenario][i].append(self.run_truck())
        return results


def run_experiment(scenarios, n_trucks=100, iterations=25, filename=''):
    model = Minimal(scenarios, n_trucks)
    results = model.run_sim(iterations)
    if filename != '':
        print(f'Saving file data/{filename}.pickle')
        import pickle
        file = open(f'data/{filename}.pickle', 'wb')
        pickle.dump(results, file)
        file.close()
    return results
