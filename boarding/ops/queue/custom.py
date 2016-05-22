import os
import typing

import pandas as pd

from boarding import configuration
from boarding.ops.queue import grouping


def populate(
        settings: dict,
        queue: pd.DataFrame,
        passengers: pd.DataFrame
) -> typing.List[int]:

    ps = settings['populate']

    path = ps['path']
    root_path = settings.get('source_path', '')
    if root_path:
        path = os.path.abspath(
            os.path.join(os.path.dirname(root_path), path)
        )

    if not path.endswith('.csv'):
        path += '.csv'

    if not os.path.exists(path):
        raise FileNotFoundError(
            'No such queue population file: "{}"'.format(path)
        )

    df = pd.read_csv(path)

    if 'passenger' not in df.columns:
        raise KeyError(
            'No "passenger" column in queue population file "{}"'.format(path)
        )

    return df['passenger'].tolist()
