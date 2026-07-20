import sys
sys.setrecursionlimit(5000000)
import os
import json
import gzip
import time
import shutil

print("Original FaaSLight test")

# Create fresh copy for original FaaSLight
if os.path.exists('realApp_original'):
    shutil.rmtree('realApp_original')
shutil.copytree('realApp', 'realApp_original')
print("Created fresh copy: realApp_original/")

# Run original Auto_delete_v6_ORIGINAL.py
print("\nRunning original Auto_delete_v6_ORIGINAL.py...")
result = os.system(
    'python3 Auto_delete_v6_ORIGINAL.py '
    '--dirname realApp_original '
    '--path realApp_original '
    '--usedfuntionlist used_func_result/used_func_reqs_final.txt '
    '--unused_gzip_dir realApp_original/gzipinfo.txt '
    '--builtlist built_list.txt'
)

print("\nVerifying original FaaSLight output...")

# Check gzipinfo.txt was created
if os.path.exists('realApp_original/gzipinfo.txt'):
    size = os.path.getsize('realApp_original/gzipinfo.txt')
    print("gzipinfo.txt created: {} bytes".format(size))

    with gzip.open('realApp_original/gzipinfo.txt', 'r') as f:
        data = json.loads(f.read().decode('utf-8'))
    print("Optional functions inside: {}".format(len(data)))
else:
    print("ERROR: gzipinfo.txt was not created")

# baseline load time
print("baseline load time")
print("Loading ALL optional functions from gzipinfo.txt:")
times = []
for i in range(10):
    start = time.time()
    with gzip.open(
        'realApp_original/gzipinfo.txt', 'r'
    ) as f:
        json.loads(f.read().decode('utf-8'))
    elapsed = (time.time() - start) * 1000
    times.append(elapsed)
    print("  Run {}: {:.4f} ms".format(i+1, elapsed))

avg = round(sum(times) / len(times), 4)

print("Original FaaSLight:")
print("  Average loading time: {} ms".format(avg))

# Save baseline result for comparison
with open('baseline_result.txt', 'w') as f:
    f.write("original_avg_ms={}".format(avg))
print("Baseline result saved to baseline_result.txt")
