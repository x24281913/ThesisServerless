import sys
sys.setrecursionlimit(5000000)
import json
import staticAdd

print("Enrich Call Graph")

open('realApp/moshu.txt', 'w').close()

staticAdd.add_info(
    'realApp',
    'realApp/output.json',
    ['realApp/main.py'],
    'realApp/moshu.txt',
    'realApp/output-re.json'
)

with open('realApp/output-re.json', 'r') as f:
    cg_re = json.load(f)

print("Complete")
print("Enriched call graph entries: {}".format(len(cg_re)))
print("Saved to output-re.json")