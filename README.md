# NSFK? (Not Safe For Kids?) - Prototype

YouTube動画の安全性を自動分析し、親が子供にとって適切なコンテンツかを判断できるAIエージェントのプロトタイプです。

## 🎯 概要

このプロトタイプは以下の機能を提供します：

- ✅ YouTube動画の自動ダウンロード
- ✅ 映像シーン検出・分析（GPT-4o-mini）
- ✅ 音声文字起こし・分析（Whisper）
- ✅ 子供向け安全性スコアリング（0-100点）
- ✅ 包括的な安全性レポート生成

## 📁 ファイル構成

```
Prototype/
├── main.py              # メイン実行ファイル
├── config.py           # 設定ファイル
├── youtube_downloader.py # YouTube動画ダウンロード
├── video_analyzer.py    # 動画分析（映像・音声）
├── safety_scorer.py     # 安全性スコアリング
├── requirements.txt     # 依存関係
├── README.md           # このファイル
├── videos/             # ダウンロード動画（一時）
├── images/             # 抽出画像（一時）
└── results/            # 分析結果
```

## 🚀 セットアップ

### 1. 依存関係のインストール

```bash
cd Prototype
pip install -r requirements.txt
```

### 2. OpenAI API キーの設定

`.env.example` を `.env` にコピーして、APIキーを設定：

```bash
cp .env.example .env
```

`.env` ファイルを編集：

```bash
# .env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

または環境変数で設定：

```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

## 📖 使用方法

### 基本的な使用方法

```bash
python main.py
```

実行後、YouTube URLまたは動画IDを入力してください。

### YouTube動画の指定方法

以下の形式に対応しています：

```bash
# 1. 完全なURL
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# 2. 短縮URL
python main.py "https://youtu.be/dQw4w9WgXcQ"

# 3. 動画IDのみ（11文字）
python main.py "dQw4w9WgXcQ"

# 4. インタラクティブ入力
python main.py
# → プロンプトでURL入力

# 5. クイック分析（簡易版）
python quick_analyze.py "dQw4w9WgXcQ"
```

### 設定のカスタマイズ

`config.py` で以下の設定を調整できます：

```python
# 分析精度 vs 速度・コストの調整
SCENE_THRESHOLD = 60.0   # 高い値＝少ないシーン＝高速・低コスト
MAX_SCENES = 20          # 最大分析シーン数
WHISPER_MODEL = "base"   # Whisperモデル(base/small/medium/large)
MAX_TOKENS = 5000        # GPT最大トークン数

# 安全性判定基準
SCORE_THRESHOLDS = {
    "safe": 80,      # 80点以上：推奨
    "caution": 60,   # 60-79点：注意
    "unsafe": 0      # 59点以下：非推奨
}
```

## 📊 出力形式

### コンソール出力例

```
🛡️ NSFK? (Not Safe For Kids?) - Prototype
============================================================
📋 ANALYSIS RESULTS
============================================================
🎬 Video: 子供向け教育動画 - 算数の基礎
⏱️ Duration: 300s | Processing: 45s

✅ Safety Score: 85/100
🎯 Recommendation: 推奨

📝 Summary: 教育的で年齢に適したコンテンツです。暴力的・性的な内容は含まれていません。

✅ Positive Aspects:
   • 教育的価値が高い
   • 年齢に適した内容
   • 清潔で安全な環境

🏷️ Keywords: 教育, 算数, 学習, 子供
```

### ファイル出力

- `results/nsfk_analysis_[VIDEO_ID]_[TIMESTAMP].json` - 詳細な分析データ（JSON形式）
- `results/nsfk_analysis_[VIDEO_ID]_[TIMESTAMP].txt` - 人間が読みやすい形式

## ⚙️ パフォーマンス仕様

- **処理時間**: 動画時間の1.5-2倍程度
- **コスト**: 1動画あたり$0.10-0.50（動画長・シーン数による）
- **対応動画**: 最大15分程度（プロトタイプ制限）

## 🛡️ 安全性評価項目

### 評価カテゴリ

1. **暴力的内容** (25点満点)
   - 武器、喧嘩、怪我、血液表現
   
2. **性的内容** (25点満点)
   - 不適切な露出、性的な表現
   
3. **不適切な言語** (25点満点)
   - 暴言、差別用語、不適切な表現
   
4. **薬物・アルコール** (25点満点)
   - 飲酒、喫煙、薬物使用

### スコア判定

- **80-100点**: ✅ 推奨 - 子供に安全
- **60-79点**: ⚠️ 注意 - 親の判断が必要
- **0-59点**: ❌ 非推奨 - 子供には不適切

## 🔧 トラブルシューティング

### よくある問題

1. **"OPENAI_API_KEY not set" エラー**
   ```bash
   # config.pyでAPIキーを設定してください
   OPENAI_API_KEY = "sk-your-key-here"
   ```

2. **動画ダウンロード失敗**
   ```bash
   # URLを確認、または動画IDのみを試してください
   python main.py "dQw4w9WgXcQ"
   ```

3. **Whisperモデル読み込み失敗**
   ```bash
   # インターネット接続を確認、モデルサイズを下げてみてください
   WHISPER_MODEL = "base"  # config.pyで設定
   ```

4. **メモリ不足**
   ```bash
   # 設定値を下げてください
   MAX_SCENES = 10
   WHISPER_MODEL = "base"
   ```

### ログとデバッグ

デバッグモードを有効にするには：

```python
# config.py
DEBUG = True
VERBOSE = True
```

## 📈 今後の改善予定

### Phase 2での拡張予定

- [ ] Chrome Extension統合
- [ ] リアルタイムUI
- [ ] YouTubeコメント分析
- [ ] Reddit/Wikipedia関連データ分析
- [ ] 処理速度最適化（GPU対応）

### プロトタイプの制限

- Chrome Extension未対応
- 外部データ（コメント等）未対応
- 長時間動画の制限
- 単一動画のみ対応

## 📝 開発情報

- **バージョン**: prototype-v1.0
- **作成日**: 2024年6月13日
- **ベース**: Reference.mdのサンプルコード
- **主要技術**: OpenAI GPT-4o-mini, Whisper, PySceneDetect, yt-dlp

## 📞 サポート

問題や質問がある場合は、以下を確認してください：

1. `config.py`の設定が正しいか
2. OpenAI APIキーが有効か
3. 依存関係が正しくインストールされているか
4. インターネット接続が安定しているか

---

**⚠️ 注意事項**
- このプロトタイプは検証目的です
- 実際の使用時は結果を人間が確認してください
- OpenAI APIの使用料金にご注意ください