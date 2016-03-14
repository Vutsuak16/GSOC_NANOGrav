__name__ = "vutsuak"

import pandas as pd
import numpy as np
from bokeh.plotting import output_file, figure, show

data = pd.read_csv("pulsar_data_test.csv")
output_file("plot.html", title="P derivative vs P plot")
p = figure(title="Period derivative vs Period", x_axis_label='Period (s)', y_axis_label='log(P\')')

log_Pdot_Y = []  # created  separate list to show separation of data later we can do it using lesser space
log_Pdot_N = []  # N means not in binary system
P_Y = []  # in binary system as Y
P_N = []

P = []
ct = 0

for i in data["Period Derivative"]:
    if data["Binary"][ct] == "Y":
        log_Pdot_Y.append(np.log(i))
        P_Y.append(data["Period"][ct])
    else:
        log_Pdot_N.append(np.log(i))
        P_N.append(data["Period"][ct])
    ct += 1

p.circle(P_Y, log_Pdot_Y, fill_color="red", legend="in BS",line_color="red")
p.line(P_Y, log_Pdot_Y,  line_color="red")
p.circle(P_N, log_Pdot_N, fill_color="black", legend="not in BS",line_color="black")
p.line(P_N, log_Pdot_N,  line_color="black")

show(p)
