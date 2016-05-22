import math

import numpy as np
import plotly.graph_objs as go
from cauldron import plotting
from cauldron import project

progress = project.shared.progress
settings = project.shared.settings
passengers = project.shared.passengers
status = project.shared.status

passenger_count = project.shared.passengers.shape[0]

waiting = []

previous_row = None
for elapsed_time, row in progress.iterrows():
    waiting.append(0)
    for passenger_index in range(passenger_count):
        if previous_row is None:
            continue

        state = row['p_{}'.format(passenger_index)]
        last_state = previous_row['p_{}'.format(passenger_index)]

        if state[0] in ['Q', 'I'] and state == last_state:
            waiting[-1] += 1

    previous_row = row
    waiting[-1] = 100.0 * waiting[-1] / passenger_count

project.display.plotly(
    data=go.Scatter(
        x=np.arange(0, len(waiting), 1) / 60.0,
        y=waiting,
        mode='lines',
        fill='tozeroy',
        line={'color': 'green'}
    ),
    layout=plotting.create_layout(
        title='Passengers Waiting',
        x_label='Boarding Time (minutes)',
        y_label='Waiting (%)',
        y_bounds=[0, 100]
    )
)

stuck_times = passengers['count_stuck'] / 60.0

project.display.plotly(
    data=go.Histogram(
        x=stuck_times,
        nbinsx=math.ceil(status['max_time'] / 60)
    ),
    layout=plotting.create_layout(
        title='Passenger Wait Times',
        x_label='Waiting Time (s)',
        y_label='Frequency (#)'
    )
)
