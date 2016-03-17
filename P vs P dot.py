__name__ = "vutsuak"

import pandas as pd
import numpy as np
from bokeh.plotting import output_file, figure, show, ColumnDataSource
from bokeh.models import HoverTool

data = pd.read_csv("pulsar_data_test.csv")
log_Pdot_Y = []  # created  separate list to show separation of data,later we can do it using lesser space
log_Pdot_N = []  # N means not in binary system
P_Y = []  # in binary system as Y
P_N = []

TOA = []
DM = []
RMS = []
Pulsar=[]
x=0

for i in data:
    x=i
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

output_file("plot.html", title="P derivative vs P plot")
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
hover = HoverTool(
        tooltips="""
        <div>
            <div>
                <span style="font-size: 10px;">Index</span>
                <span style="font-size: 10px; color: #966;">[$index]</span>
            </div>
             <div>
                <span style="font-size: 10px;">Pulsar</span>
                <span style="font-size: 10px; color: #696;">@Pulsar</span>
            </div>
            <div>
                <span style="font-size: 10px;">Location</span>
                <span style="font-size: 10px; color: #696;">($x, $y)</span>
            </div>
             <div>
                <span style="font-size: 10px;">Time Of Arrival</span>
                <span style="font-size: 10px; color: #696;">@TOA</span>
            </div>
             <div>
                <span style="font-size: 10px;">Dispersion Measure</span>
                <span style="font-size: 10px; color: #696;">@DM</span>
            </div>
             <div>
                <span style="font-size: 10px;">Root Mean Square</span>
                <span style="font-size: 10px; color: #696;">@RMS</span>
            </div>
        </div>
        """
)
TOOLS = 'box_zoom,box_select,crosshair,resize,reset,wheel_zoom, previewsave'    #sizing tools

p = figure(title="Period derivative vs Period", x_axis_label='Period (s)', y_axis_label='dot(P)', tools=[hover,TOOLS])

p.circle(P_Y, log_Pdot_Y, fill_color="red", legend="in BS", line_color="red", source=source1, size=5)
p.circle(P_N, log_Pdot_N, fill_color="black", legend="not in BS", line_color="black", source=source2, size=5)

show(p)

#add widgets like buttons etc