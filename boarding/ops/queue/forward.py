import typing
import random

import pandas as pd

from boarding import configuration
from boarding.ops.queue import grouping


def populate(
        settings: dict,
        queue: pd.DataFrame,
        passengers: pd.DataFrame
) -> typing.List[int]:
    """
    Assigns passenger indexes within the queue data frame's passenger
    column from the back of the plane to the front.

    :param settings:
        Configuration settings for the current trial
    :param queue:
        The queue data frame that is populated by the method
    :param passengers:
        The passenger data frame containing the passenger manifest
    """

    ps = settings['populate']

    aisle_groups = grouping.order_by(
        grouping.chunks(settings, passengers, queue),
        configuration.fetch_put(ps, 'group_order', 'FORWARD'),
        'FORWARD'
    )

    shuffle = configuration.fetch_put(ps, 'shuffle', False)

    out = []
    for g in grouping.to_passenger_indexes(aisle_groups, passengers):
        if not shuffle:
            g.sort()
        else:
            random.shuffle(g)
        out.extend(g)

    return out


