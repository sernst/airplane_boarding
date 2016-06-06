

def seats_in_aisle(
        aisle_index: int,
        settings: dict,
        side: str = None
) -> int:
    """

    :param aisle_index:
    :param settings:
    :param side:
    :return:
    """

    aisle_offset = 0
    for section in settings.get('airplane', []):
        aisle_offset += section['rows']
        if aisle_offset <= aisle_index:
            continue

        seats = section['seats']
        if side is None:
            return sum(seats)

        side = side[0].lower()
        if side == 'l':
            return seats[0]
        elif side == 'c':
            return seats[1]
        else:
            return seats[-1]


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
