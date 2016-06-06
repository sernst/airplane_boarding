from collections import Counter
import typing

import pandas as pd

from boarding.ops import airplane


def calculate_at_time(
        settings: dict,
        progress_row: pd.DataFrame,
        passengers: pd.DataFrame
) -> typing.List[float]:
    """

    :param settings:
    :param progress_row:
    :param passengers:
    :return:
    """

    counter = Counter()

    for passenger_index in range(passengers.shape[0]):
        status = progress_row['p_{}'.format(passenger_index)]
        state, position = status.split(':', 1)
        position = int(position)

        if position < 0:
            continue

        aisle = int(passengers.loc[passenger_index, 'aisle'])
        counter[aisle] += 1

    densities = []
    for aisle_index in range(airplane.aisle_count(settings)):
        seat_count = airplane.seats_in_aisle(aisle_index, settings)
        densities.append(counter[aisle_index] / seat_count)

    return densities


def calculate(
        settings: dict,
        progress: pd.DataFrame,
        passengers: pd.DataFrame
) -> typing.List[typing.List[float]]:
    """

    :param settings:
    :param progress:
    :param passengers:
    :return:
    """

    densities = []

    for time in range(progress.shape[0]):
        densities.append(calculate_at_time(
            settings=settings,
            progress_row=progress.iloc[time],
            passengers=passengers
        ))

    return densities



