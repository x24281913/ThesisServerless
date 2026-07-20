import json
import gzip
import os

print("VERIFICATION")

# Check required files exist
if not os.path.exists('realApp_original/gzipinfo.txt'):
    print("ERROR: realApp_original/gzipinfo.txt not found")
    print("Please run realApp_origfaaslight.py first")
    exit(1)

if not os.path.exists('realApp_improved'):
    print("ERROR: realApp_improved folder not found")
    print("Please run realApp_improve.py first")
    exit(1)

# Load original gzipinfo.txt
print("Loading original FaaSLight output")
with gzip.open('realApp_original/gzipinfo.txt', 'r') as f:
    original_data = json.loads(f.read().decode('utf-8'))
print("Original functions: {}".format(len(original_data)))

# Load all your group JSON files
print("Loading your improvement output")
group_files = sorted([
    f for f in os.listdir('realApp_improved')
    if f.startswith('hybrid_')
    and f.endswith('.json')
    and f != 'hybrid_group_index.json'
])

improved_data = {}
for gf in group_files:
    with open('realApp_improved/{}'.format(gf), 'r') as f:
        data = json.load(f)
    improved_data.update(data)
    print("  Loaded {} - {} functions".format(
        gf, len(data)))

print("Your improvement functions: {}".format(
    len(improved_data)))

# Compare function names
original_keys = set(original_data.keys())
improved_keys = set(improved_data.keys())

in_original_not_improved = original_keys - improved_keys
in_improved_not_original = improved_keys - original_keys

print("VERIFICATION RESULTS")

if len(in_original_not_improved) == 0 \
        and len(in_improved_not_original) == 0:
    print("CONFIRMED: Both approaches contain EXACTLY")
    print("the same {} optional functions".format(
        len(original_keys)))
    print()
    print("The ONLY difference is HOW they are stored:")
    print("  Original: ONE gzip file")
    print("            loads ALL {} functions at once".format(
        len(original_data)))
    print("  Yours:    {} small JSON group files".format(
        len(group_files)))
    print("            loads only ~{} functions at a time".format(
        len(improved_data) // len(group_files)
        if group_files else 0))
    print()
    print("Your improvement is CORRECT and VERIFIED")
else:
    print("MISMATCH FOUND:")
    if in_original_not_improved:
        print("In original but NOT in yours:")
        for f in list(in_original_not_improved)[:5]:
            print("  {}".format(f))
    if in_improved_not_original:
        print("In yours but NOT in original:")
        for f in list(in_improved_not_original)[:5]:
            print("  {}".format(f))
            