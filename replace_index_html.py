import re

path = 'c:/Github/-/presentation/index.html'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

replacements = [
    (
        r'<li><strong>Web GPT \(瞎子摸象\)</strong>：在網頁上用的 ChatGPT 看不到',
        r'<li><strong>受限的網頁工具</strong>：Web GPT (瞎子摸象) 在網頁上用的 ChatGPT 看不到'
    ),
    (
        r'<li><strong>IDE Agent \(數位工作室 / 頂級畫室\) \(長了眼睛跟手\)</strong>：像是 Antigravity',
        r'<li><strong>本地數位助理</strong>：IDE Agent (數位工作室 / 頂級畫室) (長了眼睛跟手) 像是 Antigravity'
    ),
    (
        r'<li><strong>SKILL \(設定檔\) = 品牌規範</strong>：將專案的',
        r'<li><strong>統一的品牌規範</strong>：SKILL (設定檔) 將專案的'
    ),
    (
        r'<li><strong>一鍵安裝</strong>：透過終端機指令，一鍵就能把大師的靈魂下載到你的專案 <code>\.agents/skills/</code> 裡，無縫接軌！',
        r'<li><strong>一鍵無縫安裝</strong>：透過終端機指令，一鍵就能把大師的靈魂下載到你的專案 <code>.agents/skills/</code> 裡，無縫接軌！'
    ),
    (
        r'<li><strong>Seed</strong>：就像角色的 <strong>DNA 基因碼</strong>，鎖定後能讓',
        r'<li><strong>鎖定初始基因</strong>：Seed 就像角色的 <strong>DNA 基因碼</strong>，鎖定後能讓'
    ),
    (
        r'<strong><i class="fa-solid fa-dna"></i> Seed \(隨機種子碼\)</strong>',
        r'<strong><i class="fa-solid fa-dna"></i> 鎖定初始基因 (Seed)</strong>'
    ),
    (
        r'<strong><i class="fa-solid fa-droplet"></i> 模型架構 \(Model Architecture\)</strong>',
        r'<strong><i class="fa-solid fa-droplet"></i> 模型血型匹配 (Model Architecture)</strong>'
    ),
    (
        r'<li><strong>🎬 Kling O3 \(可靈\)</strong>：地表最強物理運算。',
        r'<li><strong>最強物理動態</strong>：🎬 Kling O3 (可靈) 地表最強物理運算。'
    ),
    (
        r'<li><strong>🚀 Runway Gen-4</strong>：精準「專業運鏡控制」。',
        r'<li><strong>精準專業運鏡</strong>：🚀 Runway Gen-4 具備精準「專業運鏡控制」。'
    ),
    (
        r'<li><strong>🌟 SeedDance 2\.5</strong>：極致「多模態控制」。',
        r'<li><strong>多模態導演模式</strong>：🌟 SeedDance 2.5 提供極致「多模態控制」。'
    ),
    (
        r'<li><strong>🎥 Google Veo 3\.1</strong>：原生音效生成與電影語意理解。',
        r'<li><strong>原生音效語意</strong>：🎥 Google Veo 3.1 支援原生音效生成與電影語意理解。'
    ),
    (
        r'<li><strong>/goal \(死磕到底\)</strong>：加上',
        r'<li><strong>死磕到底</strong>：/goal 指令，加上'
    ),
    (
        r'<li><strong>/schedule \(定時鬧鐘\)</strong>：你可以設定定時器',
        r'<li><strong>定時鬧鐘</strong>：/schedule 指令，你可以設定定時器'
    ),
    (
        r'<li><strong>/grill-me \(反客為主\)</strong>：當你靈感枯竭時',
        r'<li><strong>反客為主</strong>：/grill-me 指令，當你靈感枯竭時'
    ),
    (
        r'<li><strong>/learn \(永恆印記\)</strong>：當你調教出',
        r'<li><strong>永恆印記</strong>：/learn 指令，當你調教出'
    ),
]

for old, new in replacements:
    text = re.sub(old, new, text)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated index.html formatting.")
