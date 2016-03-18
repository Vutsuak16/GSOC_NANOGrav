__name__ = "vutsuak"

import pandas as pd
import numpy as np
from bokeh.plotting import output_file, figure, show, ColumnDataSource, hplot
from bokeh.models import CustomJS

data = pd.read_csv("pulsar_data_test.csv")
log_Pdot_Y = []  # created  separate list to show separation of data,later we can do it using lesser space
log_Pdot_N = []  # N means not in binary system
P_Y = []  # in binary system as Y
P_N = []

TOA = []
DM = []
RMS = []
Pulsar = []
x = 0

for i in data:
    x = i
    break

for i in data[x]:
    Pulsar.append(i)
for i in data["TOAs"]:
    TOA.append(i)
for i in data["DM"]:
    DM.append(i)
for i in data["RMS"]:
    RMS.append(i)

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

output_file("plot3.html", title="P derivative vs P plot")
source1 = ColumnDataSource(
        data=dict(
                Pulsar=Pulsar,
                x=P_Y,
                y=log_Pdot_Y,
                TOA=TOA,
                DM=DM,
                RMS=RMS,
        )
)
source2 = ColumnDataSource(
        data=dict(
                Pulsar=Pulsar,
                x=P_N,
                y=log_Pdot_N,
                TOA=TOA,
                DM=DM,
                RMS=RMS,
        )
)

p = figure(title="dot(P) vs P", x_axis_label='Period (s)', y_axis_label='dot(P)',tools="lasso_select")

p.circle(P_Y, log_Pdot_Y, fill_color="red", legend="in BS", line_color="red", source=source1, size=5)
p.circle(P_N, log_Pdot_N, fill_color="black", legend="not in BS", line_color="black", source=source2, size=5)

q = figure(title="dot(P) vs P", x_axis_label='Period (s)', y_axis_label='dot(P)',tools="lasso_select")
s1 = ColumnDataSource(data=dict(x=[], y=[]))
s2 = ColumnDataSource(data=dict(x=[], y=[]))
q.circle(P_Y, log_Pdot_Y, fill_color="red", legend="in BS", line_color="red", source=s1, size=5)
q.circle(P_N, log_Pdot_N, fill_color="black", legend="not in BS", line_color="black", source=s2, size=5)

source1.callback = CustomJS(args=dict(s1=s1), code="""
        var inds = cb_obj.get('selected')['1d'].indices;
        var d1 = cb_obj.get('data');
        var d2 = s1.get('data');
        d2['x'] = []
        d2['y'] = []
        for (i = 0; i < inds.length; i++) {
            d2['x'].push(d1['x'][inds[i]])
            d2['y'].push(d1['y'][inds[i]])
        }
        s1.trigger('change');
    """)
source2.callback = CustomJS(args=dict(s2=s2), code="""
        var inds = cb_obj.get('selected')['1d'].indices;
        var d1 = cb_obj.get('data');
        var d2 = s2.get('data');
        d2['x'] = []
        d2['y'] = []
        for (i = 0; i < inds.length; i++) {
            d2['x'].push(d1['x'][inds[i]])
            d2['y'].push(d1['y'][inds[i]])
        }
        s2.trigger('change');
    """)

layout = hplot(p, q)

show(layout)

# add widgets like buttons etc
