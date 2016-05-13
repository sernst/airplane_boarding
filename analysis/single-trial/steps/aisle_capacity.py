import numpy as np
import plotly.graph_objs as go
import measurement_stats as mstats

from cauldron import project
from cauldron import plotting

progress = project.shared.progress
settings = project.shared.settings

passenger_count = project.shared.passengers.shape[0]
aisle_count = project.shared.status['aisle_count']

aisle_capacity = []

for elapsed_time, row in progress.iterrows():
    aisle_capacity.append(0)
    for passenger_index in range(passenger_count):
        state = row['p_{}'.format(passenger_index)]
        if state[0] not in ['Q', 'I']:
            continue

        aisle_index = int(state.split(':')[-1])
        if aisle_index >= 0:
            aisle_capacity[-1] += 1

    aisle_capacity[-1] = 100.0 * aisle_capacity[-1] / aisle_count

project.display.plotly(
    data=go.Scatter(
        x=np.arange(0, len(aisle_capacity), 1) / 60.0,
        y=aisle_capacity,
        mode='lines',
        fill='tozeroy',
        line={'color': 'purple'}
    ),
    layout=plotting.create_layout(
        title='Aisle Capacity',
        x_label='Boarding Time (minutes)',
        y_label='Capacity',
        y_bounds=[0, 100]
    )
)

distribution = mstats.create_distribution(
    measurements=aisle_capacity,
    uncertainties=50.0 / aisle_count
)
x_values = mstats.distributions.uniform_range(distribution, 3, 1024)

project.display.plotly(
    data=go.Scatter(
        x=x_values,
        y=distribution.probabilities_at(x_values),
        mode='lines',
        fill='tozeroy',
        line={'color': 'purple'}
    ),
    layout=plotting.create_layout(
        title='Aisle Capacity KDE Distribution',
        x_label='Aisle Capacity (%)',
        y_label='Expectation Value (au)'
    )
)
