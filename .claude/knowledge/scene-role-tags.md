# シーンロールタグシステム（Short Ad Park ver.4.3）

## シーンロール定義（15種）

各シーンに以下のロールタグを割り当て、ロールごとにnarration・overlayText・imagePrompt・videoPromptの生成ルールを制御する。

| ロールタグ | narration制約 | overlayText方向性 | 感情密度（EPS） |
|-----------|-------------|-----------------|--------------|
| `HOOK_SHOCK` | max 10文字。「。」終わり。[具体名詞/数字]+[衝撃動詞] | 衝撃ワード（3-4文字） | **Level 3 必須** |
| `HOOK_QUESTION` | max 12文字。「?」終わり。[ペイン]+してませんか? | 問いかけ（3-5文字） | **Level 3 必須** |
| `PAIN_SPECIFIC` | max 14文字。**N1口コミ生声を必ず含む** | 痛みの一言（3-4文字） | **Level 3 必須** |
| `PAIN_AMPLIFY` | max 14文字。具体数字で増幅 | 数字+「!?」（4-5文字） | Level 2-3 |
| `PIVOT` | max 8文字。「でも」「実は」「ところが」「なのに」「ただ」「けど」「一方で」「そんな中」「そんな時」で開始 | 転換ワード（2-3文字） | Level 2 |
| `MECHANISM_HOW` | max 16文字。「○○だから○○」原理/仕組み説明 | 核心動詞（3-4文字） | Level 2 |
| `MECHANISM_WHAT` | max 14文字。成分/機能/特徴を列挙 | 成分名（3-4文字） | Level 2 |
| `BENEFIT` | max 14文字。使用後の変化/体感を描写（EC型専用） | 体感ワード（3-4文字） | Level 2-3 |
| `PROOF_NUMBER` | max 12文字。数字+単位+「。」 | 数字のみ（3-5文字） | Level 2-3 |
| `PROOF_VOICE` | max 14文字。**口コミ生声をそのまま使用** | 生声抜粋（3-5文字） | **Level 3 必須** |
| `OFFER_PRICE` | max 14文字。価格対比を含む | 価格（4-5文字） | Level 2 |
| `OFFER_BARRIER` | max 12文字。「○○なし」「○○無料」 | 障壁除去（3-4文字） | Level 2 |
| `CTA_URGENCY` | max 10文字。希少性/緊急性 | 焦りワード（3-4文字） | **Level 3 必須** |
| `CTA_ACTION` | max 8文字。命令形。「今すぐ。」 | 行動指示（2-3文字） | **Level 3 必須** |

> **注**: `MECHANISM_HOW` / `MECHANISM_WHAT` は旧 `MECHANISM` の分割。`BENEFIT` はEC型専用タグ。リード型では `MECHANISM_HOW` + `MECHANISM_WHAT` で代替する。

---

## 感情密度レベル（EPS: Emotional Payload Score）

| レベル | 基準 | いつ使う |
|--------|------|---------|
| **Level 3（高）** | 内臓に来る。N1の生の言葉。パターン破壊。具体的数字 | フック、ペイン頂点、CTA |
| **Level 2（中）** | 緊張 or 発見がある。具体的ディテール | ピボット、メカニズム、証明 |
| **Level 1（低）** | 情報伝達。スムーズな橋渡し | 機能列挙、ブリッジ |

**EPSルール（ver.4.3 強制）:**
- 全シーンの **40%以上** がLevel 3
- 冒頭フックシーン + 末尾2シーンは **全て Level 3**
- Level 1 が **2シーン以上連続禁止**
- HOOK / PAIN_SPECIFIC / PROOF_VOICE / CTA_URGENCY / CTA_ACTION は **Level 3 固定**

### 尺別フックシーン数表

| 尺 | シーン数 | フックシーン | body開始 |
|----|---------|------------|---------|
| 30秒 | 14 | scene_01-02（2シーン） | scene_03 |
| 45秒 | 18 | scene_01-03（3シーン） | scene_04 |
| 60秒 | 24 | scene_01-03（3シーン） | scene_04 |

---

## シーンロールタグ割り当てディシジョンツリー

1. 冒頭フックシーンか? → `HOOK_SHOCK` or `HOOK_QUESTION`
2. N1の悩み/痛みを直接表現? → `PAIN_SPECIFIC`（口コミ含む）or `PAIN_AMPLIFY`（数字増幅）
3. 話題の転換点? → `PIVOT`
4. 商品の仕組み/原理を説明? → `MECHANISM_HOW`
5. 成分/機能/特徴を列挙? → `MECHANISM_WHAT`
6. 使用後の変化/体感を描写? → `BENEFIT`（EC型のみ）
7. 数字/データで信頼構築? → `PROOF_NUMBER`
8. 口コミ/体験談で信頼構築? → `PROOF_VOICE`
9. 価格/割引を提示? → `OFFER_PRICE`
10. 障壁除去（縛りなし、送料無料等）? → `OFFER_BARRIER`
11. 希少性/緊急性で行動促進? → `CTA_URGENCY`
12. 直接的な行動指示? → `CTA_ACTION`

---

## overlayText と narration の関係原則（ver.5.0 改訂）

### 🔴 鉄のルール: 1シーン1メッセージ原則
1. **1シーンのnarrationは1メッセージのみ**: narrationに2文以上含む場合、シーンを分割する
2. **テロップはナレーションの全内容を反映する**: narrationで言っている内容がoverlayTextに表示されない「テロップ欠落」は禁止
3. **テロップ欠落チェック（必須）**: 台本完成後、全シーンについて「このnarrationの内容はoverlayTextに全て反映されているか？」を検証する。1つでも欠落があれば修正してから素材生成に進む

### テロップ表現の原則
4. **overlayText = narrationのキーワード凝縮**: 一言一句同じでなくて良い。核心のキーワードを2-4行で表示
5. **読ませない、感じさせる**: 視聴者は「読む」のではなく「感じる」
6. **句読点の活用**: 「。」で余韻、「!?」で衝撃、「...」で含み

### NG例（ver.5.0で禁止）
❌ narration: "毎日100件送って、返信ゼロ。名簿の質、見直したことある？" → overlay: "毎日100件\n返信ゼロ"
→ 「名簿の質、見直したことある？」が完全欠落。シーンを分割せよ。

✅ 分割後:
- scene_A: narration="毎日100件送って、返信ゼロ。" → overlay="毎日100件\n返信ゼロ"
- scene_B: narration="名簿の質、見直したことある？" → overlay="名簿の質\n見直したことある？"

---

## Voice Transplant（N1生声の強制組み込み）

リサーチDIVEくんが抽出した口コミ生声を、シーンロールに分類する:

```
口コミ「マジでこれだけで変わった」→ PROOF_VOICE 用
口コミ「3週間もかかるんだよ」→ PAIN_SPECIFIC 用
口コミ「もっと早く知りたかった」→ CTA 動機付け用
口コミ「他のと全然違う」→ MECHANISM の補強用
```

**ルール**: PAIN_SPECIFIC と PROOF_VOICE のシーンでは、口コミ生声の語感・リズムを保持する義務。1-2語の調整は許容するが、感情のトーンを変えてはいけない。

---

## 獲得タイプ別 感情アーク必須形状

**30秒/14シーン（超短尺）:**
```
01-02: !! 衝撃/注意（HOOK）              — EPS Level 3 固定
03-04: vv 痛み/共感（PAIN）               — Level 2-3
05:    .. 息継ぎ（PIVOT）                 — Level 2
06-07: ^^ 発見（MECHANISM_HOW/WHAT）      — Level 2
08-09: == 信頼（PROOF）                   — Level 2-3
10-11: $$ オファー（OFFER）               — Level 2
12-14: >> 緊急/行動（CTA）                — EPS Level 3 固定
```
> 注記: 30秒は2シーンフック（scene_01-02のみ異なり、scene_03からbody開始）

**リード型（45秒/18シーン）:**
```
01-03: !! 衝撃/注意（HOOK）       — EPS Level 3 固定
04-06: vv 痛み/共感（PAIN）        — Level 2-3
07:    .. 息継ぎ（PIVOT）          — Level 2
08-10: ^^ 発見/期待（MECHANISM）   — Level 2
11-13: == 信頼（PROOF）            — Level 2-3
14-15: $$ オファー興奮（OFFER）    — Level 2
16-18: >> 緊急/行動（CTA）         — EPS Level 3 固定
```

**EC型（60秒/24シーン）:**
```
01-03: !! 衝撃/注意（HOOK）              — EPS Level 3 固定
04-06: vv 痛み/共感（PAIN）               — Level 2-3
07-08: .. 息継ぎ→ピボット（PIVOT）        — Level 2
09-10: ^^ 原理/仕組み（MECHANISM_HOW）    — Level 2
11-12: ^^ 成分/機能（MECHANISM_WHAT）     — Level 2
13-15: ** ベネフィット体感（BENEFIT）      — Level 2-3
16-18: == 信頼/権威（PROOF）              — Level 2-3
19-21: $$ オファー/障壁除去（OFFER）       — Level 2
22-24: >> 緊急/行動（CTA）                — EPS Level 3 固定
```

**アーク遷移ルール:**
- Pain → Pivot: narrationは「でも」「実は」「ところが」「なのに」「ただ」「けど」「一方で」「そんな中」「そんな時」で始まる
- Mechanism → Proof: narrationに具体的数字を含む
- Proof → Offer: narrationに価格 or パーセンテージを含む
