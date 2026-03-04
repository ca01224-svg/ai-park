# 共有アセットフォルダガイド

## 概要

商材ごとのブランドアセット（ロゴ、素材画像等）を **全スキル横断** で管理する共有フォルダ。
Banner Park / Short Ad Park / 記事LP Park が自動参照し、ブランドカラー・ロゴ等を自動適用する。

## フォルダ構造

```
AIパク/                          ← プロジェクトルート
  assets/                        ← ★共有アセットフォルダ（全スキル共通）
    {product-slug}/
      manifest.json              ← 必須: メタデータ定義
      logo.png                   ← ロゴ画像（推奨: 透過PNG）
      brand-voice.md             ← ブランドボイス（トーン・推奨/禁止ワード・CTAパターン等）
      hero.png                   ← ヒーローイメージ（任意）
      icon.png                   ← アイコン（任意）
      ...
  banner-park/
    output/{slug}-{suffix}/      ← Banner Park 出力先
  記事LP-park/
    assets/{slug}/               ← 記事LP Park固有の素材（LP全文等）
  .claude/
    commands/                    ← スキル定義
    knowledge/                   ← ナレッジDB
```

## manifest.json フォーマット

```json
{
  "product_name": "商材名（日本語）",
  "product_slug": "英数字スラッグ",
  "brand_color": "#007AFF",
  "brand_color_secondary": "#0055CC",
  "logo": "logo.png",
  "logo_position": "top-right",
  "product_url": "https://example.com/",
  "dpro_product_id": 12345,
  "category": "SaaS | EC | リード | アプリ",
  "additional_assets": [],
  "notes": "自由記述メモ"
}
```

### フィールド説明

| フィールド | 必須 | 説明 |
|-----------|------|------|
| product_name | YES | 日本語の商材名 |
| product_slug | YES | フォルダ名と一致するスラッグ |
| brand_color | YES | メインブランドカラー（HEX） |
| logo | YES | ロゴファイル名 |
| logo_position | NO | オーバーレイ位置（top-right / top-left）デフォルト: top-right |
| brand_voice | NO | ブランドボイスファイル名（例: "brand-voice.md"） |
| product_url | NO | 公式サイトURL |
| dpro_product_id | NO | DPro API の product_id |
| category | NO | 商材カテゴリ |

## スラッグ命名規則

- 英数字 + ハイフンのみ
- 例: "動画広告分析Pro" → `dpro`
- 例: "Squad beyond" → `squad-beyond`
- 例: "ビューティーパレット" → `beauty-palette`

## 登録済みアセット

| slug | 商材名 | ロゴ | カテゴリ |
|------|--------|------|---------|
| dpro | 動画広告分析Pro | logo.png (24KB) | SaaS |

## 各スキルでの動作

### Banner Park（v5.5〜）
1. Phase 0 でヒアリング → `PRODUCT_SLUG` 生成
2. Phase 0.5 冒頭で `assets/{PRODUCT_SLUG}/manifest.json` をチェック
3. **存在**: ロゴ・カラー・ブランドボイスを自動ロード、Web検索スキップ
4. **不在**: 従来どおりWeb収集 → 終了後にフォルダ作成を推奨
5. Phase 3 コピー生成時に `BRAND_VOICE`（トーン・推奨/禁止ワード・CTAパターン）を参照
6. Phase 5 のHTML生成時に `overlay-logo` として右上に配置

### Short Ad Park（v5.1〜）
1. Phase 1.5 冒頭で `assets/{PRODUCT_SLUG}/manifest.json` をチェック
2. **存在**: ブランドカラー・商材URL・ブランドボイスを自動ロード
3. **不在**: 従来どおりWeb検索で収集
4. Phase 2-B 台本生成時に `BRAND_VOICE` を参照

### 記事LP Park（v2.3〜）
1. Phase 0 のヒアリング後に `assets/{商材slug}/manifest.json` をチェック
2. **存在**: ロゴ・ブランドカラー・ブランドボイスを自動読み込み。LP分析のカラー推定より優先
3. **不在**: 従来どおりLP分析からカラー推定
4. Phase 2-C 記事LP生成時に `BRAND_VOICE` を参照
5. ※ LP全文等のスキル固有素材は従来どおり `記事LP-park/assets/{slug}/` に保存

## brand-voice.md のテンプレート

```markdown
# {商材名} — ブランドボイスガイド

## トーン & マナー
- （例: プロフェッショナルだが堅すぎない）

## 必須キーワード（使ってOK / 推奨）
- （例: 1億件、1800社以上、7日間無料トライアル）

## 禁止・注意ワード
- （例: 「業界No.1」→ 根拠なしNG）

## CTA パターン（実績あり）
- （例: 「無料で試す」「今すぐ始める」）

## N1 ペルソナ要約
- （例: 田中マコト 34歳 中小EC広告運用担当）

## コピーの型（商材固有）
- （例: 数字衝撃型「1億件から○○」）
```

## 新商材の登録方法

1. `assets/{slug}/` フォルダを作成
2. ロゴ画像（透過PNG推奨）を `logo.png` として配置
3. `manifest.json` を作成（上記フォーマット参照）
4. `brand-voice.md` を作成（上記テンプレート参照）— 任意だが推奨
5. → 次回から全スキルが自動参照（ロゴ + カラー + 書き方ルール）
