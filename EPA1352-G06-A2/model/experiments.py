import pandas as pd
from mesa.batchrunner import batch_run
from model import BangladeshModel

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 5 x 24 hours; 1 tick 1 minute
# run_length = 5 * 24 * 60

# run time 1000 ticks
run_length = 1000
par_dict = {"scenario": [1,2,3]}

results = batch_run(model_cls=BangladeshModel, parameters=par_dict, number_processes=1, iterations=1, data_collection_period=-1, max_steps=run_length, display_progress=True)
results_df = pd.DataFrame(results)
