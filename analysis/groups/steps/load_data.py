import glob
import os
import json

import pandas as pd
from cauldron import project

methods = {
    'b': 'Back',
    'f': 'Front',
    'r': 'Rand'
}

groups = {
    'two': [2, 0],
    'twogs': [2, 0]
}

data_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', '..', 'results')
)

status_glob = glob.iglob(
    '{}/**/status.json'.format(data_path),
    recursive=True
)

data = []

for path in status_glob:
    trial_name = os.path.dirname(path).split(os.sep)[-1]
    parts = trial_name.split('-')

    collection = parts[0]
    if collection not in groups:
        continue

    boarding_method = parts[1]
    group_count = int(parts[2][:-1])

    if len(parts) > 3:
        trial_index = int(parts[3][1:])
    else:
        trial_index = 1

    with open(path, 'r+') as f:
        status = json.load(f)

    trial_label = '{} {}'.format(
        methods[boarding_method],
        '{}'.format(trial_index).zfill(2) if boarding_method == 'r' else ''
    ).strip()

    status.update(dict(
        trial_index=trial_index,
        trial_label=trial_label,
        collection=collection,
        boarding_method=boarding_method,
        board_method_label=methods[boarding_method],
        group_count=group_count,
        seating_delay=groups[collection][0],
        interchange_delay=groups[collection][1]
    ))
    data.append(status)

df = pd.DataFrame(data)
project.shared.data = df

project.display.table(df, scale=0.5)
print('Shape:', df.shape)
