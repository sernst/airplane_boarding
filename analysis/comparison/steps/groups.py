import cauldron as cd
from cauldron import plotting

df = cd.shared.data
plot_collection = cd.shared.plot_collection

df = df[df.collection == 'twogis'].copy()

labels = []
for index, row in df.iterrows():
    labels.append('{}G {}'.format(row.group_count, row.trial_label))
df['trial_label'] = labels

plot_collection(
    df[df.collection == 'twogis'],
    title='Seating &amp; Interchange Delay Trials',
    color_column='group_count',
    color_values={
        1: plotting.get_color(0),
        2: plotting.get_color(1),
        3: plotting.get_color(2),
        4: plotting.get_color(3),
        5: plotting.get_color(4),
        6: plotting.get_color(5),
        8: plotting.get_color(6),
        10: plotting.get_color(7),
        'default': plotting.get_color(8)
    }
)
