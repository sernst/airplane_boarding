import os
import pandas as pd
import json

from cauldron import project

data_path = project.shared.data_path

csv_files = ['passengers', 'progress', 'queue', 'seated']
for key in csv_files:
    project.shared.put(
        key,
        pd.read_csv(os.path.join(data_path, '{}.csv'.format(key)))
    )

project.display.workspace(values=False)

# ------------------------------------------------------------------------------
# JSON Data
#   Transform the progress DataFrame in to a list of lists for serializing to
#   JSON for access by the animation. Also add the status and settings
#   dictionaries.

passenger_progress = []
for i in range(project.shared.passengers.shape[0]):
    passenger_progress.append(
        project.shared.progress['p_{}'.format(i)].tolist()
    )
project.display.json('project', {
    'passenger_count': project.shared.passengers.shape[0],
    'progress': passenger_progress,
    'status': project.shared.status,
    'settings': project.shared.settings
})


