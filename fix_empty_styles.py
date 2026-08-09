import re
import os

directory = 'c:/Github/-'
for root, _, files in os.walk(directory):
    if '.git' in root or '.agents' in root:
        continue
    for file in files:
        if file.endswith('.html') or file.endswith('.md'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # replace style="" or style="   " with nothing
            # meaning remove the whole style attribute
            new_content, count = re.subn(r'\bstyle=[\"\']\s*[\"\']', '', content)
            
            if count > 0:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Removed {count} empty style attributes in {file}")
