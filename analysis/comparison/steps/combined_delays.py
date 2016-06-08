import cauldron as cd

df = cd.shared.data
plot_collection = cd.shared.plot_collection
plot_comparison = cd.shared.plot_comparison

plot_collection(
    df[
        (df['seating_delay'] == 2) &
        (df['interchange_delay'] == 2) &
        (df['group_count'] == 1)
        ],
    '2s Seating &amp; Interchange Delay'
)
