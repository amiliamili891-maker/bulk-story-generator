# YouTube Transcription Skill

## Description
Transcribe YouTube videos to extract their full text content for analysis. Supports auto-generated and manual captions, multiple languages, and translation.

## When to Use
- User provides a YouTube URL and wants the transcript/content
- User wants to analyze a YouTube video's content
- User asks to "transcribe", "get transcript", or "get subtitles" from YouTube

## How to Use

### Quick transcript (plain text)
```bash
python3 tools/youtube_transcribe.py "YOUTUBE_URL"
```

### With timestamps
```bash
python3 tools/youtube_transcribe.py "YOUTUBE_URL" --timestamps
```

### As JSON (with start times and durations)
```bash
python3 tools/youtube_transcribe.py "YOUTUBE_URL" --format json
```

### List available languages
```bash
python3 tools/youtube_transcribe.py "YOUTUBE_URL" --list-langs
```

### Specific language or translation
```bash
python3 tools/youtube_transcribe.py "YOUTUBE_URL" --lang es
python3 tools/youtube_transcribe.py "YOUTUBE_URL" --translate fr
```

### Save to file
```bash
python3 tools/youtube_transcribe.py "YOUTUBE_URL" --output transcript.txt
```

## Workflow for Video Analysis
1. Fetch the transcript using this tool
2. Read/analyze the transcript content
3. Provide insights, summaries, or answers based on the video content

## Dependencies
- Python 3.x
- `youtube-transcript-api` package (`pip install youtube-transcript-api`)

## Limitations
- Only works with videos that have captions (manual or auto-generated)
- May be blocked by YouTube when running from cloud IPs (use proxies if needed)
- Age-restricted videos may not be accessible
