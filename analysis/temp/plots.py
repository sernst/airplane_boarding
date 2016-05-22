import math

import cauldron as cd
import numpy as np
from plotly import graph_objs as go

x = np.linspace(0, 4 * math.pi, 200)

y = (
    0.25 * np.sin(x) +
    0.1 * np.sin(2 * x) +
    0.667 * np.sin(3 * x) +
    0.1 * np.sin(4 * x) +
    0.05 * np.sin(5 * x) +
    0.05 * np.sin(6 * x)
)

traces = [go.Scatter(
    x=x,
    y=y,
    name='Function'
)]

cd.display.plotly(
    data=traces,
    layout={}
)

y1 = 0.25 * np.sin(x)

traces.append(go.Scatter(
    x=x,
    y=y1,
    name='sin(x)'
))

cd.display.plotly(
    data=traces,
    layout={}
)

y2 = y1 + 0.1 * np.sin(2 * x)

traces.append(go.Scatter(
    x=x,
    y=y2,
    name='sin(2x)'
))

cd.display.plotly(
    data=traces,
    layout={}
)

y3 = y2 + 0.667 * np.sin(3 * x)

traces.append(go.Scatter(
    x=x,
    y=y3,
    name='sin(3x)'
))

cd.display.plotly(
    data=traces,
    layout={}
)


