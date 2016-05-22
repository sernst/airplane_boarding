#!/usr/bin/env python3

import sys
import os
from argparse import ArgumentParser

# Add the boarding package to the python path so that it can be imported
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

import boarding

parser = ArgumentParser(
    description='Airplane boarding simulator'
)

parser.add_argument(
    'command',
    help='\n'.join([
        'The action to be taken by the boarding command.',
        'Possible choices are "run" or "populate"'
    ])
)

parser.add_argument(
    'settings_path',
    help='\n'.join([
        'The path to the simulation configuration settings JSON file',
        'that will be used to carry out the specified command.'
    ])
)

parser.add_argument(
    'output_directory',
    help='\n'.join([
        'The directory where the results of the command will be stored.'
    ])
)

args = parser.parse_args()
settings_path = args['settings_path']
output_directory = args['output_directory']
command = args['command'].lower()

if command == 'run':
    boarding.run(settings_path, output_directory)
else:
    passengers_path = os.path.join(output_directory, 'passengers.csv')
    boarding.create_passenger_data(settings_path, passengers_path)

    queue_path = os.path.join(output_directory, 'queue.csv')
    boarding.create_empty_queue_data(settings_path, queue_path)

print('Boarding command complete')
