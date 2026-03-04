# モーションパターンDB × Kling禁止7則（Short Ad Park）

## imagePrompt 7コンポーネント構造

全imagePromptを以下の順序で構成する:

```
[SUBJECT] + [COMPOSITION] + [LIGHTING] + [STYLE] + [EMOTION] + [TECHNICAL] + [TEXT ZONE]

1. SUBJECT:     誰/何がフレーム内にいるか（Visual Anchor参照）
2. COMPOSITION: カメラアングル、フレーミング、被写界深度
3. LIGHTING:    光源、方向、色温度（ロールに連動）
4. STYLE:       Photorealistic / UGC / Editorial / Typography
5. EMOTION:     この画像が喚起すべき感情
6. TECHNICAL:   解像度マーカー、アスペクト比
7. TEXT ZONE:   テロップ用の空白領域指定
```

---

## Visual Anchor（キャラ一貫性保証）

Phase 4（台本JSON生成前）にVisual Anchorを定義する。AIパクくんがN1ペルソナに基づき提案する。

```
VISUAL_ANCHOR = {
  protagonist: "Japanese [gender], early [age]s, [hair detail], [build], wearing [specific outfit]",
  environment_A: "[pain/before environment with specific items]",
  environment_B: "[solution/after environment with different lighting]",
  color_palette: "scenes 1-{pivot}: cold blue #1a2a4a → scene {pivot}+: warm gold #d4a854",
  brand_accent: "[商材のブランドカラー hex]"
}
```

**ルール**: 人物が登場する全シーンのimagePromptに `protagonist` 記述を丸ごとコピーする。

---

## ロール別imagePromptテンプレート

```
HOOK (UGC):
  "Close-up of {protagonist}, {hook-specific action},
  {cold blue #1a2a4a harsh single light source},
  UGC smartphone selfie angle, slight lens distortion, authentic feel,
  photorealistic, 9:16 vertical composition,
  center third of frame clear for text overlay.
  Avoid: text, watermark, blurry, western face, caucasian, studio lighting, multiple people"

PAIN (POV):
  "POV over-shoulder shot of {protagonist}, staring at {pain-specific object/screen},
  {environment_A}, cold tones, dim single desk lamp,
  handheld feel, slight motion blur,
  photorealistic, 9:16 vertical,
  center third of frame clear for text overlay.
  Avoid: text, watermark, blurry, western face, bright lighting, studio setup"

PIVOT (Abstract):
  "Light breaking through darkness, gradient from cold blue #1a2a4a to warm gold #d4a854,
  abstract composition, no person, spacious hopeful feel,
  clean editorial style,
  photorealistic, 9:16 vertical,
  center third of frame clear for text overlay.
  Avoid: text, watermark, person, face, hands, busy background, cluttered"

MECHANISM_HOW (Abstract Mechanism):
  "Abstract mechanism visualization with flowing arrows or connection lines,
  showing cause-and-effect relationship, {brand_accent} accent,
  dark background, clean infographic style,
  9:16 vertical, center third of frame clear for text overlay.
  Avoid: realistic hands, cluttered diagram, text labels"

MECHANISM_WHAT (Product Detail):
  "Close-up product detail showing {specific_ingredient_or_feature},
  clean modern product photography, {brand_accent} accent lighting,
  bright professional backdrop,
  photorealistic, 9:16 vertical,
  center third of frame clear for text overlay.
  Avoid: human hands, cluttered background, cartoon style"

BENEFIT (Transformation):
  "Medium shot of {protagonist}, relaxed and confident in {environment_B},
  warm golden lighting suggesting positive transformation,
  photorealistic, authentic lifestyle feel,
  9:16 vertical composition,
  center third of frame clear for text overlay.
  Avoid: exaggerated expression, studio lighting, western face, multiple people"

PROOF_NUMBER (Typography):
  "Bold number {specific_number} displayed on dark background #0a1628,
  subtle rim light in {brand_accent},
  minimal data visualization style,
  photorealistic, 9:16 vertical,
  center third of frame clear for text overlay.
  Avoid: text, watermark, human face, hands, realistic person, portrait"

PROOF_VOICE (Testimonial UGC):
  "Close-up of {protagonist}, slightly smiling with natural expression,
  {environment_B}, warm {brand_accent} toned soft lighting,
  UGC smartphone angle, authentic and relatable,
  photorealistic, 9:16 vertical composition,
  center third of frame clear for text overlay.
  Avoid: studio lighting, professional pose, multiple people, western face"

OFFER_PRICE (Price):
  "Price comparison visualization, {old_price} crossed out revealing {new_price},
  dark background with {brand_accent} highlights,
  clean typography focus,
  9:16 vertical, center third of frame clear for text overlay.
  Avoid: text, watermark, human face, cluttered background"

OFFER_BARRIER (Trust):
  "Clean minimal layout with shield icon or checkmark symbol,
  dark background #0a1628, {brand_accent} accent highlights,
  clean editorial style, reassuring and trustworthy feel,
  9:16 vertical composition,
  center third of frame clear for text overlay.
  Avoid: realistic person, complex scene, cluttered elements"

CTA (Minimal):
  "Minimal dark background #0a1628, single glowing element in center,
  subtle rim light in {brand_accent},
  premium clean aesthetic,
  photorealistic, 9:16 vertical,
  center third of frame clear for text overlay.
  Avoid: text, watermark, person, busy background, cluttered elements"
```

---

## ロール別ネガティブプロンプト

```
UGC/人物シーン（HOOK, PAIN, PROOF_VOICE）:
  "text, watermark, blurry, low quality, deformed, distorted face,
  extra fingers, mutated hands, poorly drawn face, cross-eyed,
  western face, caucasian, multiple people, bright studio lighting"

タイポグラフィ/データシーン（PROOF_NUMBER, OFFER_PRICE）:
  "text, watermark, blurry, low quality,
  photograph of person, human face, hands, realistic person, portrait"

抽象/トランジション（PIVOT）:
  "text, watermark, blurry, low quality,
  person, face, hands, busy background, cluttered, multiple objects"

プロダクト/UIシーン（MECHANISM）:
  "text, watermark, blurry, low quality, deformed,
  realistic hands touching screen, outdated UI, cartoon, anime, illustration"
```

> **IMPORTANT (技術的事実)**: `imageNegativePrompt` はスキーマ（script.ts）にフィールドとして存在するが、`gemini-image.ts` の実装では `contents: [{ text: prompt }]` のみをGemini APIに渡しており、**ネガティブプロンプトは実際には使用されていない**。
> **対策**: ネガティブプロンプトの重要要素をimagePrompt本体の末尾に `Avoid: {key negative elements}` として統合する。`imageNegativePrompt` フィールドは将来のパイプライン改修用に維持する。

---

## Gemini 画像生成モデル固有の制約と Tips

| 項目 | 詳細 |
|------|------|
| モデル | `gemini-2.0-flash-exp-image-generation` |
| ネガティブプロンプト | **パラメータ非対応**。imagePrompt末尾の `Avoid:` 句で代替 |
| 入力 | テキストのみ（画像入力不可） |
| 並列数 | 最大3並列、3回リトライ（gemini-image.ts実装） |
| 言語 | **英語のみ推奨**（日本語は品質低下） |

**Gemini画像生成 Tips:**
- 品質マーカー: `photorealistic`, `8k`, `sharp focus`, `high detail` を含める
- 人物安定化: `natural expression`, `neutral pose` で表情・ポーズの暴れを抑制
- ネガティブ代替: imagePrompt末尾に `Avoid: {要素1}, {要素2}, ...` で除外指定
- 環境の安定化: 具体的小道具2-3個で場面を固定（例: `wooden desk, single desk lamp, coffee mug`）
- アスペクト比: `9:16 vertical composition` を必ず含める

**英語品質 Good/Bad 例:**

| | Bad (曖昧) | Good (具体的) |
|---|-----------|-------------|
| 人物 | `a woman looking sad` | `Japanese woman, early 30s, shoulder-length black hair, wearing white blouse, looking down with subtle frown` |
| 環境 | `a dark room` | `dimly lit apartment room, single desk lamp casting warm pool of light, wooden desk, scattered papers` |
| 構図 | `photo of product` | `close-up product photography, centered in frame, soft rim light in #d4a854, dark background #0a1628` |
| 品質 | `good quality photo` | `photorealistic, 8k, sharp focus, shallow depth of field, 9:16 vertical composition` |

---

## videoPrompt構造テンプレート

```
"[Camera Motion] + [Secondary Detail], [Speed Qualifier]"
Recommended: 5-10 words / Max: 15 words
```

---

## モーションパターンDB（ロール別）

| ロール | 安全なモーション例 | 禁止 |
|--------|-------------------|------|
| **HOOK** | `Quick zoom in toward center, slight camera shake` | 表情変化、全身動作 |
| **HOOK** | `Fast dolly push forward, dramatic approach` | 頭の動き |
| **PAIN** | `Very slow zoom in, barely perceptible creeping closer` | 首の回転、手の動き |
| **PAIN** | `Slight camera drift to the right, handheld feel` | 指の操作 |
| **PIVOT** | `Light intensity increasing from left side of frame` | シーン内トランジション |
| **PIVOT** | `Soft focus pull from background to foreground` | 人物の動き |
| **MECHANISM_HOW** | `Smooth steady zoom into abstract diagram` | 人がスクリーンを操作 |
| **MECHANISM_HOW** | `Gentle horizontal pan across flowing arrows` | タイピング、クリック |
| **MECHANISM_WHAT** | `Slow zoom into product detail or ingredient` | 人物の動き |
| **MECHANISM_WHAT** | `Subtle parallax on layered product elements` | テキスト変化 |
| **BENEFIT** | `Slow zoom out revealing protagonist in bright environment` | 表情変化 |
| **BENEFIT** | `Gentle camera drift with warm light intensifying` | 急な動き |
| **PROOF** | `Slow zoom into the central number, subtle depth shift` | グラフアニメーション |
| **PROOF** | `Gentle parallax effect on layered elements` | テキスト変化 |
| **OFFER** | `Subtle zoom revealing price comparison` | ボタンクリック |
| **OFFER** | `Slow pan down revealing offer details, soft ambient light` | 人物の反応 |
| **OFFER** | `Gentle camera push toward highlighted price area` | ボタンクリック |
| **CTA** | `Subtle pulse glow effect on central element` | 指タップ |
| **CTA** | `Very slow zoom out revealing full frame, ambient particles` | 人物登場 |

---

## Kling絶対禁止7則（ver.4.3）

```
1. 顔の表情変化を記述しない（smiles, frowns, looks surprised, widens eyes）
2. 手/指の動きを記述しない（types, points, gestures, clicks, taps）
3. 全身の移動を記述しない（walks, stands up, turns around, sits down）
4. テキストの出現/変化を記述しない（numbers counting, text appearing）
5. 複数人の動きを記述しない
6. overlayTextの内容をvideoPromptに含めない
7. 5-10ワードを推奨。15ワードは上限（短いほどKling成功率が高い）
```
