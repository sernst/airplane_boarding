
def aisle_count(settings: dict) -> int:
    """

    :param settings:
    :return:
    """

    return sum([x['rows'] for x in settings.get('airplane', [])])


def seat_count(settings: dict) -> int:
    """

    :param settings:
    :return:
    """

    seats = 0
    for s in settings.get('airplane', []):
        seats += sum([x * s['rows'] for x in s['seats']])
    return seats
