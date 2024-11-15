import hashlib
import os
import json
def calculate_hash(file_path):
    sha256= hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while (chunk := f.read(4096)):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

def generate_baseline(directory, outputfile ="baseline.json"):
    baseline = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path= os.path.join(root, file)
            file_hash = calculate_hash(file_path)
            if (file_hash):
                baseline[file_path] = file_hash
                
    with open(outputfile, 'w') as f:
        json.dump(baseline, f, indent = 4)
    print(f"Baseline saved to {outputfile}")

def integrity_check(baselinefile = "baseline.json"):
    try:
        with open(baselinefile, "r") as f:
            baseline = json.load(f)
        for file_path, stored_hash in baseline.items():
            current_hash = calculate_hash(file_path)
            if not current_hash:
                print(f"FILE MISSING: {file_path}")
            elif (current_hash != stored_hash):
                print(f"FILE COMPROMISED: {file_path}")
            else:
                print(f"FILE INTACT: {file_path}")
    except FileNotFoundError:
        print(f"Baseline file not found: {baselinefile}")
    
                