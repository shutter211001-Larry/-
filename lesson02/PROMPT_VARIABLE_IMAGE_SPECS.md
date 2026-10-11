# 提示詞單一變因圖：生成規格

更新日期：2026 年 10 月 11 日  
生成方式：Codex 內建 `imagegen`  
共同參考圖：`assets/shot-002-product-tail.png`

## 教學目的

五組圖都使用同一個產品母幀作身分與材質參考。每一組固定產品、基本場景與未被測試的條件，只修改一類變因。圖內不生成教學文字；A／B／C 的中文說明由簡報與講義排版負責。

這些圖片是教學示意，用來練習控制變因與觀察差異。它們不是 Kling 固定行為的證據。若要把結論寫入 Skill，仍須在目標模型中使用相同素材、參數與測試方式驗證。

## 1. 景別與角度

輸出：`assets/prompt-variable-shot-angle.png`

```text
Use case: scientific-educational
Asset type: landscape comparison plate for a Traditional Chinese classroom slide
Input image: the attached product image is the identity and material reference. Preserve the same tall white rectangular Schwarzkopf Professional BC Bonacure Repair Rescue Shampoo bottle, hot-magenta pump, printed label layout, opaque packaging material, glossy hot-magenta sculptural pedestal, and electric-blue studio background in every panel.
Primary request: create a clean three-panel horizontal triptych that teaches how shot size and camera angle change product expression while every other condition stays fixed.
Panel A: eye-level wide shot, the full bottle appears small with ample environment.
Panel B: low-angle wide shot from near the pedestal, the full bottle feels taller and more imposing.
Panel C: macro close-up of the bottle shoulder, cap, and upper label, emphasizing surface and detail.
Style/medium: photorealistic premium cosmetic product photography.
Composition: three equal vertical panels with subtle clean gutters, same bottle, same pedestal, same electric-blue backdrop, same lighting direction and color grade.
Constraints: no captions, no letters outside the existing package, no arrows, no watermark; do not add props; do not change the bottle identity between panels; only shot size and angle change.
```

## 2. 環境動態

輸出：`assets/prompt-variable-environment-motion.png`

```text
Use case: scientific-educational
Asset type: landscape comparison plate for a Traditional Chinese classroom slide
Input image: preserve the exact same product identity, tall white rectangular shampoo bottle, hot-magenta pump, printed label layout, opaque packaging material, glossy hot-magenta pedestal, electric-blue studio composition, camera angle, lighting direction, and color grade in all panels.
Primary request: create a three-panel horizontal triptych that teaches the effect of environmental dynamics while all other conditions stay fixed.
Panel A: the bottle is completely still in calm water with no secondary event.
Panel B: one clean crystalline wave rises behind the bottle in a readable arc, supporting the product without covering it.
Panel C: too many competing secondary events at once—crossing splashes, dense foam, suspended droplets, ribbons of mist, and particles—making the composition visibly cluttered while the bottle remains in the same position.
Style: photorealistic premium cosmetic product photography.
Constraints: no captions, no arrows, no watermark; same bottle and framing in every panel; only the amount of environmental dynamics changes.
```

## 3. 焦點與動態模糊

輸出：`assets/prompt-variable-focus-blur.png`

```text
Use case: scientific-educational
Asset type: landscape comparison plate for a Traditional Chinese classroom slide
Input image: preserve the exact same product identity, tall white rectangular shampoo bottle, hot-magenta pump, printed label layout, opaque packaging material, glossy hot-magenta pedestal, electric-blue studio composition, camera angle, lighting direction, and color grade in all panels.
Primary request: create a three-panel horizontal triptych that teaches focus target and controlled motion blur while all other conditions stay fixed. In every panel a clean wave sweeps upward behind the stationary bottle.
Panel A: everything is frozen and tack sharp, including every droplet.
Panel B: the bottle, cap, brand mark, and label remain crisp and stable while only the outer spray and foreground droplets have light directional motion blur.
Panel C: excessive global motion blur affects the bottle, cap, label, and water, making the product difficult to read.
Style: photorealistic premium cosmetic product photography.
Constraints: no captions, no arrows, no watermark; identical bottle, wave, framing, exposure, and color in every panel; only focus and blur treatment change.
```

## 4. 色彩、光線與情緒

輸出：`assets/prompt-variable-color-mood.png`

```text
Use case: scientific-educational
Asset type: landscape comparison plate for a Traditional Chinese classroom slide
Input image: preserve the exact same product identity, tall white rectangular shampoo bottle, hot-magenta pump, printed label layout, opaque packaging material, glossy hot-magenta pedestal, camera angle, and composition in all panels.
Primary request: create a three-panel horizontal triptych that teaches how color, lighting, and mood change the same product shot while all objects and framing stay fixed.
Panel A: bright clear cyan daylight filtering through water, airy high-key exposure, optimistic and uplifting mood.
Panel B: hard direct flash with deep graphite shadows and restrained color, tense, intimate, rebellious mood.
Panel C: electric blue and hot magenta studio highlights with glossy reflections, pristine, energetic, premium commercial mood.
Style: photorealistic cosmetic advertising.
Constraints: no captions, no arrows, no watermark; same exact bottle, pose, scale, pedestal, background geometry, and camera angle in every panel; only color, lighting, and emotional tone change.
```

## 5. 主要運鏡

輸出：`assets/prompt-variable-camera-movement.png`

```text
Use case: scientific-educational
Asset type: landscape cinematic storyboard comparison plate for a Traditional Chinese classroom slide
Input image: preserve the same tall white rectangular shampoo bottle, hot-magenta pump, printed label layout, opaque packaging material, glossy hot-magenta sculptural pedestal, electric-blue studio setting, lighting, and color grade.
Primary request: create a clean three-column comparison board that visualizes three different camera movements. Each column contains three small sequential keyframes—start, middle, end—of the exact same bottle and scene.
Column A: slow push-in from a wide shot to a closer shot; camera remains centered and perspective direction stays stable.
Column B: lateral tracking move from left to right; bottle scale stays nearly constant while background parallax shifts sideways.
Column C: gentle orbit around the bottle; camera angle changes from front to three-quarter view while distance stays nearly constant.
Composition: three equal columns with clean white gutters; within each column, three clearly separated sequential frames stacked vertically. Keep the bottle recognizable in all nine frames.
Style: photorealistic premium cosmetic product photography presented as a professional storyboard contact sheet.
Constraints: no captions, no letters outside the existing package, no arrows, no watermark; do not add props; only the camera path changes between columns.
```

## 課堂操作

1. 先遮住 A／B／C 的說明，請學員只描述畫面差異。
2. 再公開提示詞中唯一改動的變因。
3. 請 Agent 把觀察改寫成可驗收條件。
4. 最後才到目標模型做同條件測試，記錄成功與失敗版本。
