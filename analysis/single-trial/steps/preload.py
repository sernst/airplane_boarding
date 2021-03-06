import cauldron as cd

# === 1. IDEAL BACK->FRONT === #
DATA_SLUG = ('ideal', 'ideal-b-1g')

# === 2. IDEAL FRONT->BACK === #
# DATA_SLUG = ('ideal', 'ideal-f-1g')

# === 3. IDEAL RANDOM === #
# DATA_SLUG = ('ideal', 'ideal-r-1g-@1')

# === 4. DELAY 2 RANDOM === #
# DATA_SLUG = ('two', 'two-r-1g-@1')

# === 5. SWAPPING 2 RANDOM === #
# DATA_SLUG = ('i_two', 'i_two-r-1g-@1')

# === 6. DELAY + SWAPPING 2 RANDOM === #
# DATA_SLUG = ('is_two', 'is_two-r-1g-@1')

# DATA_SLUG = ('i_ten', 'i_ten-r-1g-@11')
# DATA_SLUG = ('i_ten', 'i_ten-r-1g-@15')

# === BAD & GOOD FULL === #
# DATA_SLUG = ('twogis', 'twogis-r-1g-@2')
# DATA_SLUG = ('twogis', 'twogis-r-1g-@9')

cd.shared.slug = DATA_SLUG
cd.project.title = 'Trial: {}/{}'.format(*DATA_SLUG)
