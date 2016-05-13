import math

import pandas as pd


def time(elapsed_seconds: int) -> str:
    """
    Converts the elapsed_seconds argument into a time string formatted as
    'HH:MM:SS'

    :param elapsed_seconds:
        The number of seconds that has elapsed since a reference zero time
    """

    minutes = math.floor(elapsed_seconds/60.0)
    seconds = elapsed_seconds - 60*minutes
    return '00:{:0>2}:{:0>2}'.format(minutes, seconds)


def status(queue: pd.DataFrame, passengers: pd.DataFrame) -> str:
    """
    Returns a string that outlines the status of the boarding process for the
    current trial

    :param queue:
        The passenger queue for the current trial
    :param passengers:
        The passengers in the current trial
    """

    def to_passenger_string(i):
        if i is None:
            return None
        return '{}@{}'.format(i, passengers.loc[i, 'aisle'])

    waiting = []
    out = []

    for index, queue_entry in queue.iterrows():
        passenger_index = queue_entry['passenger']
        queue_aisle = queue_entry['aisle']

        if queue_aisle < 0:
            v = to_passenger_string(passenger_index)
            if v:
                waiting.append(v)
            continue

        out.append('{}: {} | {}'.format(
            '{}'.format(queue_aisle).ljust(4),
            to_passenger_string(passenger_index),
            int(queue_entry['seated'])*'*'
        ))

    return '{}\nWAITING: {}'.format(
        '\n'.join(out),
        len(waiting) if waiting else 'None')
