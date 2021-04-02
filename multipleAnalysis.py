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
init_percentage = int(directory.split('/')[-1])
obs_dict = {}
obs_dict[init_percentage] = []
for filename in entries:
    with open(directory + '/' + filename) as file:
        obs_dict[init_percentage].append(analyzer.analyze_input(file, False))

print(obj.Summary(obs_dict[init_percentage], init_percentage))
