import math
import random
import typing

import pandas as pd


def chunks(
        settings: dict,
        passengers: pd.DataFrame,
        queue: pd.DataFrame
) -> typing.List[typing.Tuple[int]]:
    """
    Creates a list of start and end aisle pairings for the population groups as
    specified in the configuration settings

    :param settings:
    :param passengers:
    :param queue:
    :return:
    """
    group_count = settings['populate']['groups']
    aisle_count = queue['aisle'].max() + 1

    out = []

    if group_count < 2:
        out.append((0, passengers.shape[0]))
        return out

    for index in range(group_count):
        delta = math.floor(aisle_count / group_count)
        start_aisle = index * delta
        end_aisle = max(
            start_aisle + 1,
            (index + 1) * delta
        )
        if index == (group_count - 1):
            end_aisle = aisle_count
        out.append((start_aisle, end_aisle))

    return out


def order_by(
        groups: typing.List,
        order_type: str,
        default_type: str = None
) -> typing.List:
    """
    Orders a list of groups by the specified order type, or the default type if
    the order type is 'DEFAULT' or unrecognized

    :param groups:
        A list of aisle or passenger index groups to sort by the specified
        order
    :param order_type:
        The enumerated order type, such as 'RANDOM', 'FORWARD', or 'BACKWARD'
    :param default_type:
        A default order type to use if the order_type is 'DEFAULT' or the
        order type is not recognized
    :return:
        The list of groups that has been sorted
    """

    order_type = order_type.upper()

    if order_type == 'BACKWARD':
        groups.reverse()
        return groups

    if order_type == 'FORWARD':
        return groups

    if order_type == 'RANDOM':
        random.shuffle(groups)
        return groups

    if default_type:
        return order_by(groups, default_type)

    raise ValueError(
        'Invalid configuration setting populate.group_order of "{}"'.format(
            order_type
        )
    )


def to_passenger_indexes(
        aisle_groups: typing.List[typing.Tuple[int]],
        passengers: pd.DataFrame
) -> typing.List[typing.List[int]]:
    """
    Converts a list of aisle groups into a list of passenger index groups

    :param aisle_groups:
        A list of aisle start and aisle end indexes to be converted into
        passenger indexes
    :param passengers:
        The passenger manifest data frame
    :return:
        A list of groups where each group contains a list of the passenger
        indexes in that group
    """

    out = []
    for group in aisle_groups:
        query = 'aisle >= {} and aisle < {}'.format(*group)
        out.append(list(passengers.query(query).index))
    return out
