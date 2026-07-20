import sys
sys.setrecursionlimit(5000000)
import dynamicprocess

print("Final Functions List")

dynamicprocess.result_process(
    'realApp',
    'used_func_result/used_func_reqs_update.txt',
    'used_func_result/used_func_reqs_final.txt',
    []
)

dynamicprocess.result_addlibray(
    'used_func_result/used_func_reqs_final.txt',
    'used_func_result/used_package_reqs.txt',
    'import-prefunc',
    'used_func_result/used_func_reqs_final_re.txt'
)

with open('used_func_result/used_func_reqs_final.txt',
          'r') as f:
    final = [l.strip() for l in f if l.strip()]


print("Complete")
print("Final functions: {}".format(len(final)))
