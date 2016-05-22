import os
import json

import numpy as np
import pandas as pd
import cauldron as cd

results_directory = os.path.abspath(os.path.join('..', '..', '..', 'results'))
data_path = os.path.join(results_directory, *cd.shared.slug)


cd.shared.trial_id = '/'.join(cd.shared.slug)
cd.shared.data_path = data_path

with open(os.path.join(data_path, 'settings.json'), 'r+') as f:
    cd.shared.settings = json.load(f)

with open(os.path.join(data_path, 'status.json'), 'r+') as f:
    cd.shared.status = json.load(f)

csv_files = ['passengers', 'progress', 'queue', 'seated']
for key in csv_files:
    cd.shared.put(
        key,
        pd.read_csv(os.path.join(data_path, '{}.csv'.format(key)))
    )

# ------------------------------------------------------------------------------
# JSON Data
#   Transform the progress DataFrame in to a list of lists for serializing to
#   JSON for access by the animation. Also add the status and settings
#   dictionaries.

passenger_progress = []
for i in range(cd.shared.passengers.shape[0]):
    passenger_progress.append(
        cd.shared.progress['p_{}'.format(i)].tolist()
    )

cd.display.json('project', {
    'passenger_count': cd.shared.passengers.shape[0],
    'progress': passenger_progress,
    'status': cd.shared.status,
    'settings': cd.shared.settings
})

starting_queue = cd.shared.queue.copy(deep=True)
starting_queue['passenger'] = np.NaN
starting_queue['seated'] = 0

for i in range(cd.shared.passengers.shape[0]):
    start_state = cd.shared.progress.loc[0, 'p_{}'.format(i)]
    start_position = int(start_state.split(':')[-1])

    row = starting_queue[starting_queue.aisle == start_position]
    starting_queue.loc[row.index, 'passenger'] = i

cd.shared.starting_queue = starting_queue
