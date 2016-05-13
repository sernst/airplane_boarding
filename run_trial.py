from boarding import paths
from boarding import results
from boarding import simulate

trials = [
    'trial-b1-s16-i8',
    'trial-f1-s16-i8',
    'trial-r1-s16-i8'
]

for t in trials:
    settings_path = paths.package('resources', '{}.json'.format(t))
    results_path = paths.package('results', t)
    r = simulate.run(settings_path)
    results.save(results_path, r)
