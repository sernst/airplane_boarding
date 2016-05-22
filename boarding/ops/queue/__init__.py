import sys
import logging

import pandas as pd

from boarding.ops import airplane
from boarding.ops.queue import randomized
from boarding.ops.queue import backward
from boarding.ops.queue import forward


def create(settings: dict, passengers: pd.DataFrame = None) -> pd.DataFrame:
    """
    Creates the queue data frame for the trial based on the specified settings
    and the passenger data and returns that as a data frame.

    :param settings:
        Configuration settings for the current trial
    :param passengers:
        The passengers data frame for the trial
    """

    aisle_count = airplane.aisle_count(settings)

    if passengers is None:
        passenger_count = airplane.seat_count(settings)
    else:
        passenger_count = passengers.shape[0]

    positions = []

    for index in range(-passenger_count, aisle_count):
        positions.append(dict(
            aisle=index,
            passenger=None,
            seated=0
        ))

    return pd.DataFrame(positions)


def size(settings: dict, queue: pd.DataFrame) -> int:
    """
    Returns the number of passengers currently in the queue

    :param settings:
        Configuration settings for the current trial
    :param queue:
        The queue data frame for the trial
    """

    return len(queue['passenger'].unique()) - 1


def get_population_settings(settings: dict) -> dict:
    """
    Retrieves the population specific settings from the trial settings object
    and returns that value. If no population type was specified by the settings
    object, the default 'RANDOM' type is used.

    :param settings:
        Configuration settings for the current trial
    """

    if 'populate' not in settings:
        settings['populate'] = {
            'type': 'RANDOM'
        }

    ps = settings['populate']

    if isinstance(ps, str):
        ps = {'type': ps}
        settings['populate'] = ps

    defaults = dict(
        type='RANDOM',
        groups=1,
        group_order='DEFAULT'
    )

    for key, value in defaults.items():
        if key not in ps:
            ps[key] = value

    try:
        ps['type'].upper()
        return ps
    except Exception:
        logging.getLogger('boarding').exception(
            'Invalid or missing "populate" value in trial configs'
        )
        raise


def populate(
        settings: dict,
        queue: pd.DataFrame,
        passengers: pd.DataFrame
) -> pd.DataFrame:
    """
    Populates the initial queue with passengers according to the settings for
    the trial and returns the fully populated queue data frame.

    :param settings:
        Configuration settings for the current trial
    :param queue:
        The queue data frame for the trial
    :param passengers:
        The passengers data frame for the trial
    """

    populate_settings = get_population_settings(settings)
    populate_type = populate_settings['type']
    populate_function = None

    if populate_type == 'RANDOM':
        populate_function = randomized.populate
    elif populate_type == 'BACKWARD':
        populate_function = backward.populate
    elif populate_type == 'FORWARD':
        populate_function = forward.populate
    elif populate_type == 'CUSTOM':
        populate_function = custom.populate

    if populate_function is None:
        logging.getLogger('boarding').critical(
            'Unrecognized "populate" type in trial configs: "{}"'.format(
                settings.get('populate')
            )
        )
        sys.exit(1)

    population = populate_function(
        settings=settings,
        queue=queue,
        passengers=passengers
    )

    # Reverse the order here because population index 0 should be the first
    # passenger to board the plane and the queue is filled up from back to
    # front in the for loop below
    population.reverse()

    for queue_index, passenger_index in enumerate(population):
        queue.loc[queue_index, 'passenger'] = passenger_index

    return queue

