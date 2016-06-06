from collections import Counter

import numpy as np
import pandas as pd
import cauldron as cd
from cauldron import plotting
import plotly.graph_objs as go


progress = cd.shared.progress # type: pd.DataFrame
passengers = cd.shared.passengers # type: pd.DataFrame

column_counts = []
columns_progress = []
for distance in range(10):
    count = passengers[passengers.window_distance == distance].shape[0]
    if count == 0:
        break
    column_counts.append(count)
    columns_progress.append([])

for index, entry in progress.iterrows():
    seated_counter = Counter()
    for passenger_index in range(passengers.shape[0]):
        status = entry['p_{}'.format(passenger_index)]
        if status[0] in ['Q', 'I']:
            continue

        passenger = passengers.iloc[passenger_index]
        seated_counter[int(passenger.window_distance)] += 1

    for i in range(len(column_counts)):
        columns_progress[i].append(
            100.0 * seated_counter[i] / column_counts[i]
        )

traces = []

for i in range(len(columns_progress)):
    column_progress = columns_progress[i]

    if i == 0:
        name = 'Window'
    elif i == (len(columns_progress) - 1):
        name = 'Aisle'
    else:
        name = 'Middle'

    traces.append(go.Scatter(
        x=np.arange(0, len(column_progress), 1),
        y=column_progress,
        mode='markers',
        marker={'color': plotting.get_color(i, 0.7)},
        name=name
    ))

cd.display.plotly(
    data=traces,
    layout=plotting.create_layout(
        title='Progress By "Column"',
        x_label='Time (s)',
        y_label='Progress (%)'
    )
)
