import sys
sys.setrecursionlimit(5000000)
import dynamicprocess

print("Find Indispensable Functions")

dynamicprocess.getDynamicContent_new(
    ['main.lambda_handler', 'main'],
    'realApp',
    'realApp/output-re.json',
    ['realApp/main.py'],
    'used_func_result/used_func_reqs.txt'
)

with open('used_func_result/used_func_reqs.txt', 'r') as f:
    used = [l.strip() for l in f if l.strip()]

print("Complete")
print("Used functions found: {}".format(len(used)))
