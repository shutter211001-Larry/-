import re

path = 'c:/Github/-/presentation/index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

count = 0
def repl(m):
    global count
    count += 1
    return ''

pattern = r'[ \t]*<!--(?: Slide [\d\.]+?:)? 中場休息 -->\s*<section class="slide">\s*<div class="content-area"[^>]*>\s*<div[^>]*>☕<\/div>\s*<h2[^>]*>中場休息 \d+ 分鐘<\/h2>.*?<\/section>\s*'
new_content = re.sub(pattern, repl, content, flags=re.DOTALL)

print(f'Replaced {count} occurrences.')
with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
