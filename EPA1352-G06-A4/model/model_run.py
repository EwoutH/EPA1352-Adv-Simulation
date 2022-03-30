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
run_length = 24 * 60
seed = 1234

# Loop for all 5 scenarios - each scenario runs for 10 replications
for scenario in range(0, 5):
    df = pd.DataFrame()
    for reps in range(2):
        sim_model = BangladeshModel(scenario=scenario, seed=seed)
        seed += 1
        for i in range(run_length):
            sim_model.step()
        # Turning dictionary into dataframe after each replication
        df1 = pd.DataFrame.from_dict(sim_model.arrived_car_dict)
        df = pd.concat([df,df1])
        print(f'Replication {reps} of scenario {scenario} finished.')
    # Finally saving to csv for each scenario
    df.to_csv(f'../experiments/results_scenario_{scenario}.csv')
    print(f'Scenario {scenario} has been finished.')
