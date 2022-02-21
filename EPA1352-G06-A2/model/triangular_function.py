import numpy as np
from numpy.random import default_rng
rng = default_rng()

break_XL = rng.triangular(60, 120, 240)

break_L = rng.uniform(45, 90)

break_M = rng.uniform(15, 60)

break_S = rng.uniform(10, 20)