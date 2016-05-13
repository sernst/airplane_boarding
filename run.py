import json

from boarding import paths
from boarding import results
from boarding import simulate


def run_trial(settings, results_directory):
    """

    :param settings:
    :param results_directory:
    :return:
    """

    r = simulate.run(settings)
    results.save(results_directory, r)


def run():
    """

    :return:
    """

    settings_path = paths.package('resources', 'trial.json')

    with open(settings_path, 'r+') as f:
        source_settings = json.load(f)

    for populate_type in ['RANDOM']:
        print('POPULATION TYPE:', populate_type)
        for group_count in [2, 3, 4, 6, 8, 10]:
            print('GROUP COUNT:', group_count)
            for seating_delay in [0, 4, 8, 12, 16, 20]:
                print('SEATING DELAY: {}s'.format(seating_delay))

                for i in range(50):
                    settings = json.loads(json.dumps(source_settings))
                    settings['uid'] = 'T{}-SD{}'.format(i, seating_delay)
                    settings['delay']['seating'] = seating_delay
                    settings['populate'] = {
                        'type': populate_type,
                        'groups': group_count
                    }

                    results_directory = paths.package(
                        'results',
                        '{}-{}-groups'.format(
                            populate_type.lower(),
                            group_count
                        ),
                        'seat-delay-{}'.format(seating_delay),
                        'trial-{}'.format(i)
                    )

                    print('[{} @{}s]: STARTED'.format(i, seating_delay))
                    run_trial(settings, results_directory)
                    print('[{} @{}s]: COMPLETED'.format(i, seating_delay))

if __name__ == '__main__':
    run()
