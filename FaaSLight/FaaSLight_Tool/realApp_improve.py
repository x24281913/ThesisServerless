import sys
sys.setrecursionlimit(5000000)
import os
import json
import time
import shutil

print("Improvement")

# Create fresh copy for improved version
if os.path.exists('realApp_improved'):
    shutil.rmtree('realApp_improved')
shutil.copytree('realApp', 'realApp_improved')
print("Created fresh copy: realApp_improved/")

# Run your improved Auto_delete_v6.py
print("\nRunning your improved Auto_delete_v6.py...")
result = os.system(
    'python3 Auto_delete_v6.py '
    '--dirname realApp_improved '
    '--path realApp_improved '
    '--usedfuntionlist used_func_result/used_func_reqs_final.txt '
    '--unused_gzip_dir realApp_improved/gzipinfo.txt '
    '--builtlist built_list.txt'
)

print("\nVerifying output")

# Confirm gzipinfo.txt was NOT created
if os.path.exists('realApp_improved/gzipinfo.txt'):
    print("WARNING: gzipinfo.txt was created")
else:
    print("gzipinfo.txt was NOT created")

# Check group files were created
group_files = sorted([
    f for f in os.listdir('realApp_improved')
    if f.startswith('hybrid_')
    and f.endswith('.json')
    and f != 'hybrid_group_index.json'
])

print("Group JSON files created: {}".format(
    len(group_files)))

total = 0
for gf in group_files:
    with open('realApp_improved/{}'.format(gf), 'r') as f:
        data = json.load(f)
    total += len(data)
    print("  {} - {} functions".format(gf, len(data)))

print("Total optional functions grouped: {}".format(total))

# Check group_index.json
if os.path.exists('realApp_improved/hybrid_group_index.json'):
    with open('realApp_improved/hybrid_group_index.json', 'r') as f:
        index = json.load(f)
    print("hybrid_group_index.json - {} entries".format(len(index)))

# Measure your improvement loading time
print("improved loading time")
times = []
for i in range(10):
    start = time.time()
    with open('realApp_improved/{}'.format(group_files[0]), 'r') as f:
        json.load(f)
    elapsed = (time.time() - start) * 1000
    times.append(elapsed)
    print("  Run {}: {:.4f} ms".format(i+1, elapsed))

avg = round(sum(times) / len(times), 4)


print("  Average loading time: {} ms".format(avg))

# Save improvement result for comparison
with open('improvement_result.txt', 'w') as f:
    f.write("improved_avg_ms={}".format(avg))
print("Improvement result saved to improvement_result.txt")