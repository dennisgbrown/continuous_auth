# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

"""
Read multiple log files and dump fitnesses to a matplotlib plot.
"""

datafiles = [
             'cfga',
             'cfgb',
             'cfgc',
             'cfgd',
             'cfge',
             'cfgf'
             ]

actor = 'Attacker'

plotfile = actor + ' Population Averages'

best_x_values = [[] for _ in range(len(datafiles))]
best_y_values = [[] for _ in range(len(datafiles))]

for curr_file in range(len(datafiles)):
    x_values = []
    y_values = []

    filename = '../logs/' + datafiles[curr_file] + '.txt'

    curr_run = 0

    # Read the data from the file and identify the best run
    with open(filename, 'r') as reader:
        passed_config_info = False
        # read numbers
        for curr_line in reader:
            curr_line = curr_line.strip()
            #print(curr_line)

            # Skip blank lines
            if (curr_line):
                # If we've started a run, reset the current values
                # and note that we've passed the config info so everything
                # past here should be eval numbers or "Run x"
                if (curr_line.startswith('Run')):
                    curr_run += 1
                    x_values.append([])
                    y_values.append([])
                    passed_config_info = True

                # If the log file is properly formed we can assume this
                # line contains two tab-separated numbers.
                elif (passed_config_info):
                    coord_list = list(curr_line.split('\t'))
                    if (coord_list[0] != actor): continue
                    x = float(coord_list[1])
                    y = float(coord_list[3])
                    x_values[curr_run - 1].append(x)
                    y_values[curr_run - 1].append(y)


    avg_y_values = []
    num_runs = curr_run
    for y in range(len(y_values[0])):
        total = 0
        for r in range(num_runs):
            total += y_values[r][y]
        avg_y_values.append(total / num_runs)

    plt.plot(x_values[0], avg_y_values, label = datafiles[curr_file])

plt.title(plotfile + ' Average over 30 Runs')
plt.xlabel('Evaluations')
plt.ylabel('Fitness')
# plt.xlim(left = 0)
# plt.ylim(bottom = 0)
plt.grid(True)
plt.legend(loc='lower right')
plt.savefig('../plots/' + plotfile + '.png', dpi = 600)

