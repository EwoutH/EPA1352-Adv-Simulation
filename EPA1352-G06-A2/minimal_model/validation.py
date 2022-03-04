import pandas as pd
import random
import numpy as np

# Read in the road and scenario table
df = pd.read_csv('../data/simulation_file_N1.csv')
scenarios_df = pd.read_csv('../data/scenario_delays.csv', sep=';', index_col='Scenario')

road_df = df.loc[df["model_type"] == "link"]
bridge_df = df.loc[df["model_type"] != "link"]
bridge_df = bridge_df.drop(df.tail(1).index)
bridge_df = bridge_df[["length", "condition", "length_class"]]

lengths = bridge_df["length"].to_dict()
conditions = bridge_df["condition"].to_dict()
length_classes = bridge_df["length_class"].to_dict()

road_length = road_df["length"].sum()
bridge_length = bridge_df["length"].sum()

expect_dict = {
    "XL": 140,
    "L": 67.5,
    "M": 37.5,
    "S": 15,
}

expected_time = {}
for scenario in range(9):
    expected_time[scenario] = 0

numbers = {}
bridges_cats = {}
for size_class in expect_dict.keys():
    bridges_size = {bridge: length_class for (bridge, length_class) in length_classes.items() if length_class == size_class}
    bridges_size = {bridge: condition for (bridge, condition) in conditions.items() if bridge in bridges_size.keys()}
    for cond in ['A', 'B', 'C', 'D']:
        number = list(bridges_size.values()).count(cond)
        for scenario in range(9):
            expected_time[scenario] += expect_dict[size_class] * (scenarios_df[f"Cat{cond}"][scenario]/100) * number
        bridges_cats[size_class, cond] = number

for scenario in range(9):
    print(f"Expected time in Scenario {scenario}: {expected_time[scenario]}")

index = pd.MultiIndex.from_tuples(bridges_cats.keys())
df = pd.Series(bridges_cats.values(), index=index)
df = df.unstack()
df.to_csv("../data/bridges_size_condition.csv")
print(df)

df_expected = pd.Series(expected_time, name='Expected delay times')
print(df_expected)
df_expected.to_csv("../results/validation.csv", index_label="Scenario")
