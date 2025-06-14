# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NSFK? (Not Safe For Kids?) is an AI agent system that analyzes YouTube videos to help busy parents determine if content is appropriate for their children. The system provides:
- Quick content summaries (1-2 lines)
- Key keywords extraction  
- Safety ratings
- Analysis of video content, audio, YouTube comments, and associated search data (Reddit/Wiki links)

## Architecture

The project is designed as a Chrome Extension with the following core components:

### Video Analysis Pipeline
1. **Video Acquisition**: Uses yt-dlp to download YouTube videos
2. **Scene Detection**: PySceneDetect with ContentDetector for frame extraction
3. **Visual Analysis**: GPT-4o-mini processes extracted frames via OpenAI API
4. **Audio Analysis**: Whisper transcribes audio content to text
5. **Content Generation**: Final analysis combines visual + audio data through GPT-4o-mini

### Key Dependencies
- `yt-dlp`: YouTube video downloading
- `scenedetect`: Scene change detection and frame extraction
- `opencv-python`: Video processing and frame manipulation
- `openai-whisper`: Audio transcription
- `openai`: API client for GPT-4o-mini integration

## Development Setup

## Github
・Managed on Github: https://github.com/OzasaHiro/nsfk-prototype
　Don't forget to git pull at the start of each session
　Don't forget to git push updated files at the end of each session

### Required Environment Variables
- `OPENAI_API_KEY`: Set in both `scene_analysis.py` and `make_text.py`

### Installation
```bash
pip install -r requirements.txt
```

### Key Configuration Parameters
- `video_id` in main.py: YouTube video ID to process
- `threshold` in scene.py: Scene detection sensitivity (higher = less sensitive)
- Language setting in transcription.py: `language="ja"` for Japanese content
- Model selection in transcription.py: Default uses "small" Whisper model

## Processing Flow

1. **main.py**: Orchestrates the entire pipeline
2. **youtube_dl.py**: Downloads video using yt-dlp
3. **scene.py**: Detects scene changes and extracts key frames
4. **scene_analysis.py**: Analyzes extracted frames with GPT-4o-mini
5. **transcription.py**: Transcribes audio using Whisper
6. **make_text.py**: Combines analysis results into final content

## Performance Considerations

- Processing time approximately equals video duration on CPU-only systems
- GPU acceleration possible with PyTorch modifications
- GPT-4o-mini has 128k input token / 16k output token limits
- Cost scales with scene change frequency and response length

## Chrome Extension Integration

The current codebase focuses on the core video analysis pipeline. Chrome Extension implementation should integrate this processing system to provide:
- YouTube page integration
- Real-time content analysis
- Parent-friendly safety summaries
- Popup interface for quick access

## Output Format

Generated content is saved to `contents.txt` with customizable output based on prompts in `make_text.py`. The system can generate various content types:
- Safety summaries for parents
- Detailed content breakdowns
- Keyword extraction
- Educational content analysis