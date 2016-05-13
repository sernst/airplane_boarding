import pandas as pd


def calculate(settings: dict, progress: pd.DataFrame):
    """

    :param settings:
    :param progress:
    :return:
    """

    passenger_count = settings['passenger_count']

    waiting = []

    previous_row = None
    for elapsed_time, row in progress.iterrows():
        waiting.append(0)
        for passenger_index in range(passenger_count):
            if previous_row is None:
                continue

            position = row[str(passenger_index)]
            last_position = previous_row[str(passenger_index)]

            if position == last_position:
                waiting[-1] += 1

        previous_row = row
        waiting[-1] = 100.0 * waiting[-1] / passenger_count
