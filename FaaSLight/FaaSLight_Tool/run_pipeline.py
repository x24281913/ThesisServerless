"""
run_pipeline.py
Student: Amruta Anil Dicholkar | X24281913
MSc Cloud Computing - NCI
Foundation Paper: FaaSLight (Liu et al., 2023)

Generic pipeline script - works on any application.

Usage:
  python3 run_pipeline.py realApp
  python3 run_pipeline.py app_lxml
  python3 run_pipeline.py app_pdf
  python3 run_pipeline.py app_pandas
"""

import os
import sys
import json
import gzip
import time
import shutil

sys.setrecursionlimit(5000000)

# ── Get app folder from command line ──────────────────
if len(sys.argv) < 2:
    print("Usage: python3 run_pipeline.py <app_folder>")
    print("Example: python3 run_pipeline.py realApp")
    sys.exit(1)

app_folder = sys.argv[1]

# ── Check app folder exists ────────────────────────────
if not os.path.exists(app_folder):
    print("ERROR: Folder {} not found".format(app_folder))
    sys.exit(1)

# ── Find entry point ───────────────────────────────────
entry_file = '{}/main.py'.format(app_folder)
if not os.path.exists(entry_file):
    print("ERROR: {}/main.py not found".format(app_folder))
    sys.exit(1)

# ── Find seed functions from serverless.yml ────────────
import utiltool
seedfun_list = []
yml_file = '{}/serverless.yml'.format(app_folder)
if os.path.exists(yml_file):
    seedfun_list = utiltool.foryml(yml_file)
if not seedfun_list:
    seedfun_list = [
        'main.lambda_handler',
        'main.handler',
        'main'
    ]

app_name = app_folder.replace('/', '_')

print("="*60)
print("FaaSLight Hybrid Pipeline")
print("Application: {}".format(app_folder))
print("Entry: {}".format(entry_file))
print("Seed functions: {}".format(seedfun_list))
print("="*60)

# ── STEP 1 — Remove junk files ─────────────────────────
print("\nStep 1 - Removing junk files...")
import removefile
assetsDir = {
    'ignorDir': [
        '__pycache__', 'tests', '.serverless',
        'pip', 'pkg_resources', 'setuptools', 'wheel'
    ],
    'ignorSpeDir': ['.dist-info'],
    'ignorFile': ['.pyc', '.pyi', '.pth', '.md'],
}
removefile.delFiles(app_folder, assetsDir)
print("Step 1 done")

# ── STEP 2 — Build call graph ──────────────────────────
print("\nStep 2 - Building call graph...")
output_json = '{}/output.json'.format(app_folder)
os.system(
    'python3 pycg/__main__.py '
    '--package {} {} -o {}'.format(
        app_folder, entry_file, output_json))
with open(output_json, 'r') as f:
    cg = json.load(f)
print("Call graph entries: {}".format(len(cg)))

# ── STEP 3 — Enrich call graph ─────────────────────────
print("\nStep 3 - Enriching call graph...")
import staticAdd
moshu_file = '{}/moshu.txt'.format(app_folder)
re_fun_rel = '{}/output-re.json'.format(app_folder)
open(moshu_file, 'w').close()
staticAdd.add_info(
    app_folder, output_json,
    [entry_file], moshu_file, re_fun_rel)
with open(re_fun_rel, 'r') as f:
    cg_re = json.load(f)
print("Enriched entries: {}".format(len(cg_re)))

# ── STEP 4 — Find used functions ───────────────────────
print("\nStep 4 - Finding used functions...")
import dynamicprocess
used_output = 'used_func_result/used_func_{}.txt'.format(
    app_name)
dynamicprocess.getDynamicContent_new(
    seedfun_list, app_folder, re_fun_rel,
    [entry_file], used_output)
with open(used_output, 'r') as f:
    used = [l.strip() for l in f if l.strip()]
print("Indispensable functions: {}".format(len(used)))

# ── STEP 5 — Find packages ─────────────────────────────
print("\nStep 5 - Finding packages...")
import isContainPackage
pkg_output = 'used_func_result/used_package_{}.txt'.format(
    app_name)
isContainPackage.getPackgaeName(
    used_output, app_folder, pkg_output)
print("Step 5 done")

# ── STEP 6 — Magic functions ───────────────────────────
print("\nStep 6 - Magic functions...")
moshu_update = 'moshu_functions/{}_update.txt'.format(
    app_name)
moshu_final = 'moshu_functions/{}_final.txt'.format(
    app_name)
os.system(
    'python3 find_moshu.py '
    '--dirname {} --path {} '
    '--packageset {} --moshuoutput {}'.format(
        app_folder, app_folder,
        pkg_output, moshu_update))
dynamicprocess.moshu_update(
    moshu_update, [], moshu_final)
used_update = 'used_func_result/used_func_{}_update.txt'.format(
    app_name)
dynamicprocess.getDynamicContent(
    seedfun_list, app_folder, re_fun_rel,
    [entry_file], moshu_final, used_update)
print("Step 6 done")

# ── STEP 7 — Final functions list ──────────────────────
print("\nStep 7 - Final functions list...")
used_final = 'used_func_result/used_func_{}_final.txt'.format(
    app_name)
used_final_re = 'used_func_result/used_func_{}_final_re.txt'.format(
    app_name)
dynamicprocess.result_process(
    app_folder, used_update, used_final, [])
dynamicprocess.result_addlibray(
    used_final, pkg_output,
    'import-prefunc', used_final_re)
with open(used_final, 'r') as f:
    final = [l.strip() for l in f if l.strip()]
print("Final indispensable: {}".format(len(final)))

# ── STEP 8a — Original FaaSLight baseline ──────────────
print("\nStep 8a - Original FaaSLight baseline...")
orig_folder = '{}_original'.format(app_folder)
if os.path.exists(orig_folder):
    shutil.rmtree(orig_folder)
shutil.copytree(app_folder, orig_folder)

orig_gzip = '{}/gzipinfo.txt'.format(orig_folder)
os.system(
    'python3 Auto_delete_v6_ORIGINAL.py '
    '--dirname {} --path {} '
    '--usedfuntionlist {} '
    '--unused_gzip_dir {} '
    '--builtlist built_list.txt'.format(
        orig_folder, orig_folder,
        used_final, orig_gzip))

# Measure original loading time
orig_time = 0
orig_funcs = 0
if os.path.exists(orig_gzip):
    with gzip.open(orig_gzip, 'r') as f:
        orig_data = json.loads(
            f.read().decode('utf-8'))
    orig_funcs = len(orig_data)
    times = []
    for i in range(10):
        start = time.time()
        with gzip.open(orig_gzip, 'r') as f:
            json.loads(f.read().decode('utf-8'))
        times.append((time.time() - start) * 1000)
    orig_time = round(sum(times) / len(times), 4)
    print("Optional functions: {}".format(orig_funcs))
    print("Original loading time: {} ms".format(orig_time))

# ── STEP 8b — Hybrid improvement ───────────────────────
print("\nStep 8b - Hybrid improvement...")
imp_folder = '{}_improved'.format(app_folder)
if os.path.exists(imp_folder):
    shutil.rmtree(imp_folder)
shutil.copytree(app_folder, imp_folder)

# gzipinfo.txt is NEVER created in hybrid improvement
# hybrid_assoc_*.json and hybrid_freq_*.json are created
imp_gzip = '{}/gzipinfo.txt'.format(imp_folder)
os.system(
    'python3 Auto_delete_v6.py '
    '--dirname {} --path {} '
    '--usedfuntionlist {} '
    '--unused_gzip_dir {} '
    '--builtlist built_list.txt'.format(
        imp_folder, imp_folder,
        used_final, imp_gzip))

# Find hybrid group files
hybrid_files = sorted([
    f for f in os.listdir(imp_folder)
    if f.startswith('hybrid_')
    and f.endswith('.json')
    and 'index' not in f
])

# Measure hybrid loading time
imp_time = 0
if hybrid_files:
    times = []
    for i in range(10):
        start = time.time()
        with open(
            '{}/{}'.format(imp_folder, hybrid_files[0]),
            'r'
        ) as f:
            json.load(f)
        times.append((time.time() - start) * 1000)
    imp_time = round(sum(times) / len(times), 4)
    print("Hybrid groups created: {}".format(
        len(hybrid_files)))
    print("Hybrid loading time: {} ms".format(imp_time))

# ── STEP 9 — Verify ────────────────────────────────────
print("\nStep 9 - Verifying results...")

# Count all functions in hybrid groups
improved_data = {}
for hf in hybrid_files:
    with open(
        '{}/{}'.format(imp_folder, hf), 'r'
    ) as f:
        improved_data.update(json.load(f))

print("Original optional functions: {}".format(orig_funcs))
print("Hybrid grouped functions: {}".format(
    len(improved_data)))

if orig_funcs == len(improved_data):
    print("VERIFIED: Same {} optional functions".format(
        orig_funcs))
else:
    diff = orig_funcs - len(improved_data)
    print("MISMATCH: {} functions difference".format(diff))

# ── FINAL RESULT ───────────────────────────────────────
improvement = round(orig_time - imp_time, 4)
pct = round(
    (improvement / orig_time) * 100, 1) \
    if orig_time > 0 else 0

print("\n" + "="*60)
print("RESULT — {}".format(app_folder))
print("="*60)
print("Optional functions:    {}".format(orig_funcs))
print("Indispensable:         {}".format(len(final)))
print("Hybrid groups:         {}".format(len(hybrid_files)))
print("Original loading:      {} ms".format(orig_time))
print("Hybrid loading:        {} ms".format(imp_time))
print("Improvement:           {} ms".format(improvement))
print("Percentage faster:     {}%".format(pct))
print("="*60)

# Save result
result = {
    'app': app_folder,
    'optional_functions': orig_funcs,
    'indispensable': len(final),
    'hybrid_groups': len(hybrid_files),
    'original_ms': orig_time,
    'hybrid_ms': imp_time,
    'improvement_ms': improvement,
    'improvement_pct': pct
}

result_file = '{}_result.json'.format(app_folder)
with open(result_file, 'w') as f:
    json.dump(result, f, indent=2)
print("Result saved to {}".format(result_file))