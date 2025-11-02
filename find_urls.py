import os
import re

def find_url_references(root_dir, old_url, search_pattern):
    """Find all files containing the old URL reference"""
    matches = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip venv and other non-essential directories
        if 'venv' in dirpath or '__pycache__' in dirpath or '.git' in dirpath:
            continue
            
        for filename in filenames:
            if filename.endswith('.html') or filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if old_url in content:
                            # Count occurrences
                            count = content.count(old_url)
                            matches.append((filepath, count))
                except Exception as e:
                    pass
    
    return matches

# Search for 'products:landing' references
root = r'd:\Projects\OLX_clone'
old_url = "products:landing"

print(f"Searching for '{old_url}' in {root}...\n")
results = find_url_references(root, old_url, old_url)

if results:
    print(f"Found {len(results)} files with '{old_url}':\n")
    for filepath, count in results:
        print(f"{filepath} ({count} occurrence(s))")
else:
    print(f"No files found with '{old_url}'")
