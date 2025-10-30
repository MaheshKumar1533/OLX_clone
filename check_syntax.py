#!/usr/bin/env python
"""
Quick syntax check for Python files
"""
import py_compile
import os
import sys

def check_file(filepath):
    try:
        py_compile.compile(filepath, doraise=True)
        return True, None
    except py_compile.PyCompileError as e:
        return False, str(e)

# Files to check
files_to_check = [
    'products/urls.py',
    'products/views.py',
    'accounts/views.py',
    'olx_clone/settings.py',
]

print("Checking Python files for syntax errors...\n")
all_good = True

for filepath in files_to_check:
    full_path = os.path.join(r'd:\Projects\OLX_clone', filepath)
    if os.path.exists(full_path):
        success, error = check_file(full_path)
        if success:
            print(f"✓ {filepath} - OK")
        else:
            print(f"✗ {filepath} - ERROR:")
            print(f"  {error}")
            all_good = False
    else:
        print(f"? {filepath} - File not found")

print("\n" + "="*50)
if all_good:
    print("All files passed syntax check!")
else:
    print("Some files have errors. Please review above.")
    sys.exit(1)
