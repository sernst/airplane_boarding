
Airplane Boarding Simulator
===========================

A python package for simulating the passenger boarding process of an airplane.

To run a simulation, use the command:

    ./bin/boarding run [SETTINGS_FILE_PATH] [RESULTS_DIRECTORY_PATH]

Results
-------
   
The results of each simulation will be saved in the specified results directory 
and include:

* __passengers.csv__: The DataFrame containing the passenger manifest for the flight.
* __queue.csv__: The final state of the boarding queue when the simulation ended.
* __progress.csv__: A DataFrame that contains a snapshot of the state and position for each passenger during the boarding process.
* __seated.csv__: Information on the time it took each passenger to find their seat.
* __status.json__: Metadata for the simulation including the total elapsed time.
* __settings.json__: A copy of the original settings file that was loaded for the simulation, which was populated with the default values for any data omitted in the original file.
    
Settings File
-------------

A simulation trial requires a settings file populated with the configuration
data for that trial. The expected format is JSON. A number of example trials 
have been included in _resources_ folder of this repository.
