import sys
sys.setrecursionlimit(5000000)
import os
import dynamicprocess

moshu_file_update = 'moshu_functions/reqs_update.txt'
moshu_file_final = 'moshu_functions/reqs_final.txt'

os.system(
    'python3 find_moshu.py '
    '--dirname realApp '
    '--path realApp '
    '--packageset used_func_result/used_package_reqs.txt '
    '--moshuoutput {}'.format(moshu_file_update)
)

dynamicprocess.moshu_update(
    moshu_file_update, [], moshu_file_final)

dynamicprocess.getDynamicContent(
    ['main.lambda_handler', 'main'],
    'realApp',
    'realApp/output-re.json',
    ['realApp/main.py'],
    moshu_file_final,
    'used_func_result/used_func_reqs_update.txt'
)

with open('used_func_result/used_func_reqs_update.txt',
          'r') as f:
    updated = [l.strip() for l in f if l.strip()]

print("Complete")