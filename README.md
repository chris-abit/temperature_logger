Code for an Arduino board with two temperature sensors.
Logging is performed using temp_log.py data is automatically
stored to a csv format in csv/. The files are created with
the timestamp of the day created. By default every
100 readings are written to disk.
* python temp_log.py


Data can be plotted using plot_temps.py. Where plot_temps
requires either a file or all flag:
* python plot_temps.py --all
* python plot_temps.py --file {filename}

A demo plot
* python plot_temps.py --file csv/demo.csv
