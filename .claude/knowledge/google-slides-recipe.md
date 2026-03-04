# Google Slides レシピ

AIパクが「スライド作って」と言われた時に使うレシピ。
スキルほど重くなく、メモほど軽くない「レシピ」粒度。

---

## 前提条件

- gcloud CLI インストール済み
- Google Cloud Project: `gen-lang-client-0752073678`
- アカウント: `parkmasayosi@gmail.com`
- Google Slides API & Google Drive API: 有効化済み

---

## Step 1: 認証確認

```bash
# 認証状態を確認
zsh -i -c 'gcloud auth list'

# 認証が切れていた場合（Drive スコープ付き）
zsh -i -c 'gcloud auth login --enable-gdrive-access'

# プロジェクト設定
zsh -i -c 'gcloud config set project gen-lang-client-0752073678'
```

---

## Step 2: python-pptx でスライド作成

```bash
# python-pptx インストール（初回のみ）
zsh -i -c 'pip install python-pptx'
```

### Apple Keynote 風デザインルール
- **背景**: 黒 (#000000) or ダークグレー (#1a1a1a)
- **テキスト**: 白 (#FFFFFF) メイン、グレー (#999999) サブ
- **フォント**: Noto Sans JP（Google Slides変換後に適用）
- **タイトル**: 54-72pt、太字
- **本文**: 28-36pt
- **余白**: 贅沢に。スライドの40%以上は余白
- **要素数**: 1スライド1メッセージ。詰め込み厳禁
- **アクセントカラー**: 1色だけ（ブランドに合わせる）

### Python テンプレート

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

def add_slide(title, subtitle=None, body_items=None, accent_color=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank layout

    # 黒背景
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(0, 0, 0)

    # タイトル
    left, top = Inches(1.2), Inches(2.0)
    txBox = slide.shapes.add_textbox(left, top, Inches(10.9), Inches(2.0))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(54)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.font.bold = True

    # サブタイトル
    if subtitle:
        left, top = Inches(1.2), Inches(4.2)
        txBox = slide.shapes.add_textbox(left, top, Inches(10.9), Inches(1.5))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = subtitle
        p.font.size = Pt(28)
        p.font.color.rgb = RGBColor(153, 153, 153)

    return slide

# 最後に保存
prs.save('output.pptx')
```

---

## Step 3: Google Slides にアップロード

```bash
# アクセストークン取得
ACCESS_TOKEN=$(zsh -i -c 'gcloud auth print-access-token')

# PPTX → Google Slides 変換アップロード（multipart）
curl -s -X POST \
  'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&convert=true' \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "x-goog-user-project: gen-lang-client-0752073678" \
  -F "metadata={\"name\": \"プレゼン名\", \"mimeType\": \"application/vnd.google-apps.presentation\"};type=application/json" \
  -F "file=@output.pptx;type=application/vnd.openxmlformats-officedocument.presentationml.presentation"
```

レスポンスから `id` を取得 → これがプレゼンテーションID。

---

## Step 4: フォント一括変更（Noto Sans JP）

python-pptx のフォント指定は Google Slides 変換時に無視されるため、Slides API で後から変更する。

```bash
ACCESS_TOKEN=$(zsh -i -c 'gcloud auth print-access-token')
PRESENTATION_ID="ここにID"

# 1. 全テキスト要素を取得
SLIDES_DATA=$(curl -s \
  "https://slides.googleapis.com/v1/presentations/$PRESENTATION_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "x-goog-user-project: gen-lang-client-0752073678")

# 2. Python で batchUpdate リクエストを生成
python3 << 'PYEOF'
import json, sys

data = json.loads('''ここにSLIDES_DATAの中身''')

requests = []
for slide in data.get('slides', []):
    for element in slide.get('pageElements', []):
        shape = element.get('shape', {})
        text = shape.get('text', {})
        for te in text.get('textElements', []):
            if 'textRun' in te:
                requests.append({
                    "updateTextStyle": {
                        "objectId": element['objectId'],
                        "textRange": {
                            "type": "ALL"
                        },
                        "style": {
                            "fontFamily": "Noto Sans JP"
                        },
                        "fields": "fontFamily"
                    }
                })
                break

# 重複排除
seen = set()
unique = []
for r in requests:
    oid = r['updateTextStyle']['objectId']
    if oid not in seen:
        seen.add(oid)
        unique.append(r)

print(json.dumps({"requests": unique}))
PYEOF

# 3. batchUpdate 実行
curl -s -X POST \
  "https://slides.googleapis.com/v1/presentations/$PRESENTATION_ID:batchUpdate" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "x-goog-user-project: gen-lang-client-0752073678" \
  -H "Content-Type: application/json" \
  -d @batch_request.json
```

---

## Step 5: 画像差し込み

```bash
# 画像をGoogle Driveにアップロード
curl -s -X POST \
  'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart' \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "x-goog-user-project: gen-lang-client-0752073678" \
  -F "metadata={\"name\": \"image.png\"};type=application/json" \
  -F "file=@image.png;type=image/png"

# レスポンスからファイルIDを取得し、公開URLを作成
IMAGE_FILE_ID="ここにファイルID"

# 共有設定（anyoneWithLink で閲覧可能に）
curl -s -X POST \
  "https://www.googleapis.com/drive/v3/files/$IMAGE_FILE_ID/permissions" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "x-goog-user-project: gen-lang-client-0752073678" \
  -H "Content-Type: application/json" \
  -d '{"role": "reader", "type": "anyone"}'

# Slides API で画像を挿入（createImage）
# 画像URL: https://drive.google.com/uc?id=$IMAGE_FILE_ID
curl -s -X POST \
  "https://slides.googleapis.com/v1/presentations/$PRESENTATION_ID:batchUpdate" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "x-goog-user-project: gen-lang-client-0752073678" \
  -H "Content-Type: application/json" \
  -d '{
    "requests": [{
      "createImage": {
        "url": "https://drive.google.com/uc?id='$IMAGE_FILE_ID'",
        "elementProperties": {
          "pageObjectId": "SLIDE_OBJECT_ID",
          "size": {
            "width": {"magnitude": 9600000, "unit": "EMU"},
            "height": {"magnitude": 5400000, "unit": "EMU"}
          },
          "transform": {
            "scaleX": 1, "scaleY": 1,
            "translateX": 0, "translateY": 0,
            "unit": "EMU"
          }
        }
      }
    }]
  }'
```

---

## 既存プレゼンテーション

| 名前 | ID | 用途 |
|------|-----|------|
| Claude Code × DPro 勉強会 | `1QT1yVIuOfL0IJiemC9IP2qH_H1PIgsohDtPSoimnK1k` | 2/25 勉強会用 |

---

## トラブルシューティング

- **403 quota project エラー**: `-H "x-goog-user-project: gen-lang-client-0752073678"` を付ける
- **認証切れ**: `gcloud auth login --enable-gdrive-access` で再認証
- **フォントが変わらない**: python-pptx のフォントは変換時に無視される → Step 4 で Slides API 経由で変更
- **画像が表示されない**: Drive の共有設定を `anyone` にしてからURLを使う
