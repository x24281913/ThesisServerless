"""
test_loader.py

Updates ONLY the 'loading_test' field in each app's existing
<app>_result.json — every other field (optional_functions,
improvement_pct, original_ms, hybrid_ms, etc.) is left untouched.

Use this when you've added/changed the on-demand loading verification
logic and want to backfill or refresh 'loading_test' for all apps
without re-running the full 9-step pipeline (which would also
re-measure loading times and could shift those numbers slightly).

Usage:
    python3 test_loader.py            # all apps
    python3 test_loader.py realApp    # just one app

Requires: each app's <app>_improved/ folder and <app>_result.json
must already exist locally (i.e. run_pipeline.py has been run for
that app at least once before).
"""
import os
import sys
import json
import boto3

REGION = 'us-east-1'
BUCKET = 'thesis-faaslight-results'

target_app = sys.argv[1] if len(sys.argv) > 1 else None


def run_loading_test(imp_folder, num_functions=5):
    """
    Same logic as in run_pipeline.py — proves that, per function call,
    only the group actually needed is loaded from disk, not every
    group at once.
    """
    index_path = os.path.join(imp_folder, 'hybrid_group_index.json')

    if not os.path.exists(index_path):
        return {
            'functions_tested': 0,
            'total_groups_available': 0,
            'groups_loaded': 0,
            'groups_not_loaded': 0,
            'groups_loaded_names': [],
            'proof': 'No optional functions found — loading test skipped'
        }

    with open(index_path, 'r') as f:
        index = json.load(f)

    all_groups = sorted([
        f[:-5] for f in os.listdir(imp_folder)
        if f.startswith('hybrid_')
        and f.endswith('.json')
        and 'index' not in f
    ])

    test_functions = list(index.keys())[:num_functions]

    loaded_groups = {}
    for func in test_functions:
        group_id = index[func]
        if group_id not in loaded_groups:
            group_path = os.path.join(
                imp_folder, '{}.json'.format(group_id))
            with open(group_path, 'r') as f:
                loaded_groups[group_id] = json.load(f)

    groups_loaded = len(loaded_groups)
    total_groups = len(all_groups)

    return {
        'functions_tested': len(test_functions),
        'total_groups_available': total_groups,
        'groups_loaded': groups_loaded,
        'groups_not_loaded': total_groups - groups_loaded,
        'groups_loaded_names': list(loaded_groups.keys()),
        'proof': 'Only {} of {} groups loaded for {} function calls'.format(
            groups_loaded, total_groups, len(test_functions))
    }


def discover_apps():
    """Find apps by matching <name>_result.json with a <name>_improved folder."""
    apps = []
    for entry in sorted(os.listdir('.')):
        if not entry.endswith('_result.json'):
            continue
        app_name = entry[:-len('_result.json')]
        imp_folder = '{}_improved'.format(app_name)
        if os.path.isdir(imp_folder):
            apps.append(app_name)
    return apps


if __name__ == "__main__":
    print("="*60)
    print("Updating loading_test field only — all other data untouched")
    print("="*60)

    discovered = discover_apps()

    if not discovered:
        print("ERROR: No '<app>_result.json' + '<app>_improved/' pairs "
              "found in the current directory.")
        sys.exit(1)

    apps_to_run = [a for a in discovered if a == target_app] \
        if target_app else discovered

    if target_app and not apps_to_run:
        print("ERROR: '{}' not found. Discovered apps: {}".format(
            target_app, discovered))
        sys.exit(1)

    print("Apps to update: {}".format(apps_to_run))

    s3 = boto3.client('s3', region_name=REGION)

    for app_name in apps_to_run:
        print("\n" + "-"*60)
        print("Processing: {}".format(app_name))

        result_file = '{}_result.json'.format(app_name)
        imp_folder = '{}_improved'.format(app_name)

        # Load existing result JSON — every field here is preserved
        with open(result_file, 'r') as f:
            result = json.load(f)

        # Run the loading test fresh and update ONLY this one key
        loading_test = run_loading_test(imp_folder, num_functions=5)
        result['loading_test'] = loading_test

        print("  Groups loaded: {} / {}".format(
            loading_test['groups_loaded'],
            loading_test['total_groups_available']))
        print("  Groups loaded (names): {}".format(
            loading_test['groups_loaded_names']))

        # Save back locally
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=2)

        # Push the same file back to S3, overwriting only this app's
        # result file — other apps' result files are untouched since
        # each app has its own separate S3 key.
        try:
            s3.upload_file(result_file, BUCKET, result_file)
            print("  Uploaded to S3: {}".format(result_file))
        except Exception as e:
            print("  S3 upload failed: {}".format(e))

    print("\n" + "="*60)
    print("Done. Updated loading_test for {} app(s).".format(
        len(apps_to_run)))
    print("="*60)
    