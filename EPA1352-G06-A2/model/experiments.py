from model import BangladeshModel
import pickle
import statistics

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 5 x 24 hours; 1 tick 1 minute
run_length = 24 * 60 * 5
seed = 1234
durations = {}

# Run model for each of the 9 scenario's (0 being no delays)
for scenario in range(0,9):
    sim_model = BangladeshModel(scenario, seed=seed)
    for i in range(run_length):
        sim_model.step()
    durations[scenario] = sim_model.durations
    print(f"Done with scenario {scenario}. Average delay: {statistics.mean(durations[scenario])}")


# open a file, where you want to store the data
file = open('../data/durations.pickle', 'wb')

# dump information to that file
pickle.dump(durations, file)

# close the file
file.close()

print("Done with Pickle")
