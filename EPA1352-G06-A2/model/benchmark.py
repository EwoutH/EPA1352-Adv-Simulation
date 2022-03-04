from timeit import default_timer as timer

print(f"Running Mesa Model once:")
start = timer()
import experiments
end = timer()
print(f"{end-start:.3f} seconds")
