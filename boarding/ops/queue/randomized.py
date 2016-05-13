import random
import typing

import pandas as pd

from boarding import configuration
from boarding.ops.queue import grouping


def populate(
        settings: dict,
        queue: pd.DataFrame,
        passengers: pd.DataFrame
) -> typing.List[int]:
    """
    Randomly assigns passenger indexes within the queue data frame's passenger
    column.

    :param settings:
        Configuration settings for the current trial
    :param queue:
        The queue data frame that is populated by the method
    :param passengers:
        The passenger data frame containing the passenger manifest
    """

    aisle_groups = grouping.order_by(
        grouping.chunks(settings, passengers, queue),
        configuration.fetch_put(settings['populate'], 'group_order', 'RANDOM'),
        'RANDOM'
    )

    groups = grouping.to_passenger_indexes(aisle_groups, passengers)

    permutation = []
    for group in groups:
        random.shuffle(group)
        permutation.extend(group)

    return permutation
