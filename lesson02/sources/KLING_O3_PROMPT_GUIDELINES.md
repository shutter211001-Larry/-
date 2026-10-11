# 導演指定提示詞風格準則

## 唯一風格母版

> Wide shot of a free-spirited young woman running toward the camera through a sun-drenched field, white birds exploding upward all around her like symbols of freedom. Her hair and dress are caught by the wind, captured with crisp focus on her face and light motion blur in the foreground flowers and wings. Vivid colors, bright clear sky, optimistic, uplifting cinematic tone.

往後的正式提示詞必須延續這段文字的節奏、密度與攝影語言。它不是關鍵字清單，也不是技術規格書，而是一個能直接被看見的電影瞬間。

## 風格分析

這段母版只有三句，每句負責一件事：

1. **第一句建立畫面**：景別＋主體＋主要動作＋移動方向＋具體環境＋一個有感染力的次要動態。
2. **第二句建立攝影感**：頭髮、服裝、液體、粒子或其他元素的物理反應＋清晰焦點＋受控制的動態模糊。
3. **第三句建立情緒**：色彩＋光線或天候＋二至三個一致的電影情緒詞。

它的力量來自具體動詞與可視化名詞，例如 `running toward the camera`、`birds exploding upward`、`hair and dress caught by the wind`。情緒不是抽象解說，而是由動作、環境和攝影共同產生，最後才用短句命名。

## 固定三句式

### 第一句：鏡頭與事件

```text
[Shot size and angle] of [specific subject] [one principal action] [direction or spatial relationship] through/in [specific environment], [one vivid secondary event] [optional short visual metaphor].
```

必須包含：

- 景別或角度放在最前面，例如 `Wide shot`、`Low-angle wide shot`、`Close-up`。
- 一個清楚主體，不用空泛的 `a person` 或 `a product`。
- 一個主要動作，並說明朝哪裡、穿過什麼或與鏡頭的關係。
- 一個能放大情緒的環境動態，例如鳥群、水花、風、花瓣、煙塵或反光。
- 視覺比喻最多一個，而且必須短，例如 `like symbols of freedom`。

### 第二句：物理反應與攝影

```text
[Hair, fabric, water, reflections or particles] [physical response], captured with [crisp focus target] and [controlled blur, depth or foreground treatment].
```

必須包含：

- 至少一個會自然回應主動作的元素。
- 明確指出觀眾應看清楚什麼。
- 動態模糊只放在運動中的前景、邊緣或次要元素，不模糊核心主體。
- 商品鏡頭可把這句改成「商品保持清晰不變，水、光或反射產生動態」。

### 第三句：視覺與情緒收尾

```text
[Color quality], [lighting, sky or atmosphere], [two or three compatible emotional adjectives] cinematic tone.
```

規則：

- 使用短促、有節奏的片語。
- 色彩與光線各寫一次即可。
- 情緒詞彼此必須同方向，例如 `optimistic, uplifting` 或 `tense, intimate, rebellious`。
- 結尾固定落在 `cinematic tone` 或適合商品的 `premium cinematic commercial tone`。

## 精鍊準則

1. 最終提示詞以三句為主，通常控制在 55–100 個英文單字。
2. 每鏡只寫一個主要動作；其他動態都是它的自然反應。
3. 每鏡只寫一個主要運鏡，直接嵌入第二句，不另寫攝影教科書。
4. 使用具體動詞取代抽象形容詞，例如用 `rises`、`sweeps`、`drifts`、`bursts`，少用 `beautiful`、`amazing`、`dynamic`。
5. 優先寫能被看見的內容，不解釋故事背景或創作意圖。
6. 不重複同一資訊；主體、色彩、光線與情緒各出現一次即可。
7. 不寫關鍵字串、標籤式欄位、括號補充或冗長禁止清單。
8. 一致性要求要融入自然句子，例如 `keeping the bottle and label crisp, stable, and unchanged`。
9. `圖片1`、`圖片2` 的角色在第一句直接說清楚，不另附技術說明。
10. 聲音若必要，只加入第三句的一個短片語，例如 `with soft rushing water and delicate droplets`。

## Kling O3 參考圖寫法

使用多張參考圖時仍維持三句式：

- `圖片1` 通常鎖定角色、服裝、商品、包裝或其他不可改變的身分。
- `圖片2` 通常鎖定導演核准的姿態、構圖或開場狀態。
- 兩張圖的職責在第一句自然交代，不寫成素材說明表。

第一句推薦句型：

```text
[Shot] of the exact [subject] from 圖片1 [action] in the [pose, composition or opening state] established in 圖片2, [vivid environmental event].
```

## 人物鏡頭範例

```text
Low-angle wide shot of the androgynous fashion figure from 圖片1 crouching on a nighttime stone pavement in the pose established by 圖片2, slowly lifting their chin toward the lens as the old facade stretches above them. Their shaggy hair, loose knit layers, and silver belt charms shift lightly in the breeze, captured with crisp focus on the face and gentle motion blur at the edges of the wide trousers during one slow push forward. Hard direct flash, deep graphite tones, tense, intimate, rebellious cinematic tone.
```

這個版本沿用母版的節奏：第一句是人物與事件，第二句是物理反應與攝影，第三句是視覺情緒。

## 商品鏡頭範例

```text
Low-angle wide shot of the exact Schwarzkopf Professional BC Bonacure Repair Rescue Shampoo bottle from 圖片1 standing on the glossy hot-magenta pedestal in the calm opening composition of 圖片2, a crystalline wave rising behind it in a clean arc. Clear water and suspended droplets sweep upward as the camera slowly pushes closer, captured with crisp focus on the unchanged bottle, magenta pump, brand mark, and label and light motion blur in the outer spray. Electric blue and hot magenta, polished studio highlights, pristine, energetic, premium cinematic commercial tone.
```

這個版本不把商品規格逐項列出，而是用與母版相同的三句節奏，把商品穩定性自然放進第二句。

## 快速檢查

交付提示詞前只檢查以下七點：

- 是否以景別或鏡頭角度開場？
- 第一個句子是否立刻看得到主體與主要動作？
- 是否只有一個強烈、可讀的環境動態？
- 第二句是否包含物理反應、清晰焦點與受控模糊？
- 是否只有一個主要運鏡？
- 第三句是否用色彩、光線與一致情緒俐落收尾？
- 整段是否讀起來像電影畫面，而不是提示詞工程文件？

