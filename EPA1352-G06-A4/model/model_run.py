from model import BangladeshModel
import pandas as pd
import sys
sys.setrecursionlimit(1500)

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 5 x 24 hours; 1 tick 1 minute
# run_length = 5 * 24 * 60
run_length = 24*60
seed = 1234

scenarios = []
probabilities = []

# Loop to list out scenario output names
for i in range(0, 5):
    scenarios.append("scenario" + str(i))


# Probabilities of bridges breaking down based on scenarios and bridge categories - A,B,C and D
probabilities = [{'A': 0, 'B': 0, 'C': 0, 'D': 0},
                 {'A': 0, 'B': 0, 'C': 0, 'D': 5},
                 {'A': 0, 'B': 0, 'C': 5, 'D': 10},
                 {'A': 0, 'B': 5, 'C': 10, 'D': 20},
                 {'A': 5, 'B': 10, 'C': 20, 'D': 40}]

# Loop for all 5 scenarios - each scenario runs for 10 replications
for scenarionumber in range(0, 5):
    df = pd.DataFrame()
    for reps in range(10):
        sim_model = BangladeshModel(probabilities[scenarionumber], seed=seed)
        seed += 1
        for i in range(run_length):
            sim_model.step()
        # Turning dictionary into dataframe after each replication
        df1 = pd.DataFrame.from_dict(sim_model.arrived_car_dict)
        df = pd.concat([df,df1])
        if reps == 4:
            print(f'Halfway through Scenario {scenarionumber}')
    # Finally saving to csv for each scenario
    df.to_csv(f'../experiments/results_scenario_{scenarionumber}.csv')
    print(f'Scenario {scenarionumber} has been finished.')
