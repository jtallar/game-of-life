import sys

import objects as obj
import analyzer
import utils

if len(sys.argv) <= 1:
    plot_boolean = False
else:
    plot_boolean = (sys.argv[1] == 'plot')

print(analyzer.analyze_input(sys.stdin, plot_boolean))