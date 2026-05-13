import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    if filepath.endswith('.py'):

        content = re.sub(r'(?m)^\s*#.*$', '', content)
        content = re.sub(r'(?m)
    elif filepath.endswith('.tsx') or filepath.endswith('.ts'):


        content = re.sub(r'(?m)^\s*//(?! eslint-disable).*$', '', content)
        content = re.sub(r'(?m)(?<!https:)(?<!http:)//.*$', '', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned {filepath}")

for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or '.next' in root or '.git' in root or 'venv' in root or '.venv' in root:
        continue
    for file in files:
        if file.endswith(('.py', '.tsx', '.ts')):
            process_file(os.path.join(root, file))
