import plotly.graph_objs as go

from cauldron import project
from cauldron import plotting

df = project.shared.progress

data = go.Scatter(
    x=df.index / 60.0,
    y=100.0 * df['progress'],
    mode='lines',
    fill='tozeroy'
)

project.display.plotly(
    data=data,
    layout=plotting.create_layout(
        title='Seating Progress',
        x_label='Boarding Time (minutes)',
        y_label='Completion (%)'
    )
)

rate = []

for index in range(1, df.shape[0] - 1):
    before = df.iloc[index - 1]['progress']
    after = df.iloc[index + 1]['progress']
    rate.append(100.0 * (after - before) / 2.0)

# Add values at beginning and end to maintain shape
rate.append(rate[-1])
rate.insert(0, rate[0])

data = go.Scatter(
    x=df.index / 60.0,
    y=rate,
    mode='lines',
    fill='tozeroy'
)

project.display.plotly(
    data=data,
    layout=plotting.create_layout(
        title='Seating Progress Rate',
        x_label='Boarding Time (minutes)',
        y_label='Boarding Rate (%)'
    )
)
