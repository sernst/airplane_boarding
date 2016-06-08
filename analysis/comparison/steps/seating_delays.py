import numpy as np
from cauldron import project
from cauldron import plotting
import plotly.graph_objs as go

df = project.shared.data


def plot_collection(
        data_frame,
        title,
        color_column='boarding_method',
        color_values=None
):
    data_frame = data_frame.sort_values(by='trial_label')

    times = data_frame['elapsed']
    labels = data_frame['trial_label']
    colors = []

    if color_values is None:
        color_values = dict(
            r='rgba(204, 204, 204, 0.8)',
            b=plotting.get_color(0, 0.8),
            default=plotting.get_color(1, 0.8)
        )

    for index, row in data_frame.iterrows():
        method = row[color_column]
        colors.append(
            color_values.get(method, color_values.get('default'))
        )

    project.display.plotly(
        data=go.Bar(
            y=times,
            x=labels,
            marker=dict(color=colors),
        ),
        layout=plotting.create_layout(
            title=title,
            y_label='Boarding Time (s)',
            x_label='Trial',
            y_bounds=[times.min() - 10, times.max() + 10]
        ),
        scale=0.75
    )
project.shared.plot_collection = plot_collection


def plot_comparison(data_frame, title, comparison_column, comparison_label):
    data_frame = data_frame.sort_values(by='trial_label')

    traces = []
    for method in data_frame['boarding_method'].unique():
        df_method = data_frame[data_frame['boarding_method'] == method]

        delays = []
        times = []

        for delay in sorted(df_method[comparison_column].unique()):
            x = df_method[df_method[comparison_column] == delay]
            times.append(np.median(x['elapsed']))
            delays.append(delay)

        if method == 'r':
            c = 'rgba(204, 204, 204, 0.8)'
        elif method == 'b':
            c = plotting.get_color(0, 0.8)
        else:
            c = plotting.get_color(1, 0.8)

        traces.append(go.Scatter(
            x=times,
            y=delays,
            name=method,
            mode='lines+markers',
            marker=dict(
                color=c
            )
        ))

    project.display.plotly(
        data=traces,
        layout=plotting.create_layout(
            title=title,
            x_label='Boarding Time (s)',
            y_label=comparison_label
        ),
        scale=0.75
    )
project.shared.plot_comparison = plot_comparison

plot_collection(
    df[
        (df['seating_delay'] == 0) &
        (df['interchange_delay'] == 0)
    ],
    'Ideal Trials'
)

plot_collection(
    df[
        (df['seating_delay'] == 1) &
        (df['interchange_delay'] == 0)
    ],
    '1s Seating Delay'
)

plot_collection(
    df[
        (df['seating_delay'] == 10) &
        (df['interchange_delay'] == 0)
    ],
    '10s Seating Delay'
)

plot_comparison(
    df[
        (df['interchange_delay'] == 0) &
        (df['group_count'] == 1)
    ],
    title='Seating Delay Trials',
    comparison_column='seating_delay',
    comparison_label='Seating Delay (s)'
)
