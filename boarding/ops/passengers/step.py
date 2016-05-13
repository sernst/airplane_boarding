import typing

import pandas as pd


def forward(
        index_pool: list,
        settings: dict,
        queue: pd.DataFrame,
        passengers: pd.DataFrame,
        queue_index: int = None
) -> typing.Union[None, bool]:
    """
    Moves a passenger at the first queue index in the index pool. The method
    is recursive, and will trigger moves for any passengers that obstruct the
    path of the passenger if possible.

    The method returns False if the queue_index position is empty after the
    move is carried out, or True if there is a passenger in that position. The
    method returns None if there was no queue index value to process.

    :param queue_index:
        The index in the queue data frame to process. If the value is None,
        a queue index will be selected from the index pool
    :param index_pool:
        A list of all queue data frame indexes that have not yet been processed
        during the current simulation iteration.
    :param settings:
        Configuration settings for the current trial
    :param queue:
        The current queue data frame on which to operate
    :param passengers:
        The passengers data frame for the trial
    """

    queue_index = extract_queue_index(index_pool, queue_index)
    if queue_index is None:
        # All queue positions have been addressed. Stepping is complete for
        # this iteration
        return None

    queue_item = queue.iloc[queue_index]
    passenger_index = queue_item['passenger']

    if passenger_index is None:
        return False

    if passengers.loc[passenger_index, 'moved']:
        # If the passenger at this queue position has already moved during this
        # iteration, then abort the update for this position
        return True

    # No matter what outcome happens after this point, the passenger will have
    # moved, even if it's just because they are stuck waiting
    passengers.loc[passenger_index, 'moved'] = True

    if passengers.loc[passenger_index, 'delay'] > 0:
        # If the passenger is in a delay state, decrement the delay and mark
        # the passenger as having moved this iteration
        passengers.loc[passenger_index, 'delay'] -= 1
        return True

    if passengers.loc[passenger_index, 'aisle'] == queue_item['aisle']:
        # If the passenger is at their aisle, handle the seating process

        if passengers.loc[passenger_index, 'delay_interchange'] > 0:
            decrement_interchange_delay(passenger_index, passengers)
            return True

        if not passengers.loc[passenger_index, 'interchanged']:
            has_delay = assign_interchange_delay(
                settings,
                passenger_index,
                passengers
            )
            if has_delay:
                return True

        # If the seating delay and interchange delay are done, remove the
        # passenger from the queue because they are now seated
        queue.loc[queue_index, 'passenger'] = None
        queue.loc[queue_index, 'seated'] = 1 + queue_item['seated']
        passengers.loc[passenger_index, 'seated'] = True
        return False

    blocked = move_down_aisle(
        queue_index=queue_index,
        passenger_index=passenger_index,
        passengers=passengers,
        settings=settings,
        index_pool=index_pool,
        queue=queue
    )

    if blocked:
        passengers.loc[passenger_index, 'count_stuck'] += 1
    return blocked


def extract_queue_index(index_pool: list, queue_index: int = None) -> int:
    """
    Extracts either the specified queue index integer from the pool and returns
    it, or extracts the first entry from the index pool and returns that if no
    queue_index value was specified. None will be returned only if no
    queue_index value was specified and the pool is empty.

    If a queue_index value is specified, it will be returned regardless of the
    state of the index_pool. This behavior allows for checking the status of
    already processed queue positions, which is necessary for the recursive
    stepping process.

    :param index_pool:
        The list of available entries in the index pool that have yet to be
        processed in a step function
    :param queue_index:
        A specific queue index to extract from the pool if it is in the pool.
    """
    if queue_index is None:
        if len(index_pool) == 0:
            return None
        return index_pool.pop()

    if queue_index in index_pool:
        index_pool.remove(queue_index)
    return queue_index


def move_down_aisle(
        queue_index: int,
        passenger_index: int,
        settings: dict,
        index_pool: list,
        passengers: pd.DataFrame,
        queue: pd.DataFrame
) -> bool:
    """
    Moves the specified passenger down the aisle if not blocked by a passenger
    located at the intended destination position.

    The method returns False if the queue_index position is empty after the
    move is carried out, or True if there is a passenger in that position.

    :param queue_index:
        The index in the queue data frame to process. If the value is None,
        a queue index will be selected from the index pool
    :param passenger_index:
        The passenger index into the passengers data frame at the current
        queue index position
    :param index_pool:
        A list of all queue data frame indexes that have not yet been processed
        during the current simulation iteration.
    :param settings:
        Configuration settings for the current trial
    :param queue:
        The current queue data frame on which to operate
    :param passengers:
        The passengers data frame for the trial
    """

    # Check to see if there is a passenger in the way at the next queue
    # position. If so, the update must abort
    dest_queue_index = queue_index + 1
    blocked = forward(
        queue_index=dest_queue_index,
        index_pool=index_pool,
        settings=settings,
        queue=queue,
        passengers=passengers
    )

    passenger = passengers.iloc[passenger_index]

    if blocked:
        # If the passenger cannot move because someone is blocking their way,
        # return True indicating that this queue position is full
        return True

    # Remove the passenger from the source position
    queue.loc[queue_index, 'passenger'] = None

    # Put the passenger at the destination location in the queue
    queue.loc[dest_queue_index, 'passenger'] = passenger_index

    dest_aisle = queue.loc[dest_queue_index, 'aisle']
    if passenger['aisle'] == dest_aisle:
        seating_delay = settings['delay']['seating']
        passengers.loc[passenger_index, 'delay'] = seating_delay

    # The passenger was moved, so there's no one in this queue position now
    return False


def assign_interchange_delay(
        settings: dict,
        passenger_index: int,
        passengers: pd.DataFrame
) -> bool:
    """
    Computes how much additional seating delay there is because there are
    seated passengers in the way

    :param settings:
        Configuration settings for the current trial
    :param passenger_index:
        The passenger entry for which to calculate the interchange delay
    :param passengers:
        The passengers data frame for the trial
    :return:
        Whether or not an interchange delay was encountered by the passenger
    """

    passengers.loc[passenger_index, 'interchanged'] = True

    delay = settings['delay']['interchange']
    if delay == 0:
        return False

    passenger = passengers.iloc[passenger_index]
    if passenger['aisle_distance'] == 0:
        return False

    seated_blockers = passengers.query(' and '.join([
        'seated',
        'aisle == {}'.format(passenger['aisle']),
        'side == "{}"'.format(passenger['side']),
        'aisle_distance < {}'.format(passenger['aisle_distance'])
    ]))

    delay *= seated_blockers.shape[0]

    if delay == 0:
        return False

    passenger_indexes = seated_blockers.index.tolist()
    passenger_indexes.append(passenger_index)
    for pi in passenger_indexes:
        passengers.loc[pi, 'delay_interchange'] = delay
        passengers.loc[pi, 'count_interchange'] += delay

    return True


def decrement_interchange_delay(
    passenger_index: int,
    passengers: pd.DataFrame
):
    """

    :param passenger_index:
    :param passengers:
    :return:
    """

    passenger = passengers.loc[passenger_index]
    seated_blockers = passengers.query(' and '.join([
        'seated',
        'aisle == {}'.format(passenger['aisle']),
        'side == "{}"'.format(passenger['side']),
        'aisle_distance < {}'.format(passenger['aisle_distance'])
    ]))

    passenger_indexes = seated_blockers.index.tolist()
    passenger_indexes.append(passenger_index)
    for pi in passenger_indexes:
        passengers.loc[pi, 'delay_interchange'] -= 1
