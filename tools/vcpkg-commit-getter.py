import json
import subprocess

vcpkg_commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd='../external/vcpkg').decode('utf-8').strip()

with open('../vcpkg.json', 'r+') as file: 
    data = json.load(file)
    vcpkg_commit = data['builtin-baseline']
    print(f"Current vcpkg commit hash: {vcpkg_commit}")
    data['builtin-baseline'] = vcpkg_commit_hash
    print(f"New vcpkg commit hash: {vcpkg_commit_hash}")
    file.seek(0)  # Move the cursor to the beginning of the file
    json.dump(data, file, indent=4)
    file.truncate()  # Remove any leftover data from the old file size  