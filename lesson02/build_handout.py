from html import escape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parent
PDF_OUT = ROOT / "handout.pdf"
HTML_OUT = ROOT / "handout.html"

COMFY_PROMPT = """Wide shot of a free-spirited young woman running toward the camera through a sun-drenched field, white birds exploding upward all around her like symbols of freedom. Her hair and dress are caught by the wind, captured with crisp focus on her face and light motion blur in the foreground flowers and wings. Vivid colors, bright clear sky, optimistic, uplifting cinematic tone."""

IMAGE_PROMPT = """Use the attached photograph as the character, face, wardrobe, and styling reference. Create a cinematic 16:9 landscape image: a low-angle wide shot of the same androgynous young fashion figure crouching low on a nighttime stone pavement, chin lifted and dark eyes looking upward toward the lens. Preserve their recognizable face, shaggy black hair beneath the charcoal knit beanie, oversized charcoal V-neck sweater, dramatically wide pleated trousers, worn brown belt with dangling silver charms, pointed black shoes, and oversized black padded bag resting beside them. The camera sits just above the ground with a close 20mm wide-angle perspective, subtly enlarging the foreground knees and shoes while the old stone facade and wooden windows stretch away behind them; crisp focus holds on the face with gentle falloff toward the edges. Hard direct flash mixes with faint warm window light, deep graphite tones, raw nocturnal street-fashion energy, intimate, rebellious cinematic tone."""

VIDEO_PROMPT = """Low-angle wide shot of the androgynous fashion figure from 圖片1 crouching on a nighttime stone pavement in the pose established by 圖片2, slowly lifting their chin toward the lens as the old facade stretches above them. Their shaggy hair, loose knit layers, and silver belt charms shift lightly in the breeze, captured with crisp focus on the face and gentle motion blur at the edges of the wide trousers during one slow push forward. Hard direct flash, deep graphite tones, tense, intimate, rebellious cinematic tone."""
VEO_PRODUCT_PROMPT = (ROOT / "assets" / "jagua-veo-workflow-a-prompt.txt").read_text(encoding="utf-8")


def fit_image(path: Path, max_width: float, max_height: float) -> Image:
    """Scale an image into a bounding box without changing its aspect ratio."""
    pixel_width, pixel_height = ImageReader(str(path)).getSize()
    scale = min(max_width / pixel_width, max_height / pixel_height)
    return Image(str(path), width=pixel_width * scale, height=pixel_height * scale)


# ---------- shared HTML handout ----------

def hpage(number: str, title: str, body: str, dark: bool = False) -> str:
    cls = "page dark" if dark else "page"
    return f'<section class="{cls}"><div class="eyebrow">{number}</div><h2>{title}</h2>{body}<div class="footer"><span>第二堂紙本講義｜從 Comfy 提示詞到 Kling O3</span><span>{number.split("｜")[0]}</span></div></section>'


html_pages = []
html_pages.append(hpage("01｜封面", "從 Comfy 提示詞到 Kling O3", """
<p class="lead">導演用高階語言交代創意，Agent 讀懂既有工作流、重組提示詞、準備參考圖、操作 MCP，最後把有效方法保存成 Skill。</p>
<div class="hero-pair"><img src="assets/o3-character-source.jpg" alt="原始角色圖"><img src="assets/o3-shot-001-reference.png" alt="ChatGPT 低機位廣角參考圖"></div>
<div class="box gold"><b>課程主軸</b><p>Comfy、ChatGPT Image Generation、Kling O3 與提示詞是示範工具；真正要學的是如何引導 Agent 研究、提案、執行、驗收並留下可重跑紀錄。</p></div>
""", True))

html_pages.append(hpage("02｜Agent 與工具", "先分清楚模型、介面、工作流與工具連線", """
<div class="box cyan"><b>Agent 是什麼？</b><p>Agent 是帶著目標與規則，能讀取專案資料、使用工具、等待必要決定並檢查成果的人工智慧代理執行者。</p></div>
<table><tr><th>層次</th><th>本課例子</th><th>用途</th></tr><tr><td>模型</td><td>Gemini、OpenAI 模型、Kling O3</td><td>理解、推理或生成內容</td></tr><tr><td>工作介面</td><td>Antigravity、ChatGPT、Codex</td><td>放入資料、交代任務、使用工具</td></tr><tr><td>節點工作流</td><td>ComfyUI</td><td>把模型、條件、取樣與輸出接成流程</td></tr><tr><td>工具連線</td><td>MCP</td><td>把 Kling 等服務接成 Agent 工具</td></tr><tr><td>可重用規則</td><td>AGENTS.md、Skill</td><td>保存工作方法、確認點與驗收標準</td></tr></table>
<div class="cols"><div class="box"><b>導演負責</b><p>創意、取捨、權限與最終驗收。</p></div><div class="box"><b>Agent 負責</b><p>研究、轉譯、執行、紀錄與回報。</p></div></div>
"""))

WHY_AGENT_HTML = """
<div class="cols"><div class="box"><b>一般網頁對話</b><p>適合解釋概念、改寫文字、發想選項與一次性問答。回答完成後，資料搬移、工具操作、進度紀錄與結果檢查通常由使用者接手。</p></div><div class="box cyan"><b>Agent 工作模式</b><p>適合需要跨多個步驟持續推進的工作。Agent 可以讀取同一個專案、查證資料、修改檔案、操作工具、等待核准、追蹤任務並驗收成果。</p></div></div>
<div class="diagram"><span>讀專案</span><i>→</i><span>查證與提案</span><i>→</i><span>等待核准</span><i>→</i><span>使用工具</span><i>→</i><span>驗收與保存</span></div>
<table><tr><th>一般網頁對話已足夠</th><th>應改用 Agent</th></tr><tr><td>問題可以一次回答；不必讀整個專案；不需操作外部工具；結果由人自行執行與保存。</td><td>任務要多步驟推進；必須讀檔與查來源；要修改檔案或操作 MCP；需要核准點、驗收與可重跑紀錄。</td></tr></table>
<div class="box gold"><b>差別在工作方式，不在產品名稱</b><p>ChatGPT 接上專案資料、規則與工具時，也能以 Agent 方式工作。判斷重點是：它能不能持續完成任務，並留下下一步可檢查的證據。</p></div>
"""

html_model_page = hpage("04｜影片模型與 Agent 模型", "先分清楚生成器與代理執行者，再用對的方法比較", """
<div class="box cyan"><b>這裡有兩種「模型」</b><p><b>影片生成模型</b>把文字、圖片或影片參考轉成影片；<b>Agent 使用的語言模型</b>負責讀專案、查資料、寫模型專用提示詞並操作工具。兩者不能混成同一張排行榜。</p></div>
<h3>官方文件支持到哪裡</h3>
<table class="model-style-table"><tr><th>影片模型</th><th>文件支持的輸入結構</th><th>證據性質</th></tr><tr><td>Kling VIDEO 3.0／Omni</td><td>主體＋動作＋場景＋選用的攝影語言／光線／氣氛</td><td>官方提示指南</td></tr><tr><td>Veo 3.1</td><td>主體＋動作＋風格＋攝影／構圖／鏡頭／氣氛；聲音可明寫</td><td>官方提示指南</td></tr><tr><td>Runway Gen-4.5</td><td>圖片負責外觀；文字集中描述動作、攝影機與時間進程</td><td>官方提示指南</td></tr><tr><td>Seedance 2.5</td><td>時間區段、敘事、鏡位、動作、節奏與多模態參考</td><td>官方產品說明，非完整提示規範</td></tr><tr><td>Wan 2.2／ComfyUI</td><td>提示詞擴寫、負面提示與取樣參數；節點屬工作流控制</td><td>官方程式庫＋本課專案策略</td></tr></table>
<div class="box gold"><b>教學推論</b><p>固定創意意圖、素材、片長、畫幅與驗收標準，再依各模型的輸入責任改寫。這是公平測試設計，不代表某種句型必然得到較好的作品。</p></div>
<h3>Agent／語言模型另外比較</h3>
<table><tr><th>能力</th><th>共同評分</th></tr><tr><td>讀脈絡與查證</td><td>先讀 AGENTS.md、Skill、素材和紀錄；提供官方來源與日期</td></tr><tr><td>提案與執行</td><td>交付中文意圖、模型專用提示詞、素材責任、參數、核准點與驗收表</td></tr></table>
<blockquote>請讀取這個 Kling O3 專案，先交付方案與送片摘要，不要直接執行付費生成。</blockquote>
<p class="source">官方資料查閱：2026 年 10 月 12 日。Kling：https://kling.ai/quickstart/text-to-video-prompt-guide　Veo：https://ai.google.dev/gemini-api/docs/veo　Runway：https://help.runwayml.com/hc/en-us/articles/48324313115155-Image-to-Video-Prompting-Guide　Seedance：https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5　Wan：https://github.com/Wan-Video/Wan2.2</p>
""")

html_workflow_page = hpage("05｜完成版工作流", "先看 Agent 如何完成整支影片，再回頭拆對話", """
<div class="box cyan"><b>導演先給 Agent 的基準</b><p>指定目標模型 Kling O3，提供從 Comfy 帶來的提示詞範本、角色或商品素材、鏡頭創意、限制與完成標準。</p></div>
<div class="steps">
  <p><b>1｜讀取脈絡：</b>Agent 先讀 AGENTS.md、Skill、專案素材、既有紀錄與目前可用工具。</p>
  <p><b>2｜查證方法：</b>以官方文件與 MCP 即時回傳確認模型、輸入、參數與限制；把易變資訊標上日期。</p>
  <p><b>3｜提出方案：</b>交付中文意圖、參考圖提示詞、Kling O3 提示詞、素材責任、參數與驗收表。</p>
  <p><b>4｜核准參考圖：</b>導演確認角色或商品、姿態、鏡位、構圖、色彩與光線。</p>
  <p><b>5｜完成參考圖：</b>ChatGPT 產生正式第一幀；Agent 整理完整送片摘要。</p>
  <p><b>6｜核准付費送片：</b>導演確認圖片、提示詞、模型、片長、比例、解析度、音訊、版本數與提交次數。</p>
  <p><b>7｜Kling MCP 執行：</b>上傳素材並只提交一次，保存 generationId 與 taskTraceId。</p>
  <p><b>8｜追蹤與驗收：</b>等待期間只查同一任務；完成後逐項檢查，下一版只改一個主要變因。</p>
  <p><b>9｜保存方法：</b>本次素材與紀錄留在 Project；已驗證、可跨任務重用的方法寫入 Skill。</p>
</div>
<div class="cols"><div class="box gold"><b>人要決定的兩個位置</b><p>參考圖是否通過；是否允許付費提交影片。</p></div><div class="box"><b>Agent 每次要交付的證據</b><p>來源、方案、參數、任務編號、成品與逐項驗收結果。</p></div></div>
<h3>先分清楚三種文字</h3><table><tr><th>導演 → Agent</th><th>專案 → Agent</th><th>Agent → 模型</th></tr><tr><td>高階指令：目的、素材、限制、核准點與完成標準。</td><td>AGENTS.md／Skill：可重跑步驟、工具分工與驗收規則。</td><td>提示詞與參數：依目前模型的輸入方式整理本次可執行資料。</td></tr></table>
<div class="box gold"><b>如何判斷流程真的成立</b><p>每一步都要留下下一個人能檢查的交付物；工具顯示 COMPLETED 只代表執行結束，作品是否符合創意與品牌標準仍由導演驗收。</p></div>
""")

html_pages.append(hpage("課程地圖｜七章學習路線", "每一章都產出下一章能使用的東西", """
<table><tr><th>章節</th><th>學習任務</th><th>交給下一章的成果</th></tr><tr><td>01</td><td>建立共同語言</td><td>分清楚 Agent、工作介面、影片模型、提示詞與工具</td></tr><tr><td>02</td><td>選擇工作模式</td><td>判斷一般網頁對話何時足夠，何時需要 Agent</td></tr><tr><td>03</td><td>拆學員問題</td><td>定位需求、素材、方法、工具或驗收缺口</td></tr><tr><td>04</td><td>先看完整工作流</td><td>說出高階創意如何走到核准、執行、驗收與保存</td></tr><tr><td>05</td><td>追查方法來源</td><td>從原始對話與 Comfy 找到提示詞基準和決策證據</td></tr><tr><td>06</td><td>轉譯並完成任務</td><td>參考圖、Kling 輸入、MCP 任務紀錄與成片驗收</td></tr><tr><td>07</td><td>轉移並保存</td><td>商品影片方法與可重跑的 Skill</td></tr></table>
<h3>分享學員案例時的六個問題</h3><ol><li>原本真正想完成什麼？</li><li>Agent 當時能讀到哪些素材與規則？</li><li>Agent 自行補了哪些決定？</li><li>實際結果和期待差在哪裡？</li><li>當時只修成品，還是也修正工作規則？</li><li>留下了哪些可驗收、重跑與追蹤的紀錄？</li></ol>
"""))

html_pages.append(hpage("06｜完整對話脈絡", "從建立分工、犯錯、更正到正式送片", """
<table class="dialogue-ledger"><tr><th>回合</th><th>導演原話／事件</th><th>Agent 可見回覆與結果</th><th>工作流意義</th></tr><tr><td>1</td><td>建立新工作流；指定 Kling O3；「我擔任導演。」</td><td>列出六步流程與預設規格：16:9、5 秒、1080p、單版、單鏡頭、音效開啟；付費前等待核准。</td><td>先定義角色、工具、核准權與失敗邊界。</td></tr><tr><td>2</td><td>「這是提示詞範本，我們往後的提示詞風格都要照這個樣子。」並貼上 Comfy 提示詞。</td><td>拆出景別、主體、動作、環境、物理動態、焦點、模糊、色光與情緒順序。</td><td>描述基準由導演提供；Agent 分析與轉譯。</td></tr><tr><td>3</td><td>提供角色附件；「讓他蹲下抬頭，鏡頭使用廣角鏡頭看他。」</td><td>提出低機位、20mm 感、夜間石造街景、直閃、焦點、次要動態，以及參考圖與 O3 影片提示詞草案。</td><td>短創意被補成可見、可修改的方案。</td></tr><tr><td>4</td><td>「核准。」</td><td>歷史上誤用 Kling Image O3 生成參考圖：2 點、COMPLETED，並留下 generationId。</td><td>核准仍可能因工具責任不清而執行錯誤。</td></tr><tr><td>5</td><td>「交代下去，圖片是由 CHAT GPT 生成。」</td><td>正式參考圖改由 ChatGPT Image Generation；Kling 只負責影片。舊圖保留為歷史，不作正式輸入。</td><td>糾正同時更新成品狀態、後續規則與版本紀錄。</td></tr><tr><td>6</td><td>ChatGPT 正式參考圖完成。</td><td>送片前再次列出兩張輸入圖、5 秒、16:9、1080p、1 版、多鏡頭關閉與同步音訊開啟。</td><td>執行前把素材責任、參數與費用邊界變成可檢查摘要。</td></tr><tr><td>7</td><td>「生成第一段影片。」</td><td>提交一次；保存 generationId、taskTraceId、60 點與狀態變化，只查詢同一任務。</td><td>短指令成立，因為前面已有完整摘要和執行邊界。</td></tr><tr><td>8</td><td>QUEUING → RUNNING → COMPLETED</td><td>交付影片、封面、完成時間與連結失效提醒。</td><td>工具完成後仍要依驗收表判斷內容。</td></tr><tr><td>9</td><td>「你可以把我們的對話變成 TXT 檔給我嗎？」</td><td>把可見對話、提示詞、核准點與結果整理成 UTF-8 紀錄。</td><td>工作流不只執行，也要留下可追溯教材與專案紀錄。</td></tr></table>
<div class="cols"><div class="box gold"><b>兩個實際任務編號</b><p>歷史圖片：<code>AepElq…hPgN</code><br>正式影片：<code>AR3Cf4…clsi</code></p></div><div class="box cyan"><b>對話形成的規則</b><p>ChatGPT 生正式參考圖；Kling 只生影片；付費前交摘要；等待時不重複提交；舊版本保留。</p></div></div>
<p class="source">完整整理：ORIGINAL_DIALOGUE_TEACHING.md　原始紀錄：sources/Kling_O3_對話紀錄_2026-10-11.txt</p>
"""))

html_pages.append(hpage("07｜Comfy 提示詞來源", "這段示範提示詞是從既有 Comfy 工作流帶過來的", f"""
<pre class="dialogue-prompt">{escape(COMFY_PROMPT)}</pre>
<table><tr><th>段落</th><th>作用</th></tr><tr><td>Wide shot…running toward the camera</td><td>先說景別、主體與主要動作</td></tr><tr><td>white birds…hair and dress…wind</td><td>補上環境與次要動態</td></tr><tr><td>crisp focus…motion blur</td><td>指定焦點與允許模糊的位置</td></tr><tr><td>Vivid colors…cinematic tone</td><td>用色彩、光線與情緒收束</td></tr></table>
<div class="box cyan"><b>必須講清楚</b><p>這不是 Kling 官方提示詞範本。可沿用的是創意意圖與描述順序；搬到新模型時，仍須重新決定文字、參考圖與參數各自負責什麼。</p></div>
"""))

html_pages.append(hpage("08｜認識 Comfy", "提示詞只是節點工作流中的一項輸入", """
<div class="diagram"><span>模型</span><i>＋</i><span>提示詞／文字編碼</span><i>＋</i><span>參考控制</span><i>→</i><span>取樣</span><i>→</i><span>解碼</span><i>→</i><span>輸出</span></div>
<table><tr><th>角色</th><th>白話解釋</th><th>學員要看懂</th></tr><tr><td>模型載入</td><td>選擇負責生成的核心</td><td>換模型可能改變節點與提示詞需求</td></tr><tr><td>文字編碼</td><td>把提示詞轉成條件資料</td><td>編碼器必須與模型架構相容</td></tr><tr><td>參考控制</td><td>以圖片、姿勢、深度或 LoRA 增加條件</td><td>有些要求已由節點負責</td></tr><tr><td>取樣</td><td>依模型與條件逐步形成結果</td><td>種子、步數、引導、排程與降噪都會影響輸出</td></tr><tr><td>潛在資料</td><td>生成運算中的壓縮表示</td><td>過程中不一定是可直接觀看的像素</td></tr><tr><td>VAE／解碼器</td><td>把潛在資料轉成圖片</td><td>解碼後才得到可觀看內容</td></tr></table>
<div class="box gold"><b>搬移前先問</b><p>原工作流還用了哪些參考圖、ControlNet、LoRA、種子與取樣參數？哪些視覺結果其實不是由提示詞單獨控制？</p></div>
<div class="box cyan"><b>初學者先回答三題</b><p>這次由哪個模型生成？哪些條件不是寫在提示詞裡？結果在哪一步才變成可觀看的圖片？</p></div>
"""))

html_pages.append(hpage("08｜高階指令與三層語言", "導演說創意，Agent 補成可檢查方案", """
<div class="visual-row"><img src="assets/o3-character-source.jpg" alt="原始角色參考圖"><div><blockquote>「我想要這個角色風格，讓他蹲下抬頭，鏡頭使用廣角鏡頭看他。」</blockquote><p><b>導演已決定：</b>角色來源、蹲姿、抬頭與廣角視覺。</p><p><b>Agent 提案：</b>低機位、20mm 感、夜間場景、直閃、焦點、次要動態、鏡頭速度與結尾。</p></div></div>
<table><tr><th>層次</th><th>保存內容</th></tr><tr><td>導演 → Agent</td><td>成果、素材、限制、核准點與驗收方式</td></tr><tr><td>專案 → Agent</td><td>AGENTS.md／Skill 中的可重用規則</td></tr><tr><td>Agent → 模型</td><td>依目前模型整理的提示詞、參考圖角色與參數</td></tr></table>
<div class="box cyan"><b>原則</b><p>Agent 補的是可供導演核准的提案，不是偷偷替導演決定創意。</p></div>
"""))

html_pages.append(hpage("09｜ChatGPT 參考圖", "第一個核准點：先鎖定第一幀能看見的事", f"""
<div class="hero-pair small-images"><img src="assets/o3-character-source.jpg" alt="原始角色圖"><img src="assets/o3-shot-001-reference.png" alt="ChatGPT 參考圖"></div>
<table><tr><th>素材</th><th>責任</th></tr><tr><td>原始角色圖</td><td>角色身分、臉部、髮型、服裝與配件</td></tr><tr><td>ChatGPT 正式參考圖</td><td>蹲姿、低機位、廣角透視、構圖、場景、色彩與光線</td></tr></table>
<h3>完整參考圖提示詞</h3><pre class="smallcode">{escape(IMAGE_PROMPT)}</pre>
<div class="box"><b>中文脈絡</b><p>先指定附件負責角色，再描述一個靜止瞬間；接著鎖定姿態、鏡位、透視、焦點、光線與情緒。長時間事件留到影片階段。</p></div>
"""))

html_pages.append(hpage("09｜Kling O3 影片提示詞", "實作後精鍊成三句，每句只負責一件事", f"""
<pre class="smallcode">{escape(VIDEO_PROMPT)}</pre>
<table><tr><th>句子</th><th>這一句的責任</th></tr><tr><td>第一句｜鏡頭與事件</td><td>鏡位開場；自然交代圖片1負責角色、圖片2負責姿態；只寫一個主要動作與一個環境事件。</td></tr><tr><td>第二句｜物理與攝影</td><td>頭髮、衣料與飾品的自然反應；臉保持清楚；邊緣才允許模糊；只保留一次慢速前推。</td></tr><tr><td>第三句｜視覺與情緒</td><td>以直閃、深石墨色與三個同方向的情緒詞俐落收尾。</td></tr></table>
<div class="box gold"><b>這是精鍊後的專案準則</b><p>三句通常控制在 55—100 個英文單字，讀起來像一個電影瞬間。它來自本專案實作整理，不是 Kling 官方保證有效的固定語法；仍須用成片驗證。</p></div>
<p class="source">完整準則：<a href="sources/KLING_O3_PROMPT_GUIDELINES.md">KLING_O3_PROMPT_GUIDELINES.md</a></p>
"""))

html_pages.append(hpage("10｜修正、核准與 MCP", "把一次糾正變成後續規則", """
<div class="cols"><div class="box bad"><b>歷史版本</b><p>Kling Image O3 曾完成一張參考圖，但不符合導演指定的工具分工。</p></div><div class="box good"><b>更正後</b><p>正式參考圖由 ChatGPT Image Generation 產生；Kling 只負責影片。</p></div></div>
<h3>兩個核准點</h3><ol><li><b>參考圖核准：</b>確認角色、姿態、鏡位、構圖與視覺方向。</li><li><b>影片提交核准：</b>確認圖片、提示詞、模型、片長、比例、解析度、音訊、版本數與允許提交次數。</li></ol>
<h3>Kling MCP 工具鏈</h3><div class="diagram"><span>who_am_i</span><i>→</i><span>file_upload</span><i>→</i><span>image_to_video</span><i>→</i><span>generationId</span><i>→</i><span>query_tasks</span></div>
<p><b>學員不必先寫 MCP 程式：</b>先會確認登入與模型、看懂提交參數、保存 generationId，並只查詢同一筆任務。</p>
<div class="box cyan"><b>本次歷史紀錄</b><p>5 秒、16:9、1080p、1 版；多鏡頭關閉、同步音訊開啟；任務依序為 QUEUING → RUNNING → COMPLETED。點數與模型能力只代表 2026 年 10 月 11 日這次執行。</p></div>
"""))

html_pages.append(hpage("10｜MODEL 成片驗收", "工具顯示完成，作品仍要由導演判斷", """
<div class="model-handout-proof"><video controls playsinline preload="metadata" poster="assets/shot-001-kling-o3-poster.jpg"><source src="assets/shot-001-crouching-wide-angle-kling-o3-v1.mp4" type="video/mp4"></video><div><h3>MODEL 成片</h3><p>SHOT-001｜Kling O3｜5 秒｜16:9｜1080p</p><p class="source">HTML 講義可直接播放；紙本與 PDF 顯示代表畫面。</p></div></div>
<table><tr><th>SHOT-001 驗收</th><th>可觀察標準</th></tr><tr><td>人物一致性</td><td>臉、髮型、灰色服裝、身形與配件保持</td></tr><tr><td>表演與鏡頭</td><td>低頭到抬頭清楚；低機位、廣角透視與一次平順前推成立</td></tr><tr><td>物理與結尾</td><td>頭髮、衣料、銀飾自然；最後一秒臉部與構圖仍可使用</td></tr></table>
<div class="box gold"><b>單一變因修改示範</b><p>保留人物、服裝、場景、光線與抬頭動作；只把攝影機前推速度降低一半。通過條件是人物比例穩定，最後一秒臉部仍清楚。</p></div>
"""))

html_product_page = hpage("11｜商品案例", "SHOT-002：從兩張參考圖到商品英雄水幕", """
<p><b>商品：</b>Schwarzkopf Professional BC Bonacure Repair Rescue Shampoo（極緻修護髮露）。</p>
<div class="asset-trio asset-pair"><figure><img src="assets/shot-002-product-tail.png" alt="Schwarzkopf 修護髮露的英雄結尾參考圖"><figcaption><b>圖片 1｜結尾英雄畫面</b><br>白色瓶身、桃紅壓頭、標籤、材質、藍色背景、桃紅底座與完整水幕。</figcaption></figure><figure><img src="assets/shot-002-product-opening.png" alt="ChatGPT 產生的商品開場參考圖"><figcaption><b>圖片 2｜ChatGPT 開場構圖</b><br>9:16 開場、低水位、平靜畫面與商品起始位置。</figcaption></figure></div>
<table><tr><th>輸入</th><th>交給它的責任</th></tr><tr><td>圖片 1</td><td>固定商品身分、瓶身比例、桃紅壓頭、標籤、材質、風格與最後的英雄構圖。</td></tr><tr><td>圖片 2</td><td>固定較平靜的開場、較低的水位、9:16 畫幅和商品起始位置。</td></tr><tr><td>Kling 提示詞</td><td>描述水從兩側聚集並升成透明水幕；一次緩慢前推與輕微上移；要求商品和文字全程穩定；補上水聲與商業情緒。</td></tr></table>
<div class="product-proof"><video controls muted playsinline preload="metadata" poster="assets/shot-002-product-video-poster.jpg"><source src="assets/shot-002-product-kling-o3-v1.mp4" type="video/mp4"></video><figure><img src="assets/shot-002-product-video-contact.jpg" alt="SHOT-002 開始、中段與結尾接觸表"><figcaption><b>成片接觸表</b><br>從低水位開場，到水幕上升，再回到完整英雄構圖。</figcaption></figure></div>
<table><tr><th>驗收面向</th><th>畫面上要檢查什麼</th></tr><tr><td>商品保真</td><td>白色瓶身、桃紅壓頭、瓶身比例、品牌標誌與標籤是否跨影格保持穩定。</td></tr><tr><td>環境動態</td><td>水是否由低到高自然聚集，水幕是否支援商品且沒有遮住標籤。</td></tr><tr><td>攝影機</td><td>是否只做一次緩慢前推與輕微上移，沒有突然縮放或多餘繞行。</td></tr><tr><td>結尾與聲音</td><td>結尾是否接近圖片 1 的英雄構圖；水聲是否自然且沒有搶走主體。</td></tr></table>
<div class="box gold"><b>實際生成紀錄</b><p><code>kling-video-v3_0_omni</code>｜5 秒｜9:16｜1080p｜24 fps｜單鏡頭｜同步音訊開啟｜狀態 COMPLETED。這是 2026 年 10 月 11 日的單次紀錄；授課前仍由 MCP 重新確認模型名稱與能力。</p></div>
""")

html_veo_storyboard_page = hpage("12｜Gemini Veo 商品案例", "先看成片，再看首幀與六格故事版如何分工", """
<div class="box cyan"><b>模型來源提醒</b><p>以下三支 Jagua Blue Radiance 商品影片是本專案以 Gemini Veo 產生的實際結果。海灘情境是獨立段落；商品與水、商品微距對應 Workflow A。</p></div>
<div class="veo-video-row"><figure><video controls muted playsinline preload="metadata"><source src="assets/jagua-generated-01-beach.mp4" type="video/mp4"></video><figcaption><b>海灘情境</b><br>環境、色調與品牌氣氛</figcaption></figure><figure><video controls muted playsinline preload="metadata"><source src="assets/jagua-generated-02-product-water.mp4" type="video/mp4"></video><figcaption><b>商品與水</b><br>瓶身、水與主運鏡</figcaption></figure><figure><video controls muted playsinline preload="metadata"><source src="assets/jagua-generated-03-product-macro.mp4" type="video/mp4"></video><figcaption><b>商品微距</b><br>材質、泡沫、反光與焦點</figcaption></figure></div>
<div class="veo-input-pair"><figure><img src="assets/jagua-veo-first-frame.jpg" alt="Gemini Veo 商品影片的首幀母幀"><figcaption><b>圖片 1｜首幀母幀</b><br>固定商品外觀、標籤、材質、色調與光影。</figcaption></figure><figure><img src="assets/jagua-veo-workflow-a-storyboard.webp" alt="Gemini Veo 商品影片的六格故事版"><figcaption><b>圖片 2｜Workflow A 六格故事版</b><br>微距 → 精華滴落 → 側向水花 → 泡沫 → 斜向沖洗 → 瓶肩與瓶蓋收尾。</figcaption></figure></div>
<table><tr><th>素材</th><th>交給 Veo 的責任</th></tr><tr><td>圖片 1</td><td>商品瓶型、標籤、材質、深海藍色調與水波折射光。</td></tr><tr><td>圖片 2</td><td>六段動作的順序與構圖；黑白線稿、格線不得進入成片。</td></tr><tr><td>提示詞</td><td>明確分配兩張圖的責任，再補上運鏡、動作時間線與禁止事項。</td></tr></table>
""")

html_veo_prompt_page = hpage("13｜Gemini Veo 實際提示詞", "Workflow A v5.0：原文與中文閱讀方法", f"""
<div class="cols"><div class="box cyan"><b>先看素材責任</b><p>Image 1 是外觀與光影的唯一依據；Image 2 只提供動作順序。</p></div><div class="box gold"><b>再看時間結構</b><p>Camera Movement 說明整體剪接；VFX Timeline 逐格指定水花、泡沫、沖洗與收尾。</p></div></div>
<pre class="veo-full-prompt">{escape(VEO_PRODUCT_PROMPT)}</pre>
<p class="source">完整文字檔：<a href="assets/jagua-veo-workflow-a-prompt.txt">jagua-veo-workflow-a-prompt.txt</a>。專案紀錄版本為 Workflow A v5.0，更新日期 2026-09-02；原文同時寫有 Veo／Omni，本案例成片依專案紀錄標示為 Gemini Veo。</p>
""")

html_pages.append(hpage("14｜保存與來源", "把方法保存成 Skill，把本次素材留在 Project", """
<div class="cols"><div class="box cyan"><b>Project 保存</b><p>角色、圖片、提示詞、參數、generationId、taskTraceId、成本、結果與導演回饋。</p></div><div class="box gold"><b>Skill 保存</b><p>讀脈絡、找可信資料、提出方案、核准、MCP、追蹤、驗收與失敗處理。</p></div></div>
<h3>課前確認</h3><ul><li>實際 Comfy 工作流、模型與節點可開啟。</li><li>原始角色圖、ChatGPT 定稿圖與完成影片已有本機備份。</li><li>Kling MCP 已連線，並以能力查詢工具確認模型、參數、素材上限與帳號能力。</li><li>模型名稱、點數與介面位置重新查證，不沿用歷史數值。</li></ul>
<h3>官方資料</h3><p class="source">OpenAI 模型選擇：https://learn.chatgpt.com/docs/model-selection<br>Antigravity 官方概覽：https://www.antigravity.google/docs/overview<br>Gemini 模型文件：https://ai.google.dev/gemini-api/docs/models<br>ComfyUI 核心概念：https://docs.comfy.org/essentials/core-concepts/links<br>CLIP Text Encode：https://docs.comfy.org/built-in-nodes/ClipTextEncode<br>KSampler：https://docs.comfy.org/built-in-nodes/KSampler<br>VAE Decode：https://docs.comfy.org/built-in-nodes/VAEDecode<br>Kling 圖片生成影片：https://kling.ai/quickstart/image-to-video-guide</p>
<div class="box"><b>最後的學習成果</b><p>換一個角色、商品或模型後，學員能用高階語言讓 Agent 重新研究、提出方案、執行、驗收並留下可重跑的工作流。</p></div>
"""))

def inner(page: str) -> str:
    match = re.search(r"</h2>(.*)<div class=\"footer\">", page, re.S)
    if not match:
        raise ValueError("Unable to extract handout page body")
    return match.group(1)


compact_html_pages = [
    html_pages[0],
    hpage("02｜Agent 與工具", "先分清楚模型、介面、工作流與工具連線", inner(html_pages[1])),
    hpage("03｜為什麼使用 Agent", "一般網頁對話適合回答，Agent 適合完成跨步驟專案", WHY_AGENT_HTML + "<h3>七章學習路線</h3>" + inner(html_pages[2])),
    html_model_page,
    html_workflow_page,
    hpage("06｜完整對話脈絡", "從建立分工、犯錯、更正到正式送片", inner(html_pages[3])),
    hpage("07｜Comfy 提示詞來源", "導演提供完整基準，Agent 分析描述順序", inner(html_pages[4])),
    hpage("08｜Comfy 與高階指令", "先看懂節點資料流，再讓 Agent 補成方案", inner(html_pages[5]) + "<h3>導演如何下高階指令</h3>" + inner(html_pages[6])),
    hpage("09｜從參考圖到影片提示詞", "第一幀定稿後，再補上時間中會發生的事", inner(html_pages[7]) + "<h3>Kling O3 影片提示詞與中文脈絡</h3>" + inner(html_pages[8])),
    hpage("10｜修正、MCP 與驗收", "把一次糾正變成規則，再判斷作品是否通過", inner(html_pages[9]) + "<h3>MODEL 成片驗收</h3>" + inner(html_pages[10])),
    html_product_page,
    html_veo_storyboard_page,
    html_veo_prompt_page,
    hpage("14｜保存、重跑與來源", "把有效方法留下來，下一次只給高階創意", inner(html_pages[11]) + """
<h3>交給 Agent 的重跑指令</h3><pre>請使用 Kling O3 導演工作流處理這個鏡頭。先讀專案規則、既有鏡頭紀錄與參考素材；交付中文意圖摘要、ChatGPT 參考圖提示詞、Kling O3 影片提示詞、每張素材的用途、生成參數與驗收表。參考圖核准後才能進入送片準備；付費影片提交前再次提供完整摘要並等待核准。提交後只追蹤同一個 generationId。完成後逐項驗收，每次只改一個主要變因，並把紀錄留在本次 Project。</pre>
<h3>失敗與等待怎麼處理</h3><table><tr><th>狀況</th><th>Agent 的處理</th></tr><tr><td>參考圖未通過</td><td>只修改參考圖方案，不進入 Kling 付費提交。</td></tr><tr><td>QUEUING／RUNNING</td><td>繼續查詢同一個 generationId，不重複提交。</td></tr><tr><td>FAILED／CANCELLED</td><td>回報原因與原參數，等待導演決定是否重試。</td></tr><tr><td>完成但偏離目標</td><td>依驗收表指出一個主要偏差，下一版只改一項。</td></tr><tr><td>成果網址可能失效</td><td>將核准成品下載到 Project，保存來源與任務紀錄。</td></tr></table>
"""),
]

html_css = """
@page{size:A4;margin:14mm 15mm 17mm}*{box-sizing:border-box}body{margin:0;background:#e9ecef;color:#202531;font:9.2pt/1.48 "Noto Sans TC","Microsoft JhengHei",sans-serif}.page{position:relative;width:210mm;min-height:297mm;margin:12px auto;padding:14mm 15mm 18mm;background:#fff;page-break-after:always;box-shadow:0 8px 30px #1b23301d}.page:last-child{page-break-after:auto}.page.dark{background:#111620;color:#f4f0e8}.page.dark h2,.page.dark h3,.page.dark b{color:#f4f0e8}.page.dark .box{color:#202531}.page.dark .box b,.page.dark .box h3{color:#18202b}.eyebrow{color:#a76c31;letter-spacing:.13em;font-size:8pt;font-weight:700;margin-bottom:4px}h2,h3{font-family:"Noto Serif TC","Microsoft JhengHei",serif;color:#18202b}h2{font-size:19pt;line-height:1.22;margin:0 0 9px}h3{font-size:11pt;margin:10px 0 4px}.lead{font-size:12.5pt;line-height:1.55}p{margin:3px 0 6px}ul,ol{padding-left:19px;margin:4px 0}li{margin:2px 0}table{width:100%;border-collapse:collapse;margin:7px 0;font-size:7.9pt}th,td{padding:5px 7px;border-bottom:1px solid #d9dde1;text-align:left;vertical-align:top}th{background:#f3f1ec;color:#7b4f23}.box{border:1px solid #d7dde2;border-radius:9px;padding:7px 9px;margin:6px 0}.gold{background:#fbf5eb;border-color:#e7d1ae}.cyan{background:#eff8f8;border-color:#c3e2e3}.bad{background:#fff2f0}.good{background:#effaf5}.cols{display:grid;grid-template-columns:1fr 1fr;gap:8px}.hero-pair{display:grid;grid-template-columns:.7fr 1.3fr;gap:8px;margin:10px 0}.hero-pair img{width:100%;height:105mm;object-fit:contain;border-radius:9px}.small-images img{height:52mm}.visual-row{display:grid;grid-template-columns:48mm 1fr;gap:10px;align-items:start}.visual-row img{width:48mm;height:69mm;object-fit:contain;border-radius:8px}blockquote{margin:0 0 7px;padding:9px 11px;background:#f3f5f7;border-left:3px solid #a76c31;font:10.5pt/1.48 "Noto Serif TC","Microsoft JhengHei",serif}.steps p{border-left:3px solid #d19b5e;padding-left:8px;margin:6px 0}pre{white-space:pre-wrap;word-break:break-word;background:#f3f5f7;border:1px solid #dce0e4;border-radius:7px;padding:8px 10px;font:7.2pt/1.42 Consolas,"Microsoft JhengHei",monospace}.smallcode{font-size:6.5pt;line-height:1.35}.diagram{display:flex;flex-wrap:wrap;align-items:center;gap:5px;margin:8px 0}.diagram span{padding:6px 8px;border:1px solid #cbd3db;border-radius:7px;background:#f3f6f8;font-weight:700}.diagram i{color:#a76c31;font-style:normal}.source{font-size:7.2pt;overflow-wrap:anywhere}.footer{position:absolute;left:15mm;right:15mm;bottom:7mm;display:flex;justify-content:space-between;border-top:1px solid #dde1e5;padding-top:3px;color:#7d858e;font-size:7pt}.page.dark .footer{border-color:#404754;color:#adb3bd}@media print{body{background:#fff}.page{margin:0;box-shadow:none}}
"""

html_css += """
.asset-trio{display:grid;grid-template-columns:.72fr 1.14fr 1.14fr;gap:7px}.asset-trio.asset-pair{grid-template-columns:1fr 1fr}.asset-trio figure,.poster-grid figure,.product-proof figure{margin:0;padding:5px;border:1px solid #d9dde1;border-radius:7px;background:#f7f8f9}.asset-trio img{width:100%;height:48mm;object-fit:contain;display:block}.asset-trio figure:first-child img,.asset-pair figure:first-child img{object-fit:contain}.asset-trio figcaption,.poster-grid figcaption,.product-proof figcaption{font-size:7pt;line-height:1.32;color:#59636e;padding-top:3px}.poster-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:6px}.poster-grid img{width:100%;height:52mm;object-fit:contain;display:block;border-radius:4px}.product-proof{display:grid;grid-template-columns:.42fr 1.58fr;gap:7px;margin:7px 0}.product-proof video{display:block;width:100%;height:55mm;object-fit:contain;border-radius:7px;background:#111620}.product-proof img{display:block;width:100%;height:45mm;object-fit:contain;border-radius:4px}
.variable-grid{display:grid;grid-template-columns:1fr 1fr;gap:7px}.variable-grid.variable-grid-three{grid-template-columns:repeat(3,1fr)}.variable-grid figure{margin:0;padding:5px;border:1px solid #d9dde1;border-radius:7px;background:#f7f8f9}.variable-grid img{display:block;width:100%;height:47mm;object-fit:contain;border-radius:4px}.variable-grid-three img{height:39mm}.variable-grid figcaption{font-size:7pt;line-height:1.35;color:#59636e;padding-top:3px}
.camera-variable{display:grid;grid-template-columns:1.18fr .82fr;gap:7px;margin-top:7px;padding:5px;border:1px solid #d9dde1;border-radius:7px;background:#f7f8f9}.camera-variable img{display:block;width:100%;height:48mm;object-fit:contain;border-radius:4px}.camera-variable h3{margin-top:0}.camera-variable p{font-size:7pt;line-height:1.35;margin:2px 0}
.character-plate-stack{display:grid;gap:6px}.character-plate-stack figure{margin:0;padding:5px;border:1px solid #d9dde1;border-radius:7px;background:#f7f8f9}.character-plate-stack img{display:block;width:100%;height:58mm;object-fit:contain;border-radius:4px}.character-plate-stack figcaption{font-size:7.2pt;line-height:1.38;color:#59636e;padding-top:3px}.character-plate-stack-two img{height:65mm}
.dialogue-ledger{font-size:7.35pt}.dialogue-ledger th,.dialogue-ledger td{padding:4.6px 5px;line-height:1.34}.dialogue-ledger th:first-child,.dialogue-ledger td:first-child{width:7mm;text-align:center}.dialogue-prompt{font-size:8.2pt;line-height:1.52;padding:12px}
.model-handout-proof{display:grid;grid-template-columns:1.35fr .65fr;gap:7px;margin:7px 0;padding:5px;border:1px solid #d9dde1;border-radius:7px;background:#f7f8f9}.model-handout-proof video{display:block;width:100%;height:46mm;object-fit:contain;border-radius:5px;background:#111620}.model-handout-proof h3{margin-top:2px}.model-handout-proof p{font-size:7.2pt}
.veo-video-row{display:grid;grid-template-columns:repeat(3,1fr);gap:7px}.veo-video-row figure,.veo-input-pair figure{margin:0;padding:5px;border:1px solid #d9dde1;border-radius:7px;background:#f7f8f9}.veo-video-row video{display:block;width:100%;height:57mm;object-fit:cover;border-radius:5px;background:#111620}.veo-video-row figcaption,.veo-input-pair figcaption{font-size:7.1pt;line-height:1.35;color:#59636e;padding-top:3px}.veo-input-pair{display:grid;grid-template-columns:.58fr 1.42fr;gap:7px;margin-top:7px}.veo-input-pair img{display:block;width:100%;height:64mm;object-fit:contain;border-radius:5px;background:#f3f5f7}.veo-full-prompt{font-size:6.5pt;line-height:1.34;max-height:none}
"""

HTML_OUT.write_text(
    f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>第二堂紙本講義｜從 Comfy 提示詞到 Kling O3</title><style>{html_css}</style></head><body>{"".join(compact_html_pages)}</body></html>',
    encoding="utf-8",
)


# ---------- matching 14-page PDF ----------

pdfmetrics.registerFont(TTFont("TC", r"C:\Windows\Fonts\msjh.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("TCBold", r"C:\Windows\Fonts\msjhbd.ttc", subfontIndex=0))
INK, MUTED, GOLD = colors.HexColor("#202531"), colors.HexColor("#66717e"), colors.HexColor("#a76c31")
LINE, PALE, CYAN = colors.HexColor("#d9dde1"), colors.HexColor("#fbf5eb"), colors.HexColor("#eff8f8")
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Eye", fontName="TCBold", fontSize=8, leading=11, textColor=GOLD, spaceAfter=4))
styles.add(ParagraphStyle(name="TitleTC", fontName="TCBold", fontSize=20, leading=27, textColor=INK, spaceAfter=8))
styles.add(ParagraphStyle(name="H3TC", fontName="TCBold", fontSize=11, leading=15, textColor=INK, spaceBefore=7, spaceAfter=4))
styles.add(ParagraphStyle(name="BodyTC", fontName="TC", fontSize=8.4, leading=13, textColor=INK, spaceAfter=4))
styles.add(ParagraphStyle(name="SmallTC", fontName="TC", fontSize=6.7, leading=9.6, textColor=MUTED, spaceAfter=3))
styles.add(ParagraphStyle(name="CodeTC", fontName="TC", fontSize=6.4, leading=9.1, textColor=INK))
styles.add(ParagraphStyle(name="CodeVeo", fontName="TC", fontSize=7.2, leading=10.4, textColor=INK))
styles.add(ParagraphStyle(name="CodePrompt", fontName="TC", fontSize=8.1, leading=12.2, textColor=INK))


def p(text, style="BodyTC"):
    return Paragraph(text, styles[style])


def box(items, bg=colors.white, border=LINE, pad=7):
    if not isinstance(items, list):
        items = [items]
    t = Table([[items]], colWidths=[174 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg), ("BOX", (0, 0), (-1, -1), .6, border), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), pad), ("RIGHTPADDING", (0, 0), (-1, -1), pad), ("TOPPADDING", (0, 0), (-1, -1), pad), ("BOTTOMPADDING", (0, 0), (-1, -1), pad)]))
    return t


def grid(rows, widths, font=7.5):
    data = []
    for ri, row in enumerate(rows):
        row_data = []
        for cell in row:
            st = ParagraphStyle(name=f"c{ri}{len(row_data)}", fontName="TCBold" if ri == 0 else "TC", fontSize=font, leading=font + 2.7, textColor=GOLD if ri == 0 else INK)
            row_data.append(Paragraph(str(cell).replace("\n", "<br/>"), st))
        data.append(row_data)
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), .4, LINE), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f3f1ec")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return t


def head(number, title):
    return [p(number, "Eye"), p(title, "TitleTC")]


def footer(canvas, doc):
    canvas.saveState(); canvas.setStrokeColor(LINE); canvas.line(18*mm, 14*mm, 192*mm, 14*mm)
    canvas.setFont("TC", 7); canvas.setFillColor(MUTED); canvas.drawString(18*mm, 9*mm, "第二堂紙本講義｜從 Comfy 提示詞到 Kling O3"); canvas.drawRightString(192*mm, 9*mm, f"{doc.page:02d}"); canvas.restoreState()


story = []
story += head("01｜封面", "從 Comfy 提示詞到 Kling O3")
story += [p("導演用高階語言交代創意，Agent 讀懂既有工作流、重組提示詞、準備參考圖、操作 MCP，最後把有效方法保存成 Skill。")]
img1 = fit_image(ROOT / "assets" / "o3-character-source.jpg", 50*mm, 72*mm)
img2 = fit_image(ROOT / "assets" / "o3-shot-001-reference.png", 120*mm, 67.5*mm)
hero = Table([[img1, img2]], colWidths=[52*mm, 122*mm]); hero.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 2)]))
story += [hero, Spacer(1, 5*mm), box([p("課程主軸", "H3TC"), p("Comfy、ChatGPT Image Generation、Kling O3 與提示詞是示範工具；真正要學的是如何引導 Agent 研究、提案、執行、驗收並留下可重跑紀錄。")], PALE), PageBreak()]

story += head("02｜Agent 與工具", "先分清楚模型、介面、工作流與工具連線")
story += [box([p("Agent 是什麼？", "H3TC"), p("Agent 是帶著目標與規則，能讀取專案資料、使用工具、等待必要決定並檢查成果的人工智慧代理執行者。")], CYAN), grid([["層次","本課例子","用途"],["模型","Gemini、OpenAI 模型、Kling O3","理解、推理或生成內容"],["工作介面","Antigravity、ChatGPT、Codex","放入資料、交代任務、使用工具"],["節點工作流","ComfyUI","把模型、條件、取樣與輸出接成流程"],["工具連線","MCP","把 Kling 等服務接成 Agent 工具"],["可重用規則","AGENTS.md、Skill","保存工作方法、確認點與驗收標準"]],[34*mm,62*mm,78*mm]), Spacer(1,3*mm), grid([["導演負責","Agent 負責"],["創意、取捨、權限與最終驗收。","研究、轉譯、執行、紀錄與回報。"]],[87*mm,87*mm]), PageBreak()]

story += head("03｜為什麼使用 Agent", "一般網頁對話適合回答，Agent 適合完成跨步驟專案")
story += [grid([["一般網頁對話","Agent 工作模式"],["適合解釋概念、改寫文字、發想選項與一次性問答。回答之後，資料搬移、工具操作、進度紀錄與結果檢查由使用者接手。","持續讀取同一個專案，查找可信資料、修改檔案、操作工具、等待核准、追蹤任務並驗收結果。"]],[87*mm,87*mm],7.0),
          box(p("讀專案 → 查證與提案 → 等待核准 → 使用工具 → 驗收與保存", "H3TC"), CYAN),
          grid([["一般網頁對話已足夠","應改用 Agent"],["問題能一次回答；不必讀整個專案；不需操作外部工具；結果由人自行執行與保存。","任務要多步驟推進；必須讀檔與查來源；要修改檔案或操作 MCP；需要核准點、驗收與可重跑紀錄。"]],[87*mm,87*mm],6.8),
          box([p("差別在工作方式，不在產品名稱", "H3TC"), p("ChatGPT 接上專案資料、規則與工具時，也能以 Agent 方式工作。判斷重點是它能不能持續完成任務，並留下下一步可檢查的證據。")], PALE),
          p("七章學習路線", "H3TC")]
story += [grid([["章節","學習任務","交給下一章的成果"],["01","建立共同語言","分清楚 Agent、工作介面、影片模型、提示詞與工具"],["02","選擇工作模式","判斷一般網頁對話何時足夠，何時需要 Agent"],["03","拆學員問題","定位需求、素材、方法、工具或驗收缺口"],["04","先看完整工作流","說出高階創意如何走到核准、執行、驗收與保存"],["05","追查方法來源","從原始對話與 Comfy 找到提示詞基準和決策證據"],["06","轉譯並完成任務","參考圖、Kling 輸入、MCP 任務紀錄與成片驗收"],["07","轉移並保存","商品影片方法與可重跑的 Skill"]],[23*mm,48*mm,103*mm],6.2), p("分享案例時的六個問題", "H3TC")]
for line in ["原本真正想完成什麼？","Agent 當時能讀到哪些素材與規則？","Agent 自行補了哪些決定？","實際結果和期待差在哪裡？","當時只修成品，還是也修正工作規則？","留下了哪些可驗收、重跑與追蹤的紀錄？"]: story.append(p("•　" + line))
story += [PageBreak()]

story += head("04｜影片模型與 Agent 模型", "先分清楚生成器與代理執行者，再用對的方法比較")
story += [box([p("這裡有兩種『模型』", "H3TC"), p("影片生成模型把文字、圖片或影片參考轉成影片；Agent 使用的語言模型負責讀專案、查資料、寫模型專用提示詞並操作工具。兩者不能混成同一張排行榜。")], CYAN),
          p("官方文件支持到哪裡", "H3TC"),
          grid([["影片模型","文件支持的輸入結構","證據性質"],["Kling 3.0／Omni","主體＋動作＋場景＋選用攝影／光線／氣氛","官方提示指南"],["Veo 3.1","主體＋動作＋風格＋攝影／構圖／鏡頭／氣氛","官方提示指南"],["Runway Gen-4.5","圖片負責外觀；文字集中描述動作與時間進程","官方提示指南"],["Seedance 2.5","時間區段、鏡位、動作、節奏、多模態參考","官方產品說明"],["Wan 2.2／ComfyUI","擴寫、負面提示、取樣參數；節點另屬工作流","官方程式庫＋專案策略"]],[39*mm,84*mm,51*mm],5.8),
          box([p("教學推論", "H3TC"), p("固定創意意圖、素材、片長、畫幅與驗收標準，再依各模型的輸入責任改寫。這是公平測試設計，不代表某種句型必然得到較好的作品。")], PALE),
          p("Agent／語言模型另外比較", "H3TC"),
          grid([["能力","共同評分"],["讀脈絡與查證","先讀規則、素材、紀錄；提供官方來源與日期"],["提案與執行","交付中文意圖、模型專用提示詞、素材責任、參數、核准點與驗收表"]],[45*mm,129*mm],6.4),
          box(p("請讀取這個 Kling O3 專案，先交付方案與送片摘要，不要直接執行付費生成。", "BodyTC"), PALE),
          p("官方資料（2026-10-12 查閱）：Kling、Veo、Runway、Seedance 與 Wan；完整網址見 HTML 講義與 VIDEO_MODEL_GUIDE.md。", "SmallTC"), PageBreak()]

story += head("05｜完成版工作流", "先看 Agent 如何完成整支影片，再回頭拆對話")
story += [box([p("導演先給 Agent 的基準", "H3TC"), p("指定 Kling O3，提供從 Comfy 帶來的提示詞範本、角色或商品素材、鏡頭創意、限制與完成標準。")], CYAN),
          grid([["步驟","Agent 的工作與交付"],
                ["1｜讀取脈絡","讀 AGENTS.md、Skill、專案素材、既有紀錄與目前工具。"],
                ["2｜查證方法","以官方文件與 MCP 回傳確認模型、輸入、參數與限制。"],
                ["3｜提出方案","交付中文意圖、兩種提示詞、素材責任、參數與驗收表。"],
                ["4｜核准參考圖","導演確認角色或商品、姿態、鏡位、構圖、色彩與光線。"],
                ["5｜完成參考圖","ChatGPT 產生正式第一幀；Agent 整理完整送片摘要。"],
                ["6｜核准付費送片","導演確認圖片、提示詞、模型、規格、音訊、版本與提交次數。"],
                ["7｜Kling MCP 執行","上傳素材並只提交一次，保存 generationId 與 taskTraceId。"],
                ["8｜追蹤與驗收","只查同一任務；完成後逐項檢查，下一版只改一個主要變因。"],
                ["9｜保存方法","本次素材與紀錄留在 Project；已驗證方法寫入 Skill。"]],[39*mm,135*mm],7.1),
          grid([["人要決定的兩個位置","Agent 每次要交付的證據"],["參考圖是否通過；是否允許付費提交影片。","來源、方案、參數、任務編號、成品與逐項驗收結果。"]],[87*mm,87*mm],7),
          p("先分清楚三種文字", "H3TC"),
          grid([["導演 → Agent","專案 → Agent","Agent → 模型"],
                ["高階指令：說清楚想完成什麼、素材、限制、核准點與完成標準。","AGENTS.md／Skill：保存可重跑的步驟、工具分工與驗收規則。","提示詞與參數：依目前模型的輸入方式，整理本次可執行資料。"]],[58*mm,58*mm,58*mm],6.8),
          box([p("如何判斷流程真的成立", "H3TC"), p("每一步都要留下下一個人能檢查的交付物；工具顯示 COMPLETED 只代表執行結束，作品是否符合創意與品牌標準仍由導演驗收。")], PALE), PageBreak()]

story += head("06｜完整對話脈絡", "從建立分工、犯錯、更正到正式送片")
story += [grid([["回合","導演原話／事件","Agent 可見回覆與結果","工作流意義"],["1","建立新工作流；指定 Kling O3；我擔任導演","六步流程；16:9、5 秒、1080p、單版、單鏡頭、音效開啟；付費前核准","先定角色、工具、核准權與失敗邊界"],["2","提供從 Comfy 帶來的完整提示詞範本","拆出景別、主體、動作、環境、物理、焦點、色光與情緒順序","描述基準由導演提供；Agent 分析轉譯"],["3","角色附件；蹲下抬頭；廣角看他","補低機位、20mm 感、場景、光線、動態與兩份提示詞草案","短創意成為可見、可修改方案"],["4","核准","歷史上誤用 Kling Image：2 點、COMPLETED，保存 generationId","核准後仍可能因工具責任不清而做錯"],["5","圖片是由 CHAT GPT 生成","改由 ChatGPT 生正式圖；Kling 只生影片；舊圖留作歷史","修成品，也修規則與版本狀態"],["6","ChatGPT 正式參考圖完成","送片前重列兩張圖、5 秒、16:9、1080p、1 版、多鏡頭關閉、音訊開啟","把輸入、參數與費用邊界做成摘要"],["7","生成第一段影片","提交一次；60 點；保存 generationId、taskTraceId；只查同一任務","短指令成立，因為前面已有完整邊界"],["8","QUEUING → RUNNING → COMPLETED","交付影片、封面、完成時間與連結失效提醒","工具完成後仍需內容驗收"],["9","把我們的對話變成 TXT","整理可見對話、提示詞、核准點與結果","工作流留下可追溯專案紀錄"]],[11*mm,42*mm,69*mm,52*mm],6.15), box([p("兩個實際任務編號", "H3TC"),p("歷史圖片：AepElq…hPgN　｜　正式影片：AR3Cf4…clsi")], PALE), box([p("從對話形成的規則", "H3TC"),p("ChatGPT 生正式參考圖；Kling 只生影片；付費前交摘要；等待時不重複提交；舊版本保留。")], CYAN), p("完整整理：ORIGINAL_DIALOGUE_TEACHING.md　原始紀錄：sources/Kling_O3_對話紀錄_2026-10-11.txt", "SmallTC"), PageBreak()]

story += head("07｜Comfy 提示詞來源", "這段示範提示詞是從既有 Comfy 工作流帶過來的")
story += [box(p(escape(COMFY_PROMPT), "CodePrompt"), colors.HexColor("#f3f5f7")), grid([["段落","作用"],["Wide shot…running toward the camera","景別、主體與主要動作"],["white birds…hair and dress…wind","環境與次要動態"],["crisp focus…motion blur","焦點與允許模糊的位置"],["Vivid colors…cinematic tone","色彩、光線與情緒收束"]],[72*mm,102*mm]), box([p("必須講清楚", "H3TC"),p("這不是 Kling 官方提示詞範本。可沿用的是創意意圖與描述順序；搬到新模型時，仍須重新決定文字、參考圖與參數各自負責什麼。")], CYAN), PageBreak()]

story += head("08｜認識 Comfy", "提示詞只是節點工作流中的一項輸入")
story += [box(p("模型 ＋ 提示詞／文字編碼 ＋ 參考控制 → 取樣 → 解碼 → 輸出", "H3TC"), PALE), grid([["角色","白話解釋","學員要看懂"],["模型載入","選擇生成核心","換模型會改變節點與提示詞需求"],["文字編碼","提示詞轉成條件資料","編碼器要與模型相容"],["參考控制","圖片、姿勢、深度、LoRA","部分要求已由節點負責"],["取樣","依模型與條件形成結果","種子、步數、引導、排程與降噪影響輸出"],["潛在資料","生成中的壓縮表示","過程不一定是可觀看像素"],["VAE／解碼器","把潛在資料轉成圖片","解碼後才得到可觀看內容"]],[34*mm,60*mm,80*mm],6.9), box([p("搬移前先問", "H3TC"),p("原工作流用了哪些參考圖、ControlNet、LoRA、種子與取樣參數？哪些視覺結果其實不是由提示詞單獨控制？")], CYAN), box([p("初學者先回答三題", "H3TC"), p("這次由哪個模型生成？哪些條件不是寫在提示詞裡？結果在哪一步才變成可觀看的圖片？")], PALE), PageBreak()]

story += head("08｜高階指令與三層語言", "導演說創意，Agent 補成可檢查方案")
pic = fit_image(ROOT / "assets" / "o3-character-source.jpg", 45*mm, 67*mm)
copy = [p("「我想要這個角色風格，讓他蹲下抬頭，鏡頭使用廣角鏡頭看他。」", "H3TC"), p("<b>導演已決定：</b>角色來源、蹲姿、抬頭與廣角視覺。"), p("<b>Agent 提案：</b>低機位、20mm 感、夜間場景、直閃、焦點、次要動態、鏡頭速度與結尾。")]
t = Table([[pic, copy]], colWidths=[49*mm,125*mm]); t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP")]))
story += [t, grid([["層次","保存內容"],["導演 → Agent","成果、素材、限制、核准點與驗收方式"],["專案 → Agent","AGENTS.md／Skill 中的可重用規則"],["Agent → 模型","依目前模型整理的提示詞、參考圖角色與參數"]],[43*mm,131*mm]), box([p("原則", "H3TC"),p("Agent 補的是可供導演核准的提案，不是偷偷替導演決定創意。")], CYAN), PageBreak()]

story += head("09｜ChatGPT 參考圖", "第一個核准點：先鎖定第一幀能看見的事")
a = fit_image(ROOT / "assets" / "o3-character-source.jpg", 36*mm, 50*mm); b = fit_image(ROOT / "assets" / "o3-shot-001-reference.png", 89*mm, 50*mm)
imgs = Table([[a,b]], colWidths=[39*mm,92*mm], hAlign="CENTER"); imgs.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
story += [imgs, grid([["素材","責任"],["原始角色圖","角色身分、臉部、髮型、服裝與配件"],["ChatGPT 正式參考圖","蹲姿、低機位、廣角透視、構圖、場景、色彩與光線"]],[49*mm,125*mm]), p("完整參考圖提示詞", "H3TC"), box(p(escape(IMAGE_PROMPT), "CodeTC"), colors.HexColor("#f3f5f7")), p("中文脈絡：先指定附件負責角色，再描述一個靜止瞬間；接著鎖定姿態、鏡位、透視、焦點、光線與情緒。長時間事件留到影片階段。", "SmallTC"), PageBreak()]

story += head("09｜Kling O3 影片提示詞", "實作後精鍊成三句，每句只負責一件事")
story += [box(p(escape(VIDEO_PROMPT), "CodeTC"), colors.HexColor("#f3f5f7")), grid([["句子","這一句的責任"],["第一句｜鏡頭與事件","鏡位開場；交代圖片1角色、圖片2姿態；一個主要動作與一個環境事件。"],["第二句｜物理與攝影","自然物理反應、臉部清晰、受控邊緣模糊與一次慢速前推。"],["第三句｜視覺與情緒","直閃、深石墨色與三個同方向的情緒詞收尾。"]],[49*mm,125*mm],6.8), box([p("這是精鍊後的專案準則", "H3TC"),p("三句通常為 55—100 個英文單字，讀起來像一個電影瞬間。這不是 Kling 官方固定語法，仍須用成片驗證。")], PALE), p("完整準則：sources/KLING_O3_PROMPT_GUIDELINES.md", "SmallTC"), PageBreak()]

story += head("10｜修正、核准與 MCP", "把一次糾正變成後續規則")
story += [grid([["歷史版本","更正後"],["Kling Image O3 曾完成參考圖，但不符合導演指定分工。","正式參考圖由 ChatGPT Image Generation 產生；Kling 只負責影片。"]],[87*mm,87*mm]), p("兩個核准點", "H3TC"), p("1. <b>參考圖核准：</b>確認角色、姿態、鏡位、構圖與視覺方向。"), p("2. <b>影片提交核准：</b>確認圖片、提示詞、模型、片長、比例、解析度、音訊、版本數與允許提交次數。"), p("Kling MCP 工具鏈", "H3TC"), box(p("who_am_i → file_upload → image_to_video → generationId → query_tasks", "H3TC"), CYAN), p("學員不必先寫 MCP 程式：先會確認登入與模型、看懂提交參數、保存 generationId，並只查詢同一筆任務。", "SmallTC"), box([p("本次歷史紀錄", "H3TC"),p("5 秒、16:9、1080p、1 版；多鏡頭關閉、同步音訊開啟；QUEUING → RUNNING → COMPLETED。點數與模型能力只代表 2026 年 10 月 11 日這次執行。")], PALE), PageBreak()]

story += head("10｜MODEL 成片驗收", "工具顯示完成，作品仍要由導演判斷")
model_poster = fit_image(ROOT / "assets" / "shot-001-kling-o3-poster.jpg", 96*mm, 54*mm)
model_poster_notes = [
    p("<b>SHOT-001｜Kling O3 人物成片</b>", "SmallTC"),
    p("5 秒｜16:9｜1080p", "SmallTC"),
    p("HTML 講義可直接播放；紙本與 PDF 顯示同一支影片的代表畫面。", "SmallTC"),
]
model_poster_table = Table([[model_poster, model_poster_notes]], colWidths=[101*mm, 73*mm])
model_poster_table.setStyle(TableStyle([("BOX",(0,0),(-1,-1),.4,LINE),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
story += [model_poster_table, grid([["SHOT-001 驗收","可觀察標準"],["人物一致性","臉、髮型、灰色服裝、身形與配件保持"],["表演與鏡頭","低頭到抬頭清楚；低機位、廣角透視與一次平順前推成立"],["物理與結尾","頭髮、衣料、銀飾自然；最後一秒臉部與構圖仍可使用"]],[50*mm,124*mm],6.5), box([p("單一變因修改示範", "H3TC"),p("保留人物、服裝、場景、光線與抬頭動作；只把攝影機前推速度降低一半。通過條件是人物比例穩定，最後一秒臉部仍清楚。")], PALE), PageBreak()]

story += head("11｜商品案例", "SHOT-002：從兩張參考圖到商品英雄水幕")
story += [p("<b>商品：</b>Schwarzkopf Professional BC Bonacure Repair Rescue Shampoo（極緻修護髮露）。", "SmallTC")]
tail_img = fit_image(ROOT / "assets" / "shot-002-product-tail.png", 35*mm, 62.2*mm)
opening_img = fit_image(ROOT / "assets" / "shot-002-product-opening.png", 35*mm, 62.2*mm)
asset_table = Table([[
    [tail_img, p("<b>圖片 1｜結尾英雄畫面</b><br/>商品身分、標籤、材質、色光與完整水幕。", "SmallTC")],
    [opening_img, p("<b>圖片 2｜ChatGPT 開場構圖</b><br/>9:16 開場、低水位、平靜畫面與起始位置。", "SmallTC")]
]], colWidths=[87*mm, 87*mm])
asset_table.setStyle(TableStyle([("BOX",(0,0),(-1,-1),.4,LINE),("INNERGRID",(0,0),(-1,-1),.4,LINE),("VALIGN",(0,0),(-1,-1),"TOP"),("ALIGN",(0,0),(-1,-1),"CENTER"),("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
contact_img = fit_image(ROOT / "assets" / "shot-002-product-video-contact.jpg", 96*mm, 54*mm)
result_notes = [p("<b>實際 Kling O3 成片</b>", "SmallTC"), p("5 秒｜9:16｜1080p｜24 fps<br/>單鏡頭｜同步音訊開啟<br/>狀態：COMPLETED", "SmallTC"), p("水由低水位升成透明水幕；攝影機緩慢前推並輕微上移。", "SmallTC")]
result_table = Table([[contact_img, result_notes]], colWidths=[101*mm,73*mm])
result_table.setStyle(TableStyle([("BOX",(0,0),(-1,-1),.4,LINE),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
story += [asset_table,
          p("三種輸入責任", "H3TC"),
          grid([["輸入","交給它的責任"],["圖片 1","商品身分、瓶身比例、桃紅壓頭、標籤、材質與最後英雄構圖"],["圖片 2","較平靜的開場、較低水位、9:16 畫幅與商品起始位置"],["提示詞","水幕上升、一次前推與輕微上移、商品穩定規則、聲音與情緒"]],[35*mm,139*mm],6.4),
          p("成片證據", "H3TC"), result_table,
          p("驗收表", "H3TC"),
          grid([["面向","可觀察標準"],["商品保真","白瓶、桃紅壓頭、比例、品牌標誌與標籤跨影格保持穩定"],["環境動態","水由低到高自然聚集，水幕支援商品且未遮住標籤"],["攝影機","只做一次緩慢前推與輕微上移，沒有突然縮放或多餘繞行"],["結尾與聲音","結尾接近圖片 1；水聲自然且不搶主體"]],[35*mm,139*mm],6.2),
          p("模型 kling-video-v3_0_omni 與上述能力是 2026 年 10 月 11 日的單次紀錄；授課前仍由 MCP 即時確認。", "SmallTC"), PageBreak()]

story += head("12｜Gemini Veo 商品案例", "先看成片，再看首幀與六格故事版如何分工")
veo_results = fit_image(ROOT / "assets" / "jagua-veo-results-contact.jpg", 174*mm, 95*mm)
veo_first = fit_image(ROOT / "assets" / "jagua-veo-first-frame.jpg", 43*mm, 76*mm)
veo_storyboard = fit_image(ROOT / "assets" / "jagua-veo-workflow-a-storyboard.webp", 123*mm, 76*mm)
veo_inputs = Table([[
    [veo_first, p("<b>圖片 1｜首幀母幀</b><br/>固定瓶型、標籤、材質、色調與光影。", "SmallTC")],
    [veo_storyboard, p("<b>圖片 2｜Workflow A 六格故事版</b><br/>微距 → 精華滴落 → 側向水花 → 泡沫 → 斜向沖洗 → 瓶肩與瓶蓋收尾。", "SmallTC")]
]], colWidths=[48*mm,126*mm])
veo_inputs.setStyle(TableStyle([("BOX",(0,0),(-1,-1),.4,LINE),("INNERGRID",(0,0),(-1,-1),.4,LINE),("VALIGN",(0,0),(-1,-1),"TOP"),("ALIGN",(0,0),(-1,-1),"CENTER"),("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
story += [box([p("模型來源提醒", "H3TC"), p("三支 Jagua Blue Radiance 商品影片是本專案以 Gemini Veo 產生的實際結果。海灘情境是獨立段落；商品與水、商品微距對應 Workflow A。")], CYAN), veo_results, p("三段結果：海灘情境｜商品與水｜商品微距", "SmallTC"), veo_inputs, grid([["素材","交給 Veo 的責任"],["圖片 1","商品外觀、標籤、材質、深海藍色調與水波折射光"],["圖片 2","六段動作的順序與構圖；黑白線稿、格線不得進入成片"],["提示詞","分配兩張圖的責任，再補上運鏡、時間線與禁止事項"]],[35*mm,139*mm],6.4), PageBreak()]

story += head("13｜Gemini Veo 實際提示詞", "Workflow A v5.0：原文與中文閱讀方法")
veo_prompt_text = escape(VEO_PRODUCT_PROMPT).replace("\n", "<br/>")
story += [grid([["先看素材責任","再看時間結構"],["Image 1 是外觀與光影的唯一依據；Image 2 只提供動作順序。","Camera Movement 說明整體剪接；VFX Timeline 逐格指定水花、泡沫、沖洗與收尾。"]],[87*mm,87*mm],6.7), box(p(veo_prompt_text, "CodeVeo"), colors.HexColor("#f3f5f7")), p("完整文字檔：assets/jagua-veo-workflow-a-prompt.txt。專案紀錄版本為 Workflow A v5.0，更新日期 2026-09-02；原文同時寫有 Veo／Omni，本案例成片依專案紀錄標示為 Gemini Veo。", "SmallTC"), PageBreak()]

story += head("14｜保存與來源", "把方法保存成 Skill，把本次素材留在 Project")
story += [grid([["Project 保存","Skill 保存"],["角色、圖片、提示詞、參數、generationId、taskTraceId、成本、結果與導演回饋。","讀脈絡、找可信資料、提出方案、核准、MCP、追蹤、驗收與失敗處理。"]],[87*mm,87*mm]), p("課前確認", "H3TC")]
for line in ["實際 Comfy 工作流、模型與節點可開啟。","原始角色圖、ChatGPT 定稿圖與完成影片已有本機備份。","Kling MCP 已連線，並確認模型、參數、素材上限與帳號能力。","模型名稱、點數與介面位置重新查證，不沿用歷史數值。"]: story.append(p("•　" + line))
story += [p("官方資料", "H3TC"), p("OpenAI 模型選擇　https://learn.chatgpt.com/docs/model-selection<br/>Antigravity 官方概覽　https://www.antigravity.google/docs/overview<br/>Gemini 模型文件　https://ai.google.dev/gemini-api/docs/models<br/>ComfyUI 核心概念　https://docs.comfy.org/essentials/core-concepts/links<br/>CLIP Text Encode　https://docs.comfy.org/built-in-nodes/ClipTextEncode<br/>KSampler　https://docs.comfy.org/built-in-nodes/KSampler<br/>VAE Decode　https://docs.comfy.org/built-in-nodes/VAEDecode<br/>Kling 圖片生成影片　https://kling.ai/quickstart/image-to-video-guide", "SmallTC"), box([p("最後的學習成果", "H3TC"), p("換一個角色、商品或模型後，學員能用高階語言讓 Agent 重新研究、提出方案、執行、驗收並留下可重跑的工作流。")], CYAN)]
story += [p("交給 Agent 的重跑指令", "H3TC"), box(p("請使用 Kling O3 導演工作流處理這個鏡頭。先讀專案規則、既有鏡頭紀錄與參考素材；交付中文意圖摘要、ChatGPT 參考圖提示詞、Kling O3 影片提示詞、每張素材的用途、生成參數與驗收表。參考圖核准後才能進入送片準備；付費影片提交前再次提供完整摘要並等待核准。提交後只追蹤同一個 generationId。完成後逐項驗收，每次只改一個主要變因，並把紀錄留在本次 Project。", "SmallTC"), colors.HexColor("#f3f5f7")), p("失敗與等待怎麼處理", "H3TC"), grid([["狀況","Agent 的處理"],["參考圖未通過","只修改參考圖方案，不進入 Kling 付費提交。"],["QUEUING／RUNNING","查詢同一個 generationId，不重複提交。"],["FAILED／CANCELLED","回報原因與原參數，等待導演決定。"],["完成但偏離目標","指出一個主要偏差，下一版只改一項。"],["成果網址可能失效","把核准成品保存到 Project。"]],[46*mm,128*mm],6.9)]

# Merge related short conceptual pages while retaining every section and both full prompts.
merged_story = []
break_number = 0
for item in story:
    if isinstance(item, PageBreak):
        if break_number in {7, 9, 11}:
            merged_story.append(Spacer(1, 4*mm))
        else:
            merged_story.append(item)
        break_number += 1
    else:
        merged_story.append(item)

doc = SimpleDocTemplate(str(PDF_OUT), pagesize=A4, leftMargin=17*mm, rightMargin=17*mm, topMargin=13*mm, bottomMargin=18*mm, title="第二堂紙本講義｜從 Comfy 提示詞到 Kling O3", author="")
doc.build(merged_story, onFirstPage=footer, onLaterPages=footer)
print(f"Wrote {HTML_OUT}")
print(f"Wrote {PDF_OUT}")

