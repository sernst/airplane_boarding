import pandas as pd


def seating(settings: dict, queue: pd.DataFrame, passengers: pd.DataFrame):
    """
    Validates that no passengers have missed their seat assignments and are
    located in an aisle position greater than the one where their seat resides.

    :param settings:
    :param queue:
    :param passengers:
    """

    for index, queue_entry in queue.iterrows():
        if queue_entry['aisle'] < 0:
            continue

        passenger_index = queue_entry['passenger']
        if passenger_index is None:
            continue

        if passengers.loc[passenger_index, 'aisle'] < queue_entry['aisle']:
            raise ValueError(
                'Invalid location "{}" for passenger seated in "{}"'.format(
                    queue_entry['aisle'],
                    passengers.loc[passenger_index, 'aisle']
            ))
