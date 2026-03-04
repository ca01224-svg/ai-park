# Short Ad Park ver.7.0 — DNA転用 × デスマス調連続トーク × デュアル素材 × マルチシーン

strategy.json + Concept Park 完了前提。strategy.json の `formatStrategy.shortAd` を動画に**翻訳**する。コンセプト・N1・フック角度・KVトーンは全て strategy.json から読む。自前でリサーチやコンセプト設計はしない。

`/shortad-park` で起動。

---

## 起動時表示

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SHORT AD PARK ver.7.0
  DNA転用 × デスマス調連続トーク × デュアル素材 × マルチシーン
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  前提: /research-park + /concept-park 完了済み
  搭載システム:
  - strategy.json 戦略翻訳エンジン
  - HIT広告DNA分析→抽象化→商材転用
  - デスマス調話し言葉 × 連続トークスタイル
  - デュアル素材: Nano Banana Pro画像 × Grok Imagine Video動画
  - マルチシーン（30秒15シーン × 各≤2秒） + 10秒4シーン
  - ベクトル品質ゲート + テロップ欠落チェック + flowCheck
  - 冒頭3パターン × Hook別BGM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

ランダム1行:
- 「HIT広告のDNAを抽出して、戦略に翻訳する。」
- 「全シーンが1本のトーク。繋がる、流れる、刺さる。」
- 「N1の脳内に1番乗りする動画、作るぞ。」
- 「Nano Bananaが画、Grokが動き。デュアルで仕掛ける。」

---

## ver.6.0 → ver.7.0 の転換

| 領域 | ver.6.0 | ver.7.0 |
|------|---------|---------|
| 尺 | 10秒固定（4シーン） | **30秒15シーン（各≤2秒）+ 10秒4シーンの選択制** |
| 台本スタイル | 短文テロップ | **デスマス調話し言葉の連続トーク（全シーンが接続詞で繋がる1本のトーク）** |
| DNA参照 | DPro構成参考（オプション） | **HIT広告DNA分析→抽象化→商材転用（Phase 1で必ず実行）** |
| 素材エンジン | Grok動画 + Veo動画（デュアルエンジン） | **Nano Banana Pro画像 + Grok動画（デュアル素材）** |
| 画像エンジン | Gemini 3 Pro Image（キーフレームのみ） | **Nano Banana Pro（全シーン画像生成）** |
| 動画エンジン | Grok 10秒ワンショット + Veo 8秒ワンショット | **Grok 2秒シーン別クリップ × 8本** |
| ループ | 許容 | **ループ禁止 → B-roll挿入** |
| BGM | 合成BGM | **フリーBGM（甘茶の音楽工房等）× Hook別に異なるBGM** |
| テロップ検証 | なし | **テロップ欠落チェック + flowCheck（接続詞検証）** |
| Oh my teethパターン | なし | **OFFER stacking（30%）、「これでは終わりません！」ブリッジ、低バリアCTA** |

---

## ワークフロー概要

```
Phase 0: strategy.json読み込み + 動画設定ヒアリング
    ↓
Phase 1: HIT広告DNA分析（DProで取得 → シーン分析 → DNA抽出 → 抽象化）
    ↓
Phase 2: 戦略翻訳 × DNA転用
    2-A: hookVectorsから3フック自動選定（ベクトル多様性最大化）
    2-B: Visual Anchor設計
    2-C: DNA転用台本ドラフト（デスマス調連続トーク）
    2-D: テロップ欠落チェック + flowCheck + ベクトル品質ゲート
    ↓
Phase 3: ユーザー確認 → 台本JSON生成（3ファイル）
    ↓
Phase 4: デュアル素材生成
    Step 1: Nano Banana Pro 画像生成（全15シーン）
    Step 2: Grok Imagine Video クリップ生成（8シーン）+ ポートレート変換
    Step 3: Fish Audio TTS で音声生成（1.2倍速）
    Step 4: フリーBGM取得（Hook別3曲）
    ↓
Phase 5: アセンブル（moviepy — 画像Ken Burns + 動画クリップ + テロップ + TTS + BGM）
    ↓
Phase 6: レポート + バリエーション展開
```

---

## モジュラーアーキテクチャ参照

### knowledge/（ナレッジDB）
- `.claude/knowledge/scene-role-tags.md` — シーンロールタグ15種 + EPS + 1シーン1メッセージ原則（ver.5.0）
- `.claude/knowledge/motion-patterns.md` — imagePrompt構造 + Visual Anchor + モーションパターンDB
- `.claude/knowledge/shortad-dna-templates.md` — 勝ちDNAテンプレート A〜G + 縦型広告の鉄則14条（ver.5.0）
- `.claude/knowledge/hook-db.md` — ショート広告用フックDB H1〜H8
- `.claude/knowledge/cta-db.md` — ショート広告用CTADB C1〜C8

---

## 環境設定（全Phase共通）

- `XAI_KEY` = 環境変数 `XAI_API_KEY`（Grok Imagine Video用）
- `GEMINI_KEY` = 環境変数 `GEMINI_API_KEY_1` / `_2` / `_3`（Nano Banana Pro画像用 + Veoバックアップ）
- `FISH_KEY` = 環境変数 `FISH_AUDIO_API_KEY`
- `FFMPEG` = `/Users/aipark2/Library/Python/3.9/lib/python/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1`
- 出力先: `shortad-park/output/{slug}/`

---

## Phase 0: strategy.json読み込み + 動画設定ヒアリング

### 0-A: strategy.json 読み込み

v6.0と同じ。`research-park/output/{PRODUCT_SLUG}/strategy.json` を Read。

### 0-B: 動画設定ヒアリング

```
━━━ 動画設定（strategy.json読み込み済み） ━━━

  商材: {productIntel.name}
  コンセプト: 「{concept.selected}」

  以下を選択してください:

1. 尺とスタイルは？
   a) 30秒マルチシーン × デスマス調連続トーク（推奨 — v7.0新機能）
   b) 10秒4シーン × 短文テロップ（v6.0互換）

2. DNA参照元は？（30秒モード時）
   a) DProから同ジャンルTOP5を自動取得（推奨）
   b) 手動でDPro IDを指定
   c) DNA参照なし（strategy.jsonのみ）

3. BGMは？
   a) フリーBGM自動取得 × Hook別（推奨）
   b) 合成BGM
   c) BGMなし

4. ボイスは？
   a) ほしVer3.0（デフォルト） referenceId: 54fa0418415a4103885ec909023b0285
   b) 信ボイスver1.0  referenceId: 92c556e1a13e4ac7add3d1a8665c3cb8
   c) ふうか  referenceId: 46745543e52548238593a3962be77e3a
   d) 佐藤 葵  referenceId: f787e74f89d84b148bb5355fda204641
━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 1: HIT広告DNA分析

### 設計思想

HIT広告のDNA（構成パターン・ナレーションスタイル・接続詞パターン・OFFER配分比率）を抽出し、抽象化して対象商材に転用する。Oh my teeth DNA転用で実証済み。

### Step 1: DProでHIT動画取得

```
genre_id: {特定したジャンルID}
media_type: video
sort: cost_difference-desc
interval: 30
limit: 50
```

### Step 2: TOP5のシーン分析JSON生成

各動画を視聴し、以下の構造でシーン分析JSONを生成:

```json
{
  "total_duration_sec": 54,
  "scene_count": 18,
  "scenes": [
    {
      "scene_number": 1,
      "duration_sec": 1.7,
      "role": "HOOK/PAIN",
      "narration_text": "前歯が2mmズレてる人",
      "overlay_text": "前歯が2mmズレてる人"
    }
  ],
  "overall_structure": "Hook→Offer→Pivot→Proof→Mechanism→Offer(multi)→CTA",
  "voice_style": "男性、明瞭、ハキハキ、親しみやすい"
}
```

### Step 3: DNA抽出（5つの要素）

TOP5から以下のDNA要素を抽出:

| DNA要素 | 抽出対象 | 例 |
|---------|---------|-----|
| **構成パターン** | シーンロール配分比率 | OFFER 30%、CTA 20% |
| **接続詞パターン** | シーン間の橋渡し語 | 「というのも」「なんですが」「つまり」「しかも」 |
| **ブリッジパターン** | OFFER畳み掛けの加速ポイント | 「これでは終わりません！」 |
| **CTAパターン** | 低バリアCTAの型 | 「○○だけでもチェックしてみてください」 |
| **トークスタイル** | 話し方の特徴 | デスマス調、話し言葉、連続トーク |

### Step 4: 抽象化→一般化

抽出したDNAを商材非依存の一般型に変換:

```
具体: "前歯が2mmズレてる人" → 抽象: "[具体的痛点を数字で刺す]人"
具体: "矯正代6ヶ月分0円" → 抽象: "[メイン機能]を[期間/量]無料"
具体: "予約枠が空いてるかだけでもチェックしてみて" → 抽象: "無料で[メイン機能]だけでもチェックしてみてください"
```

---

## Phase 2: 戦略翻訳 × DNA転用

### 2-A: hookVectorsから3フック自動選定

v6.0と同じベクトル多様性最大化アルゴリズム。

### 2-B: Visual Anchor設計

v6.0と同じ。strategy.jsonのkeyVisual + primaryN1 から自動生成。

### 2-C: DNA転用台本ドラフト（デスマス調連続トーク）

**翻訳の原則: strategy.json × DNA = 台本。DNAが骨格、strategy.jsonが肉。**

#### 30秒15シーン構成テンプレート（DNA: パターンG）

```
scene_01 [HOOK]            2.0s — フック（A/B/Cの3パターン）
scene_02 [PAIN]            2.0s — 痛点質問「○○、見直したことありますか？」
scene_03 [PIVOT]           1.5s — 転換「実はですね。」
scene_04 [MECHANISM_HOW]   2.0s — 仕組み「○○を変えるだけで結果が変わるんです。」
scene_05 [BRAND]           2.0s — ブランド導入「○○っていうサービスなんですが。」
scene_06 [MECHANISM_WHAT]  2.0s — 機能説明「○○だけを○○できるんですよね。」
scene_07 [BENEFIT]         2.0s — 効果「つまり○○にだけ○○できます。」
scene_08 [PROOF_NUMBER]    2.0s — 実績数字「導入○○社、○○%削減の実績です。」
scene_09 [OFFER_PRICE]     2.0s — 価格「月○○円で○○が完全無制限なんですよ。」
scene_10 [OFFER]           2.0s — 追加価値「しかも○○が今日から使えます。」
scene_11 [BRIDGE]          1.0s — 畳み掛け加速「これでは終わりません！」
scene_12 [OFFER_BARRIER]   2.0s — 障壁除去「初期費用ゼロ円、無料トライアル○日間。」
scene_13 [URGENCY]         2.0s — 緊急性「導入○日で○○の会社さんもありますので。」
scene_14 [CTA_ACTION]      2.5s — 低バリアCTA「まずは無料で○○だけでもチェックしてみてください。」
scene_15 [CTA_FINAL]       3.0s — テロップのみ「○○をチェック ↓↓↓」
                          ─────
                          30.0s
```

#### 🔴 鉄のルール: デスマス調連続トーク 7原則

1. **全シーンが1本の連続トークとして繋がる** — 台本を全部繋げて読んだ時に1人のトークとして自然に流れること
2. **接続詞で橋渡し** — シーン間は「なんですが」「つまり」「しかも」「ので」等で接続。途切れない
3. **デスマス調** — 全narrationが「です」「ます」「ください」で終わる。ただし「実はですね。」等の話し言葉的なデスマスOK
4. **話し言葉** — 書き言葉NG。「～んです」「～なんですよ」「～んですよね」「～ついてます」等の自然な口語
5. **単語単語NG** — チョッピーな単語の羅列は禁止。文として意味が完結する
6. **1シーン1メッセージ** — 1シーンに詰め込みすぎない。2文以上になったらシーン分割
7. **テロップ ≠ narrationのコピペ** — テロップはnarrationの核心キーワードだけ抽出（短く。5-15文字）

#### flowCheck（台本完成時に必ず実行）

全シーンの接続を検証:

```json
{
  "scene_02→03": "？→実はですね。（疑問→転換）",
  "scene_04→05": "んです。→っていうサービスなんですが。（説明→ブランド接続）",
  "scene_09→10": "なんですよ。→しかも（価格→追加価値）",
  "scene_10→11": "使えます。→これでは終わりません！（Oh my teethブリッジ）"
}
```

全ペアが自然に接続していることを確認。不自然な断絶があれば修正。

#### テロップ欠落チェック（ver.5.0 — 必須）

全シーンのnarrationの核心メッセージがoverlayTextに反映されていることを確認:

```
NG: narration「名簿の質、見直したことある？」→ overlayText なし ← テロップ欠落！
OK: narration「名簿の質、見直したことありますか？」→ overlayText「名簿の質\n見直したこと\nありますか？」
```

### 2-D: ベクトル品質ゲート

v6.0と同じ。Hook × N1需要、台本 × コンセプト、Hook × 競合、Hook間多様性の4検証。

---

## Phase 3: ユーザー確認 → 台本JSON生成

### 台本JSON テンプレート（v7.0）

```json
{
  "title": "Short Ad DNA v7: {商材名} — {DNA元}DNA × デスマス調連続トーク",
  "version": "7.0",
  "dnaSource": "{DNA元}_top5_golden ({パターン名})",
  "dnaElements": {
    "talkStyle": "デスマス調話し言葉。全シーンが1本の連続トーク。",
    "connectors": ["なんですが", "つまり", "しかも", "これでは終わりません！"],
    "offerStacking": "OFFER系シーンが全体の33%",
    "bridgePattern": "「これでは終わりません！」",
    "ctaPattern": "「○○だけでもチェックしてみてください」"
  },
  "settings": {
    "aspectRatio": "9:16",
    "resolution": { "width": 1080, "height": 1920 },
    "fps": 30,
    "totalDuration": 30,
    "voice": { "referenceId": "...", "speed": 1.2 },
    "imageEngine": "nano-banana-pro (gemini-3-pro-image-preview)",
    "videoEngine": "grok-imagine-video",
    "maxSceneDuration": 2
  },
  "hooks": { "A": {...}, "B": {...}, "C": {...} },
  "scenes": [...],
  "telopCheck": { "rule": "ver.5.0", "allPassed": true },
  "flowCheck": { "connectors": {...}, "allPassed": true }
}
```

---

## Phase 4: デュアル素材生成

### デュアル素材設計（v7.0の核心）

| 素材 | エンジン | モデル | 用途 | 理由 |
|------|---------|--------|------|------|
| **画像** | Nano Banana Pro | `gemini-3-pro-image-preview` | 全15シーンの静止画 | 英語テキスト混入なし。品質安定 |
| **動画** | Grok Imagine Video | `grok-imagine-video` | 動きが必要な8シーン | LM Arena #1。プロンプト忠実度最強 |

**なぜデュアル素材？**: 全シーン動画だと生成時間・コスト大。画像（Ken Burns効果）と動画を交互に配置することで、視覚的多様性＋コスト最適化。静止画シーンの「止まった感」をKen Burnsのゆっくりズーム/パンで解消。

### Step 1: Nano Banana Pro 画像生成（全15シーン）

```python
# gemini-3-pro-image-preview で画像生成
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key={api_key}"
payload = {
    "contents": [{"parts": [{"text": image_prompt}]}],
    "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}
}
# レスポンスから inlineData.data をbase64デコードしてJPG保存
```

imagePrompt必須要素:
- Visual Anchor（protagonist記述）
- `vertical 9:16 portrait orientation`
- `no text no words no English no letters`（🔴 これを必ず入れる）
- `photorealistic, cinematic lighting`

### Step 2: Grok Imagine Video クリップ生成（8シーン）

動きが必要なシーンのみGrokで生成:
- HOOK (scene_01): 人物の動き
- MECHANISM系 (scene_04, 06): データ変換・フィルター
- PROOF (scene_08): チャートアニメーション
- OFFER (scene_10): リストスクロール
- BRIDGE (scene_11): 人物の表情変化
- URGENCY (scene_13): カレンダーめくり
- CTA (scene_14): 指差しジェスチャー

```python
resp = requests.post("https://api.x.ai/v1/videos/generations",
    headers={"Authorization": f"Bearer {XAI_KEY}"},
    json={"model": "grok-imagine-video", "prompt": prompt, "duration": 2})
request_id = resp.json()["request_id"]
# ポーリング: video キーの存在で完了判定
```

### 🔴 Grok ポートレート変換（必須！）

**Grokは必ず848x480（ランドスケープ）で出力する**。vertical 9:16をプロンプトに書いても無視される。全Grokクリップは以下で必ず変換:

```bash
"$FFMPEG" -y -i "$raw_clip" -vf "scale=-1:1280,crop=720:1280" -c:a copy "$portrait_clip"
```

これをスキップすると映像がグリッチする（v5で実証済み）。

### Step 3: Fish Audio TTS

```python
resp = requests.post("https://api.fish.audio/v1/tts",
    headers={"Authorization": f"Bearer {FISH_KEY}"},
    json={"text": narration, "reference_id": ref_id, "format": "mp3"})
# 1.2倍速化
"$FFMPEG" -y -i "$raw.mp3" -filter:a "atempo=1.2" -vn "$fast.mp3"
```

### Step 4: フリーBGM取得（Hook別3曲）

甘茶の音楽工房から明るい雰囲気の3曲をDL:
```
https://amachamusic.chagasi.com/mp3/{filename}.mp3
```

Hook別にBGMを変えることで、A/Bテストの音響変数も追加。

---

## Phase 5: アセンブル

### moviepy 2.1.2 でのアセンブル

```python
from moviepy import VideoFileClip, ImageClip, TextClip, AudioFileClip,
    CompositeVideoClip, concatenate_videoclips, CompositeAudioClip

# 各シーン: Grok動画 or NanoBanana画像(Ken Burns)
for scene in scenes:
    if grok_clip_exists(scene):
        vc = VideoFileClip(grok_path).resized((720, 1280))
    else:
        vc = ImageClip(image_path).with_duration(scene.duration).resized(height=1280)
        # Center cropで720x1280
    # テロップ overlay
    telop = TextClip(text=overlay_text, font=FONT, font_size=52,
                     color="white", stroke_color="black", stroke_width=3,
                     method="caption", size=(640, None))
    scene_clip = CompositeVideoClip([vc, telop.with_position(("center", 0.45), relative=True)])

# BGM volume: with_volume_scaled(0.10)
# TTS: AudioFileClip → with_start(time)
```

### 🔴 ループ禁止ルール

narration音声がシーン動画より長い場合:
- ❌ 動画をループさせる → 映像が止まって見える
- ✅ B-roll（別の短いGrokクリップ）を挿入する

```python
if raw.duration < target_dur:
    main_clip = raw.subclipped(0, raw.duration - 0.04)
    remain = target_dur - main_clip.duration
    broll = VideoFileClip(broll_path).subclipped(0, remain)
    vc = concatenate_videoclips([main_clip, broll])
```

### フォント

```
/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc
```

---

## Phase 6: レポート + バリエーション展開

### 成果物一覧

```
shortad-park/scripts/{slug}-v7.0-omt.json     ← 台本JSON
shortad-park/output/{slug}-v7/
  ├── images/scene_{01-15}.jpg                 ← Nano Banana Pro画像
  ├── clips/scene_{01,04,06,08,10,11,13,14}.mp4 ← Grok動画クリップ
  ├── audio/{hook_A,hook_B,hook_C,scene_02-14}_fast.mp3 ← TTS
  ├── bgm/{happytime,picopicodisco,lovelyflower}.mp3    ← フリーBGM
  ├── final-hookA-v7.mp4                       ← 完成動画A
  ├── final-hookB-v7.mp4                       ← 完成動画B
  └── final-hookC-v7.mp4                       ← 完成動画C
```

---

## 品質チェックリスト（Phase 5完了後に必ず実行）

- [ ] テロップ欠落チェック: 全シーンのnarration核心がoverlayTextに反映
- [ ] flowCheck: 全シーン間が接続詞で自然に接続
- [ ] 1シーン1メッセージ: 1シーンに2文以上ないか
- [ ] 全シーン ≤ 2秒: 同じシーンが2秒以上続かないか
- [ ] ループなし: 映像が止まって見えるシーンがないか
- [ ] Grokポートレート変換済み: 全Grokクリップが720x1280か
- [ ] デスマス調: 全narrationが「です/ます/ください」で終わるか
- [ ] 連続トーク: 全シーンを繋げて読んで1本のトークとして自然か

---

## トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| Grok動画がランドスケープ | 🔴 必ず `scale=-1:1280,crop=720:1280` で変換。v7.0の鉄則 |
| 映像が止まって見える | ループ禁止。B-rollクリップを挿入 |
| テロップが欠落 | scene-role-tags ver.5.0 のテロップ欠落チェック |
| narrationが途切れて聞こえる | flowCheck → 接続詞を補強 |
| Nano Banana Proに英語テキスト | プロンプトに `no text no words no English` を必ず追加 |
| Gemini APIエラー | 3キーローテーション。三浦莉さん（U073VJMS751）に報告 |
| Grokクレジット枯渇 | 画像Ken Burns + エフェクトでフォールバック |
| DPro MCPエラー | 即鍋谷報告（C05H9N7C33L）。curlフォールバック |

---

## 注意事項

- **これは「戦略翻訳 × DNA転用」スキル**。コンセプトやN1を新規設計しない
- **DNA分析がv7.0の核心**。HIT広告の構成を抽象化→商材転用する
- **デスマス調連続トークが最大の差別化**。チョッピーなテロップ動画から、流れるトーク動画へ
- APIキーは環境変数（.zshrc）に設定
- **サブエージェントは WebSearch / WebFetch / DPro MCP にアクセス不可**
- スキルのバージョンアップは全承認。許可を求めず自走する
