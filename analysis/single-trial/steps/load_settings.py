import os
import json

from cauldron import project

# DATA_SLUG = ('random-1-groups', 'seat-delay-0', 'trial-0')
# DATA_SLUG = ('random-4-groups', 'seat-delay-0', 'trial-0')
DATA_SLUG = ('run_trial',)

results_directory = os.path.abspath(os.path.join('..', '..', '..', 'results'))
data_path = os.path.join(results_directory, *DATA_SLUG)

project.shared.data_path = data_path

with open(os.path.join(data_path, 'settings.json'), 'r+') as f:
    project.shared.settings = json.load(f)

with open(os.path.join(data_path, 'status.json'), 'r+') as f:
    project.shared.status = json.load(f)

