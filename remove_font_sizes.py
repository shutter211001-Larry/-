import re

path = 'c:/Github/-/presentation/index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

count = 0
def repl(m):
    global count
    size_str = m.group(1)
    size = float(size_str)
    # Keep it if size >= 6 (like 6rem or 8rem for emojis), remove otherwise
    if size >= 6:
        return m.group(0) # Keep original
    else:
        count += 1
        # m.group(0) is like 'font-size: 3rem;'
        # we return empty string to remove it
        return ''

# match font-size: Xrem; and optional trailing space
pattern = r'font-size:\s*([0-9.]+)(?:rem|px|em);?\s*'
new_content = re.sub(pattern, repl, content)

print(f'Removed {count} inline font-size declarations.')
with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
