# NSFK? (Not Safe For Kids?) - Prototype

An AI-powered YouTube video safety analyzer that helps busy parents determine if video content is appropriate for their children.

## 🎯 Overview

This prototype provides the following features:

- ✅ Automatic YouTube video download and processing
- ✅ Scene detection and visual analysis (GPT-4o-mini)
- ✅ Audio transcription and analysis (OpenAI Whisper)
- ✅ Child safety scoring system (0-100 points)
- ✅ Comprehensive safety reports generation

## 📁 Project Structure

```
nsfk-prototype/
├── main.py              # Main execution file
├── config.py           # Configuration settings
├── youtube_downloader.py # YouTube video download functionality
├── video_analyzer.py    # Video analysis (visual + audio)
├── safety_scorer.py     # Safety scoring and evaluation
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore patterns
├── videos/             # Downloaded videos (temporary)
├── images/             # Extracted frames (temporary)
└── results/            # Analysis results
```

## 🚀 Setup

### 1. Install Dependencies

```bash
git clone https://github.com/OzasaHiro/nsfk-prototype.git
cd nsfk-prototype
pip install -r requirements.txt
```

### 2. OpenAI API Key Configuration

Copy `.env.example` to `.env` and set your API key:

```bash
cp .env.example .env
```

Edit the `.env` file:

```bash
# .env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

Alternatively, set as environment variable:

```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

## 📖 Usage

### Basic Usage

```bash
python main.py
```

After execution, enter a YouTube URL or video ID when prompted.

### YouTube Video Input Formats

The following formats are supported:

```bash
# 1. Full URL
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# 2. Short URL
python main.py "https://youtu.be/dQw4w9WgXcQ"

# 3. Video ID only (11 characters)
python main.py "dQw4w9WgXcQ"

# 4. Interactive input
python main.py
# → Enter URL at prompt

# 5. Quick analysis (simplified version)
python quick_analyze.py "dQw4w9WgXcQ"
```

### Configuration Customization

Adjust settings in `config.py`:

```python
# Analysis precision vs speed/cost trade-off
SCENE_THRESHOLD = 60.0   # Higher value = fewer scenes = faster/cheaper
MAX_SCENES = 20          # Maximum scenes to analyze
WHISPER_MODEL = "base"   # Whisper model (base/small/medium/large)
MAX_TOKENS = 5000        # GPT maximum tokens

# Safety evaluation thresholds
SCORE_THRESHOLDS = {
    "safe": 80,      # 80+ points: Recommended
    "caution": 60,   # 60-79 points: Caution advised
    "unsafe": 0      # 0-59 points: Not recommended
}
```

## 📊 Output Format

### Console Output Example

```
🛡️ NSFK? (Not Safe For Kids?) - Prototype
============================================================
📋 ANALYSIS RESULTS
============================================================
🎬 Video: Educational Video for Kids - Math Basics
⏱️ Duration: 300s | Processing: 45s

✅ Safety Score: 85/100
🎯 Recommendation: Recommended

📝 Summary: Educational content appropriate for children. No violent or sexual content detected.

✅ Positive Aspects:
   • High educational value
   • Age-appropriate content
   • Clean and safe environment

🏷️ Keywords: education, math, learning, children
```

### File Output

- `results/nsfk_analysis_[VIDEO_ID]_[TIMESTAMP].json` - Detailed analysis data (JSON format)
- `results/nsfk_analysis_[VIDEO_ID]_[TIMESTAMP].txt` - Human-readable format

## ⚙️ Performance Specifications

- **Processing Time**: Approximately 1.5-2x video duration
- **Cost**: $0.10-0.50 per video (varies by video length and scene count)
- **Supported Videos**: Up to 15 minutes (prototype limitation)

## 🛡️ Safety Evaluation Categories

### Evaluation Categories

1. **Violence** (25 points max)
   - Weapons, fighting, injuries, blood

2. **Sexual Content** (25 points max)
   - Inappropriate exposure, sexual expressions

3. **Inappropriate Language** (25 points max)
   - Profanity, hate speech, inappropriate expressions

4. **Drugs/Alcohol** (25 points max)
   - Drinking, smoking, substance use

### Score Interpretation

- **80-100 points**: ✅ Recommended - Safe for children
- **60-79 points**: ⚠️ Caution - Parental guidance advised
- **0-59 points**: ❌ Not Recommended - Inappropriate for children

## 🔧 Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY not set" Error**
   ```bash
   # Set your API key in .env file
   OPENAI_API_KEY=sk-your-key-here
   ```

2. **Video Download Failure**
   ```bash
   # Verify URL or try with video ID only
   python main.py "dQw4w9WgXcQ"
   ```

3. **Whisper Model Loading Failure**
   ```bash
   # Check internet connection, try smaller model size
   WHISPER_MODEL = "base"  # Set in config.py
   ```

4. **Memory Issues**
   ```bash
   # Reduce settings in config.py
   MAX_SCENES = 10
   WHISPER_MODEL = "base"
   ```

### Debug Mode

Enable debug mode for detailed error information:

```python
# config.py
DEBUG = True
VERBOSE = True
```

## 📈 Future Roadmap

### Phase 2 Planned Features

- [ ] Chrome Extension integration
- [ ] Real-time UI interface
- [ ] YouTube comments analysis
- [ ] Reddit/Wikipedia related data analysis
- [ ] Processing speed optimization (GPU support)

### Current Prototype Limitations

- No Chrome Extension support
- No external data analysis (comments, etc.)
- Long video processing limitations
- Single video processing only

## 📝 Development Information

- **Version**: prototype-v1.0
- **Created**: June 13, 2024
- **Base**: Reference.md sample code
- **Key Technologies**: OpenAI GPT-4o-mini, Whisper, PySceneDetect, yt-dlp

## 📞 Support

If you encounter issues or have questions, please check:

1. `config.py` settings are correct
2. OpenAI API key is valid
3. Dependencies are properly installed
4. Internet connection is stable

## 🤝 Contributing

This is a prototype for validation purposes. For production use, please review results manually and monitor OpenAI API usage costs.

## 📄 License

This project is for educational and research purposes. Please ensure compliance with YouTube's Terms of Service and OpenAI's usage policies.

---

**⚠️ Important Notes**
- This prototype is for validation purposes only
- Always verify results manually for actual use
- Monitor OpenAI API usage costs
- Ensure compliance with platform terms of service