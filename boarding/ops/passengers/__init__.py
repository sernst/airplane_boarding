import math

import pandas as pd
import numpy as np
import string

from boarding.ops import queue as queue_ops
from boarding.ops.passengers import step


def create(settings: dict) -> pd.DataFrame:
    """
    Creates a data frame representing the passengers for the flight based on
    the trial configuration settings

    :param settings:
        Configuration settings for the current trial
    """

    airplane = settings['airplane']
    if not isinstance(airplane, (list, tuple)):
        airplane['class'] = airplane.get('class', 'standard')
        airplane = [airplane]

    data_frames = []
    row_offset = 0

    for section in airplane:
        df = create_class_section(section, row_offset)
        row_offset = df.iloc[-1]['aisle'] + 1
        data_frames.append(df)

    return pd.concat(data_frames, ignore_index=True)


def create_class_section(section: dict, row_offset: int = 0) -> pd.DataFrame:
    """
    Creates a data frame populated with passenger information for the specified
    section (i.e. class) of the airplane. The data frame contains the
    following columns:

        - aisle: The aisle index where the each passenger's seat resides.
                This is calculated based on the seat assignment for the
                passenger (i.e. their index) and the configuration of the
                airplane as specified by the trial configs.
        - side: The side of the airplane where the passenger's seat resides.
                Values are 'L' for left and 'R' for right. These directions
                are relative to the airplane, not the passengers. That
                means that 'L' is the left side of the airplane.
        - column: The column in which the passenger's seat resides. A
                value of 0 indicates the left-most column of seats in that
                section and increasing values are to the right.
        - letter: The letter representation of the seat column within the
                section. For example, the leftmost column would have a
                letter 'A'. This is a friendly format for columns intended
                to make results more human readable.
        - aisle_distance: The number of seats between this passenger's seat
                and the aisle. A value of zero indicates that the seat is
                an aisle seat. In a section with 3 seats on a side of the
                airplane, a value of 2 would be the window seat because
                there are 2 seats between the aisle and that seat.
        - moved: A boolean specifying whether or not the passenger has
                moved during a given simulation time step. Defaults to
                False and is reset to False at the beginning of each
                new iteration of the simulation until it is complete.
        - delay: The delay experience by the passenger when transitioning
                from one state to another. It defaults to zero, and is
                modified during the simulation loop, when a transition
                delay is required.
        - seated: A boolean that specified whether or not the passenger
                has been seated, in which case they are no longer in the
                queue.
    """

    row_count = section['rows']

    seat_arrangement = section['seats']
    if not isinstance(seat_arrangement, (list, tuple)):
        seat_arrangement = [
            math.ceil(0.5 * seat_arrangement),
            seat_arrangement - math.ceil(0.5 * seat_arrangement)
        ]
    seats_per_row = sum(seat_arrangement)

    passenger_count = seats_per_row * row_count

    row = []
    side = []
    column = []
    aisle_distance = []
    letter = []
    moved = []
    delay = []
    seated = []
    interchanged = []
    delay_interchange = []
    count_interchange = []
    count_stuck = []

    for index in range(passenger_count):
        row.append(row_offset + math.floor(index / seats_per_row))
        column.append(index % seats_per_row)
        letter.append(string.ascii_uppercase[column[-1]])

        if column[-1] < seat_arrangement[0]:
            side.append('L')
            aisle_distance.append(seat_arrangement[0] - 1 - column[-1])
        else:
            side.append('R')
            aisle_distance.append(column[-1] - seat_arrangement[0])

        moved.append(False)
        seated.append(False)
        delay.append(0)
        delay_interchange.append(0)
        count_stuck.append(0)
        count_interchange.append(0)
        interchanged.append(False)

    return pd.DataFrame({
        'aisle': row,
        'side': side,
        'column': column,
        'aisle_distance': aisle_distance,
        'letter': letter,

        'moved': moved,
        'seated': seated,
        'delay': delay,
        'interchanged': interchanged,
        'delay_interchange': delay_interchange,
        'count_interchange': count_interchange,
        'count_stuck': count_stuck
    })


def move(settings: dict, passengers: pd.DataFrame, queue: pd.DataFrame):
    """ Runs a relaxation loop that moves all passengers forward one iteration

    :param settings:
        Configuration settings for the current trial
    :param passengers:
        The passengers data frame for the trial
    :param queue:
        The current queue data frame on which to operate
    """

    passengers['moved'] = False

    index_pool = list(np.random.permutation(queue.shape[0]))
    while len(index_pool) > 0:
        step.forward(index_pool, settings, queue, passengers)

    # Confirm that all passengers have been moved during this move action
    moved = passengers.query('moved == True').shape[0]
    if moved < queue_ops.size(settings, queue):
        raise RuntimeError('Passengers.move failed')
