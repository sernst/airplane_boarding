import pandas as pd

from boarding import configuration
from boarding import results
from boarding import simulate
from boarding.ops import passengers as passenger_ops
from boarding.ops import queue as queue_ops


def create_passenger_data(
        settings_path: str,
        save_path: str = None
) -> pd.DataFrame:
    """
    Uses the specified settings file to create a passenger manifest data frame
    and returns the data frame. If a save path is specified, the data frame is
    also saved to that csv file. If no save path is specified, the data frame
    is saved alongside the settings file.

    :param settings_path:
        The path to the simulation configuration file for which the passenger
        data should be created
    :param save_path:
        An optional location where the passenger data will be saved. If
        omitted, the data will be saved to the default location alongside the
        settings file with the name "[SETTINGS_FILENAME]_passengers.csv"

    :return:
        The passenger manifest data frame for the specified settings file
    """

    settings = configuration.load(settings_path)
    df = passenger_ops.create(settings)

    if not save_path:
        save_path = '{}_passengers.csv'.format(settings_path[:-5])
        df.to_csv(save_path)

    return df


def create_empty_queue_data(
        settings_path: str,
        save_path: str = None
) -> pd.DataFrame:
    """
    Uses the specified settings file to create an empty queue data frame
    and returns the data frame. If a save path is specified, the data frame is
    also saved to that csv file. If no save path is specified, the data frame
    is saved alongside the settings file.

    :param settings_path:
        The path to the simulation configuration file for which the queue data
        should be created
    :param save_path:
        An optional location where the queue data will be saved. If
        omitted, the data will be saved to the default location alongside the
        settings file with the name "[SETTINGS_FILENAME]_queue.csv"

    :return:
        An empty queue data frame for the specified settings file
    """

    settings = configuration.load(settings_path)
    df = queue_ops.create(settings)

    if not save_path:
        save_path = '{}_queue.csv'.format(settings_path[:-5])
        df.to_csv(save_path)

    return df


def run(settings_path: str, results_directory: str) -> dict:
    """
    Runs the simulation using the configuration settings loaded from the
    specified settings path and saves the results in the specified directory

    :param settings_path:
        The path to a json file where the simulation configuration settings
        reside
    :param results_directory:
        The path to a directory where the simulation results will be written
    :return:
        A dictionary containing the collected results
    """

    r = simulate.run(settings_path)
    results.save(results_directory, r)
    return r

