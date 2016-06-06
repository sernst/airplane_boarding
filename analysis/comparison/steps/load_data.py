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
    'ideal': [0, 0],
    'one': [1, 0],
    'two': [2, 0],
    'five': [5, 0],
    'ten': [10, 0],
    'i_one': [0, 1],
    'i_two': [0, 2],
    'i_five': [0, 5],
    'i_ten': [0, 10],
    'twogs': [2, 0],
    'twogis': [2, 2]
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

df['pp_dev'] = 0
df['fitness'] = 0


for method in df['boarding_method'].unique():
    ideal = df[
        (df['boarding_method'] == method) &
        (df['seating_delay'] == 0) &
        (df['interchange_delay'] == 0)
    ].iloc[0]

    query = (
        (df['boarding_method'] == method) &
        (
            (df['seating_delay'] > 0) |
            (df['interchange_delay'] > 0)
        )
    )

    df.loc[query, 'pp_dev'] = abs(
        df.loc[query, 'elapsed'] - ideal['elapsed']
    ) / df.loc[query, 'available_seats']

    df.loc[query, 'fitness'] = (
        df.loc[query, 'seating_delay'] + df.loc[query, 'interchange_delay']
    ) / df.loc[query, 'pp_dev']

project.display.table(df, scale=0.5)
print('Shape:', df.shape)
