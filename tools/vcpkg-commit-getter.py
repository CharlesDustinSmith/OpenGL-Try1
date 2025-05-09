import json
import subprocess
import os

current_file_path = os.path.dirname(os.path.abspath(__file__))
base_folder_path = os.path.dirname(current_file_path)
vcpkg_folder_path = os.path.join(base_folder_path, 'external', 'vcpkg')

print(f"The current path is : {current_file_path}")
print(f"The Base folder path is : {base_folder_path}")
print(f"The VCPKG folder path is : {vcpkg_folder_path}")

vcpkg_commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=vcpkg_folder_path).decode('utf-8').strip()
print(f"Vcpkg commit hash: {vcpkg_commit_hash}")

with open('../vcpkg.json', 'r+') as file: 
    data = json.load(file)
    vcpkg_commit = data['builtin-baseline']
    print(f"Current vcpkg commit hash: {vcpkg_commit}")
    data['builtin-baseline'] = vcpkg_commit_hash
    print(f"New vcpkg commit hash: {vcpkg_commit_hash}")
    file.seek(0)  # Move the cursor to the beginning of the file
    json.dump(data, file, indent=4)
    file.truncate()  # Remove any leftover data from the old file size  