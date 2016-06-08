from boarding import paths
from boarding import results
from boarding import simulate

# trials = [
#     'i-five/i-five-b-1g',
#     'i-five/i-five-f-1g',
#     ('i-five/i-five-r-1g', '@1'),
#     ('i-five/i-five-r-1g', '@2'),
#     ('i-five/i-five-r-1g', '@3'),
#     ('i-five/i-five-r-1g', '@4'),
#     ('i-five/i-five-r-1g', '@5'),
#     ('i-five/i-five-r-1g', '@6'),
#     ('i-five/i-five-r-1g', '@7')
# ]

methods = ['r']  # ['b', 'f', 'r']
groups = [8, 10]  # , 2, 3, 4, 5, 6, 8, 10]  # 2,3,4,5,6,8,10]
collections = ['twogis']
# collections = [
#     'one', 'two', 'five', 'ten',
#     'i-one', 'i-two', 'i-five', 'i-ten'
# ]

trial_slug = '{collection}/{collection}-{method}-{group}g'
start_index = 1
end_index = 11

for c in collections:
    for g in groups:
        for method in methods:
            for index in range(start_index, end_index):
                source_name = trial_slug.format(
                    collection=c,
                    method=method,
                    group=g
                )
                trial_name = '{}-@{}'.format(source_name, index)

                print('--- TRIAL: {} ---'.format(trial_name))
                settings_path = paths.package(
                    'resources', '{}.json'.format(source_name)
                )
                results_path = paths.package('results', trial_name)
                r = simulate.run(settings_path)
                results.save(results_path, r)
