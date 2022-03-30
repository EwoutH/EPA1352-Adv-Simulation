from model import BangladeshModel
import pandas as pd

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 5 x 24 hours; 1 tick 1 minute
# run_length = 5 * 24 * 60
run_length = 60 * 60
cooldown = 24 * 60
reps = 5
seed = 1234

# Loop for all 5 scenarios - each scenario runs for 10 replications
for scenario in [4]:
    df = pd.DataFrame()
    for rep in range(reps):
        sim_model = BangladeshModel(scenario=scenario, seed=seed, run_length=run_length, cooldown=cooldown)
        seed += 1
        # Turning dictionary into dataframe after each replication
        df1 = pd.DataFrame.from_dict(sim_model.arrived_car_dict)
        df = pd.concat([df,df1])
        print(f'Replication {rep} of scenario {scenario} finished.')
    # Finally saving to csv for each scenario
    df.to_csv(f'../experiments/iteration/scen_{scenario}_{int(run_length/60)}_hours_{reps}_reps_{int(cooldown/60)}h_cooldown.csv')
    print(f'Scenario {scenario} has been finished.')
print("Finished!")