from model import BangladeshModel
import pandas as pd
"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 5 x 24 hours; 1 tick 1 minute
run_length = 5 * 24 * 60
replication_amount = 10
# run time 1000 ticks
# run_length = 1000

seed = 1234567

#simulation_model = BangladeshModel(seed=seed, )

# Check if the seed is set
#print("SEED " + str(simulation_model._seed))

# One run with given steps
# for i in range(run_length):
#     simulation_model.step()


# Get scenario
scenarionames = []
for i in range(0, 5):
    scenarionames.append("scenario" + str(i))


for scenario_id in range(0, 4):
    df = pd.DataFrame()
    for replication in range(replication_amount):
        simulation_model = BangladeshModel(seed=seed, scenario=scenario_id)
        #seed += seed
        for i in range(run_length):
            simulation_model.step()
        # Turning dictionary into dataframe after each replication
        df1 = pd.DataFrame.from_dict(simulation_model.dic_arrivedcars)
        df = df.append(df1)
    # Finally saving to csv for each scenario
    df.to_csv('../experiments' + scenarionames[scenario_id] + '.csv')