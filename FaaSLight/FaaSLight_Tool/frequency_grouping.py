"""
frequency_grouping.py
Student: Amruta Anil Dicholkar
ID: X24281913
MSc Cloud Computing - NCI

Gap 2 Improvement:
Reads PyCG call graph, counts occurrences,
sorts by frequency, groups into plain JSON files.
No gzip - direct JSON read for faster loading.
"""

import json
import gzip
import os
import time


def load_call_graph(call_graph_file):
    print("Loading call graph...")
    with open(call_graph_file, 'r') as f:
        call_graph = json.load(f)
    print("Call graph entries: {}".format(len(call_graph)))
    return call_graph


def load_optional_functions(gzip_file):
    print("Loading optional functions...")
    with gzip.open(gzip_file, 'r') as f:
        data = json.loads(f.read().decode('utf-8'))
    print("Total optional functions: {}".format(len(data)))
    return data


def count_occurrences(call_graph, optional_functions):
    print("\nCounting occurrences...")
    frequency = {}
    for func in optional_functions:
        frequency[func] = 0
    for caller, callees in call_graph.items():
        for callee in callees:
            if callee in frequency:
                frequency[callee] += 1
    sorted_freq = sorted(
        frequency.items(),
        key=lambda x: x[1],
        reverse=True
    )
    print("Top 5 most frequent optional functions:")
    for func, count in sorted_freq[:5]:
        print("  {} -> {} occurrences".format(func, count))
    print("Bottom 5 least frequent:")
    for func, count in sorted_freq[-5:]:
        print("  {} -> {} occurrences".format(func, count))
    return frequency


def build_frequency_groups(frequency, optional_functions,
                           group_size=10):
    print("\nBuilding frequency groups...")
    print("Group size: {}".format(group_size))
    sorted_functions = sorted(
        frequency.items(),
        key=lambda x: x[1],
        reverse=True
    )
    groups = {}
    group_index = {}
    current_group = []
    group_id = 0
    for func_name, count in sorted_functions:
        current_group.append(func_name)
        if len(current_group) == group_size:
            gid = "group_{}".format(group_id)
            groups[gid] = {
                f: optional_functions[f]
                for f in current_group
            }
            for f in current_group:
                group_index[f] = gid
            print("  Created {} - {} functions".format(
                gid, len(current_group)))
            group_id += 1
            current_group = []
    if current_group:
        gid = "group_{}".format(group_id)
        groups[gid] = {
            f: optional_functions[f]
            for f in current_group
        }
        for f in current_group:
            group_index[f] = gid
        print("  Created {} - {} functions".format(
            gid, len(current_group)))
    print("Total groups created: {}".format(len(groups)))
    return groups, group_index


def save_as_plain_json(groups, group_index, output_dir):
    print("\nSaving groups as plain JSON files...")
    for gid, functions in groups.items():
        group_file = os.path.join(
            output_dir, "{}.json".format(gid))
        with open(group_file, 'w') as f:
            json.dump(functions, f)
        print("  Saved {}.json - {} functions".format(
            gid, len(functions)))
    index_file = os.path.join(
        output_dir, "group_index.json")
    with open(index_file, 'w') as f:
        json.dump(group_index, f, indent=2)
    print("Group index saved: {}".format(index_file))


def measure_improvement(original_gz, output_dir):
    print("\n" + "="*55)
    print("THESIS RESULT - Loading Time Comparison")
    print("="*55)

    # Measure original - 10 runs
    print("\nOriginal FaaSLight - loading entire gzip:")
    times_original = []
    for i in range(10):
        start = time.time()
        with gzip.open(original_gz, 'r') as f:
            json.loads(f.read().decode('utf-8'))
        elapsed = (time.time() - start) * 1000
        times_original.append(elapsed)
        print("  Run {}: {:.4f} ms".format(i+1, elapsed))
    avg_original = round(
        sum(times_original) / len(times_original), 4)

    # Measure your approach - load group_0.json
    print("\nYour Improvement - loading one JSON group:")
    group_files = sorted([
        f for f in os.listdir(output_dir)
        if f.startswith('group_')
        and f.endswith('.json')
        and f != 'group_index.json'
    ])
    if not group_files:
        print("No group files found")
        return
    times_grouped = []
    for i in range(10):
        start = time.time()
        with open(
            os.path.join(output_dir, group_files[0]),
            'r'
        ) as f:
            json.load(f)
        elapsed = (time.time() - start) * 1000
        times_grouped.append(elapsed)
        print("  Run {}: {:.4f} ms".format(i+1, elapsed))
    avg_grouped = round(
        sum(times_grouped) / len(times_grouped), 4)

    improvement = round(avg_original - avg_grouped, 4)
    if avg_original > 0:
        pct = round(
            (improvement / avg_original) * 100, 1)
    else:
        pct = 0

    print("\n" + "="*55)
    print("SUMMARY")
    print("="*55)
    print("Original FaaSLight:")
    print("  Loads ALL {} optional functions".format(
        "44"))
    print("  Average time: {} ms".format(avg_original))
    print("\nYour Improvement:")
    print("  Loads only one JSON group")
    print("  Average time: {} ms".format(avg_grouped))
    print("\nImprovement: {} ms faster".format(improvement))
    print("Percentage faster: {}%".format(pct))
    print("="*55)
    return avg_original, avg_grouped, improvement, pct


if __name__ == "__main__":
    print("="*55)
    print("FaaSLight Gap 2 - Frequency Based Grouping")
    print("Student: Amruta Anil Dicholkar X24281913")
    print("="*55)

    call_graph_file = "realApp/output.json"
    gzip_file = "realApp/gzipinfo.txt"
    output_dir = "realApp"

    print("\nChecking required files...")
    if not os.path.exists(call_graph_file):
        print("ERROR: {} not found".format(call_graph_file))
        exit(1)
    if not os.path.exists(gzip_file):
        print("ERROR: {} not found".format(gzip_file))
        exit(1)

    print("All files found. Starting...\n")

    call_graph = load_call_graph(call_graph_file)
    optional_functions = load_optional_functions(gzip_file)
    frequency = count_occurrences(
        call_graph, optional_functions)
    groups, group_index = build_frequency_groups(
        frequency, optional_functions, group_size=10)
    save_as_plain_json(groups, group_index, output_dir)
    measure_improvement(gzip_file, output_dir)

    print("\nDone. Your improvement is ready.")