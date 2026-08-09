import re

path = 'c:/Github/-/presentation/index.html'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Find style attributes that only contain whitespace
pattern = r'style=\"\s*\"'
matches = list(re.finditer(pattern, text))

for m in matches[:10]:
    line_num = text[:m.start()].count('\n') + 1
    print(f'Line {line_num}: {m.group(0)}')

print(f'Total empty styles: {len(matches)}')

# Also replace them and write back
new_text = re.sub(pattern, '', text)
if len(matches) > 0:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Fixed empty styles in index.html.")
