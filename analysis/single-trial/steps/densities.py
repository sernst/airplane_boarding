import numpy as np
import cauldron as cd
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource

from boarding.analysis import density
from boarding.ops import airplane
from boarding.echo import time as pretty_time

settings = cd.shared.settings
raw_densities = density.calculate(
    settings=settings,
    progress=cd.shared.progress,
    passengers=cd.shared.passengers
)

densities = []
time_slices = []

time_delta = max(1, int(0.05 * cd.shared.status['elapsed']))
for i in range(0, len(raw_densities), time_delta):
    time_slices.append(pretty_time(i))
    densities.append(raw_densities[i])

colormap = list(reversed([
    "#641918",
    "#ad3029",
    "#ca9653",
    "#e4ab59",
    "#36b3e4",
    "#86e4c7",
    "#87e463"
]))

xname = []
yname = []
color = []
alpha = []
times = []

for i in range(len(densities)):
    for aisle_index in range(airplane.aisle_count(settings)):
        xname.append(aisle_index + 1)
        yname.append(-i)
        times.append(time_slices[i])

        alpha.append(0.75)
        dense = densities[i][aisle_index]
        if dense < 0.01:
            color.append('#CCCCCC')
        else:
            color_index = int(round((len(colormap) - 1) * dense))
            color.append(colormap[color_index])

source = ColumnDataSource(data=dict(
    xname=['{}'.format(x) for x in xname],
    yname=['{}'.format(x) for x in yname],
    times=times,
    colors=color,
    alphas=alpha,
    count=np.array(densities).flatten(),
))

p = figure(
    title="Density vs Boarding Time",
    x_axis_location="above",
    tools="resize,hover,save",
    x_range=[0, airplane.aisle_count(cd.shared.settings) + 1],
    y_range=[-len(densities) - 1, 1]
)

p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "10pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = np.pi / 3

p.rect(
    'xname', 'yname', 0.9, 0.9,
    source=source,
    color='colors',
    alpha='alphas',
    line_color=None
)

p.select_one(HoverTool).tooltips = [
    ('Row', '@xname'),
    ('Time', '@times'),
    ('Density', '@count'),
]

cd.display.bokeh(p)

