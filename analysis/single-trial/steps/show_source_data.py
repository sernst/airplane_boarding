import cauldron as cd

# cd.display.workspace(values=False)

cd.display.header('Passengers', level=2)
cd.display.table(
    cd.shared.passengers[[
        'aisle',
        'letter',
        'side',
        'window_distance',
        'aisle_distance'
    ]],
    scale=0.4
)

cd.display.header('Starting Queue', level=2)
cd.display.table(
    cd.shared.starting_queue[[
        'aisle',
        'passenger'
    ]],
    scale=0.4
)
