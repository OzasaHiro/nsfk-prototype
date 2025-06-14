#!/bin/bash

# NSFK? プロトタイプ環境セットアップスクリプト

echo "🛡️ NSFK? Prototype Environment Setup"
echo "======================================"

# 仮想環境の確認
if [ ! -d "nsfk_env" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv nsfk_env
else
    echo "✅ Virtual environment already exists"
fi

# 仮想環境のアクティベート
echo "🔄 Activating virtual environment..."
source nsfk_env/bin/activate

# pipのアップグレード
echo "📈 Upgrading pip..."
pip install --upgrade pip

# 基本パッケージのインストール
echo "📚 Installing basic packages..."
pip install yt-dlp scenedetect opencv-python openai requests numpy

# Whisperのインストール（少し時間がかかる場合があります）
echo "🎧 Installing OpenAI Whisper..."
pip install git+https://github.com/openai/whisper.git

# PyTorchのインストール（Whisperに必要）
echo "🔥 Installing PyTorch..."
pip install torch torchvision torchaudio

# 設定確認
echo "⚙️ Testing configuration..."
python test_config.py

echo ""
echo "✅ Setup completed!"
echo ""
echo "📝 Next steps:"
echo "1. Edit config.py and set your OpenAI API key"
echo "2. Activate environment: source nsfk_env/bin/activate"
echo "3. Run prototype: python main.py"
echo ""
echo "🔑 Don't forget to set your OpenAI API key in config.py!"
echo "   OPENAI_API_KEY = \"sk-your-api-key-here\""