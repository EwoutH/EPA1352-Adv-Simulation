import numpy as np
from numpy.random import default_rng

rng = default_rng()

delay_dict = {
    "XL": ("triangular", (60, 120, 240)),
    "L": ("uniform", (45, 90)),
    "M": ("uniform", (15, 60)),
    "S": ("uniform", (10, 20)),
}


def get_delay_value(bridge_class):
    if delay_dict[bridge_class][0] == "triangular":
        return rng.triangular(*delay_dict[bridge_class][1])

    if delay_dict[bridge_class][0] == "uniform":
        return rng.uniform(*delay_dict[bridge_class][1])

    else:
        print("Unknown input!")
        return
