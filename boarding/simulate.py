import typing

from boarding import configuration
from boarding.ops import passengers as passenger_ops
from boarding.ops import queue as queue_ops
from boarding import results
from boarding import validate


def run(settings: typing.Union[str, dict]) -> dict:
    """
    Runs the simulation specified by the settings argument and returns a
    dictionary containing the trial results

    :param settings:
        The configuration for the trial simulation to be forward or a path
        to the file where the settings can be loaded
    """

    settings = configuration.load(settings)
    passengers = passenger_ops.create(settings)
    queue = queue_ops.populate(
        settings,
        queue_ops.create(settings, passengers),
        passengers
    )

    # Create results and update them with the time = 0 starting values
    result = results.create(settings, queue, passengers)
    results.update(result)

    previous_status = None

    while queue_ops.size(settings, queue) > 0:
        # Main simulation loop, which iterates until the passenger queue is
        # empty because all passengers have been seated

        passenger_ops.move(
            settings=settings,
            passengers=passengers,
            queue=queue
        )

        if settings.get('validate'):
            # If validation is active for this trial, confirm that the current
            # state of the simulation meets the validation criteria
            validate.seating(settings, queue, passengers)

        results.update(result)
        previous_status = print_status(previous_status, result['status'])

    print_status(previous_status, result['status'], force=True)

    return result


def print_status(
        previous_status: dict,
        new_status: dict,
        force: bool = False
) -> dict:
    """
    Prints to the console the time and boarding status at regular intervals of
    10% by comparing the previous_status and new_status to determine if a
    status update is necessary.

    :param previous_status:
        The last status that was printed to the console, which is used to
        determine if a status update should be printed or not by comparing
        this status to the new_status. If previous_status is None, the new
        status will be returned but nothing will be printed.
    :param new_status:
        The new status to compare against the previous one. If the new status
        progress differs by less than 10% then no console update is printed.
    :param force:
        Forces an update unless the previous and new status arguments are the
        same.
    """

    if not previous_status:
        return new_status

    if force:
        do_update = (new_status != previous_status)
    else:
        do_update = (
            (new_status['progress'] - previous_status['progress']) >= 0.1 or
            (new_status['elapsed'] - previous_status['elapsed']) > 30
        )

    if not do_update:
        return previous_status

    progress = '{}%'.format(int(100.0 * new_status['progress']))
    print(new_status['time'], progress)
    return new_status
