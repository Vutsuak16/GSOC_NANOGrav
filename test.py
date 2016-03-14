__name__ = "vutsuak"

import pandas as pd
import numpy as np

data = pd.read_csv("pulsar_data_test.csv")
for i in data:
    x=i
    break

print(data[x])

