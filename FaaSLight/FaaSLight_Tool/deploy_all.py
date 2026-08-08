import os
import sys
import json
import time
import boto3
import zipfile

REGION = 'us-east-1'
ROLE_ARN = 'arn:aws:iam::056106910789:role/LabRole'
LAYER_ARN = 'arn:aws:lambda:us-east-1:056106910789:layer:thesis-custom-funtemplate:1'
DEFAULT_HANDLER = 'main.lambda_handler'

# ── Optional: filter to a single app via command line ──
# Usage:
#   python3 deploy_all.py            -> runs every discovered app
#   python3 deploy_all.py realApp    -> runs only realApp
target_app = sys.argv[1] if len(sys.argv) > 1 else None


def discover_apps():
    """
    Auto-discover apps by scanning the current directory for
    '<name>_original' / '<name>_improved' folder pairs, instead of
    relying on a hardcoded list. Any app run through run_pipeline.py
    automatically becomes deployable here with zero script edits.
    """
    apps = []
    for entry in sorted(os.listdir('.')):
        if not entry.endswith('_original') or not os.path.isdir(entry):
            continue
        app_name = entry[:-len('_original')]
        imp_folder = '{}_improved'.format(app_name)
        if os.path.isdir(imp_folder):
            apps.append({
                'name': app_name,
                'handler': DEFAULT_HANDLER
            })
    return apps


def zip_folder(folder_path, zip_path):
    """Zip entire folder for Lambda deployment"""
    print("  Zipping {}...".format(folder_path))
    with zipfile.ZipFile(zip_path, 'w',
                         zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(folder_path):
            dirs[:] = [d for d in dirs
                      if d not in ['__pycache__', '.git']]
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(
                    file_path, folder_path)
                zf.write(file_path, arcname)

    size = os.path.getsize(zip_path)
    print("  Zipped: {:.1f} MB".format(
        size / 1024 / 1024))
    return zip_path


def deploy_lambda(function_name, zip_path,
                  handler, role_arn):
    """Deploy zip to AWS Lambda"""
    client = boto3.client('lambda', region_name=REGION)

    with open(zip_path, 'rb') as f:
        zip_bytes = f.read()

    try:
        client.get_function(FunctionName=function_name)
        client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_bytes
        )
        time.sleep(3)
        client.update_function_configuration(
            FunctionName=function_name,
            Layers=[LAYER_ARN]
        )
        print("  Updated: {}".format(function_name))

    except client.exceptions.ResourceNotFoundException:
        # Create new function
        client.create_function(
            FunctionName=function_name,
            Runtime='python3.9',
            Role=role_arn,
            Handler=handler,
            Code={'ZipFile': zip_bytes},
            Timeout=120,
            MemorySize=128,
            Description='FaaSLight Thesis - {}'.format(
                function_name),
            Layers=[LAYER_ARN]
        )
        print("  Created: {}".format(function_name))

    # Wait for function to be ready
    print("  Waiting for function to be ready...")
    waiter = client.get_waiter('function_active')
    waiter.wait(FunctionName=function_name)
    print("  Ready!")


def measure_cold_start(function_name, invocations=5):
    """Invoke Lambda and measure response times"""
    client = boto3.client('lambda', region_name=REGION)
    times = []

    print("  Invoking {} times...".format(invocations))
    for i in range(invocations):
        start = time.time()
        try:
            response = client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps({})
            )
            elapsed = (time.time() - start) * 1000
            times.append(elapsed)
            print("  Run {}: {:.2f} ms".format(
                i+1, elapsed))
        except Exception as e:
            print("  Run {} failed: {}".format(i+1, e))
        time.sleep(1)

    if times:
        return round(sum(times) / len(times), 2)
    return 0


if __name__ == "__main__":
    print("="*60)
    print("Lambda Deployment")
    print("Region: {}".format(REGION))
    print("Role: {}".format(ROLE_ARN))
    print("Layer: {}".format(LAYER_ARN))
    print("="*60)

    discovered_apps = discover_apps()

    if not discovered_apps:
        print("ERROR: No '<name>_original' / '<name>_improved' folder "
              "pairs found in the current directory. Run "
              "run_pipeline.py first.")
        sys.exit(1)

    apps_to_run = [a for a in discovered_apps if a['name'] == target_app] \
        if target_app else discovered_apps

    if target_app and not apps_to_run:
        print("ERROR: '{}' not found. Discovered apps: {}".format(
            target_app, [a['name'] for a in discovered_apps]))
        sys.exit(1)

    print("Apps to deploy: {}".format(
        [a['name'] for a in apps_to_run]))

    all_results = {}

    for app in apps_to_run:
        app_name = app['name']
        handler = app['handler']

        print("\n" + "="*60)
        print("Processing: {}".format(app_name))
        print("="*60)

        orig_folder = '{}_original'.format(app_name)
        imp_folder = '{}_improved'.format(app_name)

        if not os.path.exists(orig_folder):
            print("SKIP: {} not found".format(orig_folder))
            continue

        if not os.path.exists(imp_folder):
            print("SKIP: {} not found".format(imp_folder))
            continue

        orig_name = "thesis-{}-orig".format(
            app_name.replace('_', '-'))
        imp_name = "thesis-{}-impr".format(
            app_name.replace('_', '-'))

        try:
            # Deploy original
            print("\nDeploying original FaaSLight...")
            orig_zip = "{}_original.zip".format(app_name)
            zip_folder(orig_folder, orig_zip)
            deploy_lambda(orig_name, orig_zip,
                         handler, ROLE_ARN)

            # Deploy improved
            print("\nDeploying hybrid improvement...")
            imp_zip = "{}_improved.zip".format(app_name)
            zip_folder(imp_folder, imp_zip)
            deploy_lambda(imp_name, imp_zip,
                         handler, ROLE_ARN)

            # Measure cold start
            print("\nMeasuring original cold start...")
            orig_time = measure_cold_start(orig_name)

            print("\nMeasuring improved cold start...")
            imp_time = measure_cold_start(imp_name)

            # Calculate improvement
            improvement = round(orig_time - imp_time, 2)
            pct = round(
                (improvement / orig_time) * 100, 1) \
                if orig_time > 0 else 0

            all_results[app_name] = {
                'original_ms': orig_time,
                'improved_ms': imp_time,
                'improvement_ms': improvement,
                'improvement_pct': pct
            }

            print("\nResult for {}:".format(app_name))
            print("  Original:    {} ms".format(orig_time))
            print("  Improved:    {} ms".format(imp_time))
            print("  Improvement: {}%".format(pct))

            # Clean up zip files
            if os.path.exists(orig_zip):
                os.remove(orig_zip)
            if os.path.exists(imp_zip):
                os.remove(imp_zip)

        except Exception as e:
            print("ERROR processing {}: {}".format(
                app_name, e))
            import traceback
            traceback.print_exc()
            continue

    # Save results — merge with existing so other apps aren't wiped out
    existing_results = {}
    if os.path.exists('lambda_coldstart_results.json'):
        with open('lambda_coldstart_results.json', 'r') as f:
            existing_results = json.load(f)

    existing_results.update(all_results)

    with open('lambda_coldstart_results.json', 'w') as f:
        json.dump(existing_results, f, indent=2)

    # ── AUTO UPLOAD TO S3 ───────────────────────────────
    try:
        s3 = boto3.client('s3', region_name=REGION)
        s3.upload_file(
            'lambda_coldstart_results.json',
            'thesis-faaslight-results',
            'lambda_coldstart_results.json'
        )
        print("Cold start results uploaded to S3: "
              "lambda_coldstart_results.json")
    except Exception as e:
        print("S3 upload skipped: {}".format(e))

    print("\n" + "="*60)
    print("FINAL RESULTS (this run)")
    print("="*60)
    for app_name, r in all_results.items():
        print("{:<20} orig: {:>8} ms  "
              "impr: {:>8} ms  "
              "improvement: {}%".format(
            app_name,
            r['original_ms'],
            r['improved_ms'],
            r['improvement_pct']))
    print()
    print("Results saved to lambda_coldstart_results.json "
          "({} total apps tracked)".format(len(existing_results)))
          