import sys
import os
import analyzer
import objects as obj

if len(sys.argv) <= 1:
    print("Must run with python multipleAnalysis.py directory")
    sys.exit(1)

if sys.argv[1][-1] == '/':
    directory = sys.argv[1][:-1:]
else:
    directory = sys.argv[1]

entries = os.listdir(directory)
obs_list = []
for filename in entries:
    with open(directory + '/' + filename) as file:
        obs_list.append(analyzer.analyze_input(file, False))

print(obj.Summary(obs_list))
