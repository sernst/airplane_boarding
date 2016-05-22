import json
import numpy as np
from cauldron import plotting
from cauldron import project

df = project.shared.data


def plot_groupings(boarding_method, title):
    group_counts = [1, 2, 3, 4, 5, 6, 8, 10]
    elapsed = []
    elapsed_uncertainties = []

    for gc in group_counts:
        df_slice = df[
            (df['boarding_method'] == boarding_method) &
            (df['group_count'] == gc)
        ]
        elapsed.append(
            np.median(df_slice['elapsed'])
        )
        elapsed_uncertainties.append(
            np.median(np.abs(
                df_slice['elapsed'] - elapsed[-1]
            ))
        )

    if boarding_method == 'r':
        c = 'rgba(150, 150, 150, 0.8)'
        fc = 'rgba(150, 150, 150, 0.2)'
    elif boarding_method == 'b':
        c = plotting.get_color(0, 0.8)
        fc = plotting.get_color(0, 0.2)
    else:
        c = plotting.get_color(1, 0.8)
        fc = plotting.get_color(1, 0.2)

    definition = dict(
        x=group_counts,
        y=elapsed,
        y_unc=elapsed_uncertainties,
        name=boarding_method.upper(),
        color=c,
        fill_color=fc
    )

    plot = plotting.make_line_data(**definition)

    project.display.plotly(
        data=plot['data'],
        layout=plotting.create_layout(
            plot['layout'],
            title=title,
            x_label='Group Count (#)',
            y_label='Boarding Time (s)',
        ),
        scale=0.75
    )
    return plot['data']

traces = (
    plot_groupings('b', 'Backward Boarding in Row Groups') +
    plot_groupings('f', 'Forward Boarding in Row Groups') +
    plot_groupings('r', 'Random Boarding in Row Groups')
)

project.display.plotly(
    data=traces,
    layout=plotting.create_layout(
        title='Comparison Boarding in Row Groups',
        x_label='Group Count (#)',
        y_label='Boarding Time (s)',
    ),
    scale=0.75
)


