__name__ = "vutsuak"

import pandas as pd
import numpy as np
from bokeh.plotting import output_file, figure, show, ColumnDataSource
from bokeh.models import HoverTool, CustomJS
from bokeh.models.widgets import Panel, Tabs

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

ct = 0

for i in data["Period Derivative"]:
    if data["Binary"][ct] == "Y":
        log_Pdot_Y.append(np.log(i))
        P_Y.append(data["Period"][ct])
    else:
        log_Pdot_N.append(np.log(i))
        P_N.append(data["Period"][ct])
    ct += 1

output_file("plot2.html", title="dot(P) vs P plot")
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
TOOLS = 'box_zoom,box_select,crosshair,resize,reset,wheel_zoom, previewsave'  # sizing tools

p1 = figure(title="dot(P) vs P", x_axis_label='Period (s)', y_axis_label='dot(P)', tools=[hover, TOOLS])
p1.circle(P_Y, log_Pdot_Y, fill_color="red", legend="in BS", line_color="red", source=source1, size=5)
p1.circle(P_N, log_Pdot_N, fill_color="black", legend="not in BS", line_color="black", source=source2, size=5)

tab1 = Panel(child=p1, title="circle")

p2 = figure(title="dot(P) vs P", x_axis_label='Period (s)', y_axis_label='dot(P)')
p2.line(P_Y, log_Pdot_Y, legend="in BS", line_color="red", source=source1)
p2.line(P_N, log_Pdot_N, legend="not in BS", line_color="black", source=source2)
p2.circle(P_Y, log_Pdot_Y, legend="in BS", line_color="red", source=source1)
p2.circle(P_N, log_Pdot_N, legend="not in BS", line_color="black", source=source2)

tab2 = Panel(child=p2, title="line")

p3 = figure(title="dot(P) vs P", x_axis_label='Period (s)', y_axis_label='dot(P)')
p3.arc(P_Y, log_Pdot_Y, legend="in BS",  source=source1,radius=0.01, start_angle=0.4, end_angle=4.8, color="navy")
p3.arc(P_N, log_Pdot_N, legend="not in BS",source=source2,radius=0.01, start_angle=0.4, end_angle=4.8, color="red")

tab3 = Panel(child=p3, title="arc")
tabs = Tabs(tabs=[tab1, tab2, tab3])

show(tabs)
