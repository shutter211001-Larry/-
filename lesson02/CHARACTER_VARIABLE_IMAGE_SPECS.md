# 人物差異預測圖：生成規格

更新日期：2026 年 10 月 11 日  
生成方式：Codex 內建 `imagegen`  
共同參考圖：`assets/o3-character-source.jpg`、`assets/o3-shot-001-reference.png`

## 教學定位

五組圖固定人物身分、灰色服裝、針織帽、蹲姿、黑色包包與石造街景，只改一類變因。圖片用來協助學員預測風險及建立驗收表，不代表 Kling 必然產生相同結果。實際結論必須在目標模型中以相同素材與參數測試。

共同限制：保留可辨識臉部、中性氣質、服裝與場景；圖內不放 A／B／C、說明文字、箭頭或浮水印；不新增人物與無關道具。

## 1. 景別與角度

輸出：`assets/character-variable-shot-angle.png`

```text
Create a clean horizontal triptych showing the same character in the same crouched pose and nighttime stone street, with only shot size and camera angle changing.
Panel A: eye-level medium-wide shot; the whole crouched body and more environment are visible.
Panel B: very low-angle wide shot from pavement level with a close 20mm perspective; foreground shoes and knees are slightly enlarged and the architecture stretches upward.
Panel C: tight facial close-up from a slightly low angle; face and eyes dominate while the full pose and environment become unreadable.
Keep the same person, wardrobe, pose, bag location, stone facade, lighting direction and color grade.
```

## 2. 環境動態

輸出：`assets/character-variable-environment-motion.png`

```text
Create a clean horizontal triptych showing the exact same character, pose, framing, camera angle, lighting and street scene, with only the amount of environmental motion changing.
Panel A: completely still scene; hair, knitwear, belt charms and surrounding air are motionless.
Panel B: one controlled light night breeze; only a few hair strands, the sweater hem and silver belt charms move subtly while the face remains clear.
Panel C: excessive competing events—strong wind, whipping hair and fabric, flying dry leaves, loose paper, dense mist and rain streaks—visibly clutter the frame and obscure the character.
```

## 3. 焦點與動態模糊

輸出：`assets/character-variable-focus-blur.png`

```text
Create a clean horizontal triptych teaching focus target and controlled motion blur while every other condition remains fixed. The character begins to lift their chin slightly in all three panels.
Panel A: everything is frozen and tack sharp, including face, hair, clothing, charms, bag and background.
Panel B: eyes and face remain crisp; only a few moving hair strands, swinging silver charms and the closest foreground edge have light directional motion blur.
Panel C: excessive global motion blur affects face, eyes, body, clothing and architecture, making identity and expression difficult to read.
```

## 4. 主要運鏡

輸出：`assets/character-variable-camera-movement.png`

```text
Create a three-column comparison board showing three predicted camera movements around the exact same crouched character. Each column contains three sequential keyframes stacked vertically: start, middle and end.
Column A: slow centered push-in from a medium-wide low-angle view to a closer low-angle view; direction and horizon stay stable.
Column B: lateral tracking from left to right; character scale stays nearly constant while the stone facade and window parallax shift sideways.
Column C: gentle orbit from frontal low-angle to a three-quarter side view; camera distance stays nearly constant and the character remains crouched.
Keep the same identity, pose, beanie, charcoal clothing, belt charms and black bag in all nine frames.
```

## 5. 色彩、光線與情緒

輸出：`assets/character-variable-color-mood.png`

```text
Create a clean horizontal triptych showing the exact same character, pose, camera angle, framing, outfit, bag and architecture, with only color, lighting and emotional tone changing.
Panel A: soft cool dawn light with clear cyan ambience and gentle fill; airy, calm and approachable.
Panel B: hard direct on-camera flash, warm window practicals and deep graphite shadows; tense, intimate and rebellious.
Panel C: saturated electric-blue and hot-magenta studio-like spill across the same stone street with glossy highlights; energetic premium fashion campaign.
```

## 課堂判讀

1. 先描述畫面中真的改變了什麼。
2. 再寫出對人物身分、表演、服裝和場景連續性的預測。
3. 把預測改寫成可觀察的驗收條件。
4. 到目標模型實測後，才決定能否保存成 Skill 規則。
