import sys
sys.setrecursionlimit(5000000)
import os
import json

print("Build Call Graph Using PyCG")

os.system(
    'python3 pycg/__main__.py '
    '--package realApp realApp/main.py '
    '-o realApp/output.json'
)

with open('realApp/output.json', 'r') as f:
    cg = json.load(f)

print("Complete")
print("Call graph entries: {}".format(len(cg)))
print("Saved to realApp/output.json")
