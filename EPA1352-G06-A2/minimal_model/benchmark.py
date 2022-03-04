import timeit

replications = 10
print(f"Running Minimal Model {replications} times:")

min_mod_time = timeit.timeit('minimal.run_experiment(scenarios=range(9), n_trucks=1000, iterations=1)', setup='import minimal', number=replications)
print(f"{min_mod_time:.3f} seconds")
