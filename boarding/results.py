import os
import shutil
import json

import pandas as pd

from boarding import echo
from boarding.ops import queue as queue_ops


def create(
        settings: dict,
        queue: pd.DataFrame,
        passengers: pd.DataFrame) -> dict:
    """
    :param settings:
        Configuration settings for the current trial
    :param queue:
        The queue data frame for the trial
    :param passengers:
        The passengers data frame for the trial
    """

    progress = create_progress(settings, passengers)
    status = create_status(settings, queue, passengers, progress)

    return {
        'passengers': passengers,
        'queue': queue,
        'settings': settings,
        'status': status,
        'progress': progress,
        'seated': create_seated(settings, passengers)
    }


def create_progress(
        settings: dict,
        passengers: pd.DataFrame
) -> pd.DataFrame:
    """
    :param settings:
        Configuration settings for the current trial
    :param passengers:
        The passengers data frame for the trial
    """

    columns = ['p_{}'.format(x) for x in range(0, passengers.shape[0], 1)]
    columns.insert(0, 'time')
    columns.insert(0, 'progress')
    columns.insert(0, 'aisle_density')

    df = pd.DataFrame(columns=columns)
    return df


def create_seated(
        settings: dict,
        passengers: pd.DataFrame) -> pd.DataFrame:
    """
    :param settings:
        Configuration settings for the current trial
    :param passengers:
        The passengers data frame for the trial
    """

    passenger_index = []
    seat_names = []
    seated_time = []

    for index, passenger in passengers.iterrows():
        passenger_index.append(index)
        seat_names.append(
            '{}{}'.format(passenger['aisle'], passenger['letter'])
        )
        seated_time.append(None)

    return pd.DataFrame({
        'passenger': passenger_index,
        'seat': seat_names,
        'time': seated_time
    })


def create_status(
        settings: dict,
        queue: pd.DataFrame,
        passengers: pd.DataFrame,
        progress: pd.DataFrame,
        **kwargs) -> dict:
    """
    :param settings:
        Configuration settings for the current trial
    :param queue:
        The queue data frame for the trial
    :param passengers:
        The passengers data frame for the trial
    :param progress:
        The current progress data frame for the snapshot
    """

    passenger_count = passengers.shape[0]
    queue_size = queue_ops.size(settings, queue)

    return {
        'progress': 1.0 - queue_size / passenger_count,
        'time': echo.time(progress.shape[0]),
        'elapsed': progress.shape[0]
    }


def update(result: dict) -> dict:
    """
    :param result
        The current result object that will be updated with values
    """

    result['status'] = create_status(**result)
    result['progress'] = update_progress(**result)
    result['seated'] = update_seated(**result)

    return result


def update_progress(
        status: dict,
        settings: dict,
        progress: pd.DataFrame,
        queue: pd.DataFrame,
        passengers: pd.DataFrame,
        **kwargs
) -> pd.DataFrame:
    """
    :param status:
        The current status of the simulation
    :param settings:
        Configuration settings for the current trial
    :param progress:
        The current progress data frame for the snapshot, which will be
        replaced by the one returned
    :param queue:
        The queue data frame for the trial
    :param passengers:
        The passengers data frame for the trial
    """

    row = dict(
        progress=status['progress'],
        time=status['time']
    )

    aisle_vacancies = []

    for queue_index in range(queue.shape[0]):
        queue_item = queue.loc[queue_index]
        passenger_index = queue_item['passenger']

        if queue_item['aisle'] >= 0:
            aisle_vacancies.append(0 if passenger_index is None else 1)

        if passenger_index is not None:
            key = 'p_{}'.format(passenger_index)
            row[key] = 'Q:{}'.format(queue_item['aisle'])

    seated = passengers.query('delay_interchange > 0')
    for passenger_index, passenger in seated.iterrows():
        key = 'p_{}'.format(passenger_index)
        row[key] = '{}:{}'.format(
            'O' if passenger['seated'] else 'I',
            passenger['aisle']
        )

    seated = passengers.query('seated and delay_interchange == 0')
    for passenger_index, passenger in seated.iterrows():
        key = 'p_{}'.format(passenger_index)
        row[key] = 'S:{}'.format(passenger['aisle'])

    row['aisle_density'] = sum(aisle_vacancies)/len(aisle_vacancies)

    return progress.append(row, ignore_index=True)


def update_seated(
        status: dict,
        settings: dict,
        seated: pd.DataFrame,
        passengers: pd.DataFrame,
        **kwargs
) -> pd.DataFrame:
    """
    :param status:
        The current status of the simulation
    :param settings:
        Configuration settings for the current trial
    :param seated:
        The current seated data frame for the snapshot, which will be
        replaced by the one returned
    :param passengers:
        The passengers data frame for the trial
    """

    for index, passenger in passengers.query('seated').iterrows():
        if seated.loc[index, 'time'] is None:
            seated.loc[index, 'time'] = status['elapsed']

    return seated


def save(directory: str, result: dict):
    """
    :param directory:
        The directory where the trial results should be saved

    :param result:
        The results dictionary containing all of the results to be written
    """

    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

    for key, value in result.items():
        if key == 'status':
            value = final_status(result)

        if hasattr(value, 'to_csv'):
            # Pandas data frames are saved to csv
            value.to_csv(os.path.join(directory, '{}.csv'.format(key)))
        else:
            # Dictionaries are saved as json files
            path = os.path.join(directory, '{}.json'.format(key))
            with open(path, 'w') as f:
                json.dump(value, f)


def final_status(result: dict) -> dict:
    max_seats = []
    aisle_count = 0
    available_seats = 0

    for section in result['settings']['airplane']:
        seats = section['seats']
        index = 0

        aisle_count += section['rows']
        available_seats += section['rows'] * sum(seats)

        while index < min(len(seats), len(max_seats)):
            max_seats[index] = max(max_seats[index], seats[index])
            index += 1

        while index < len(seats):
            max_seats.append(seats[index])
            index += 1

    out = {
        'aisle_count': aisle_count,
        'max_time': result['status']['elapsed'],
        'available_seats': available_seats,
        'max_seats_in_row': max_seats
    }
    out.update(result['status'])
    return out


def load(directory: str) -> dict:
    """ Loads results from files stored in the specified directory into a
        results object identical to the one

    :param directory:
        The absolute path to the directory where the results files should be
        loaded from
    """

    result = dict()

    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if item.endswith('.csv'):
            result[item[:-4]] = pd.read_csv(path)
        elif item.endswith('.json'):
            with open(path, 'r') as f:
                result[item[:-5]] = json.load(f)

    return result
