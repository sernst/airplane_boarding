from cauldron import project

df = project.shared.data
plot_collection = project.shared.plot_collection
plot_comparison = project.shared.plot_comparison

plot_collection(
    df[
        (df['seating_delay'] == 0) &
        (df['interchange_delay'] == 1)
        ],
    '1s Interchange Delay'
)

plot_collection(
    df[
        (df['seating_delay'] == 0) &
        (df['interchange_delay'] == 10)
        ],
    '10s Interchange Delay'
)

plot_comparison(
    df[
        (df['seating_delay'] == 0) &
        (df['group_count'] == 1)
        ],
    title='Interchange Delay Trials',
    comparison_column='interchange_delay',
    comparison_label='Interchange Delay (s)'
)
