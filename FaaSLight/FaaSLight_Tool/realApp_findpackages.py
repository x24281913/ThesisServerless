import sys
sys.setrecursionlimit(5000000)
import isContainPackage

print("Find Used Packages")

isContainPackage.getPackgaeName(
    'used_func_result/used_func_reqs.txt',
    'realApp',
    'used_func_result/used_package_reqs.txt'
)

with open('used_func_result/used_package_reqs.txt', 'r') as f:
    pkgs = [l.strip() for l in f if l.strip()]

print("Complete")
print("Used packages found: {}".format(len(pkgs)))
