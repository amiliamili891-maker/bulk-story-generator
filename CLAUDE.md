# Bulk Story Generator

## YouTube Transcription

This project includes a YouTube transcription skill for analyzing video content.

### Quick Start
```bash
pip install -r requirements.txt
python3 tools/youtube_transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### MCP Server
An MCP server for YouTube transcripts is configured in `.claude/settings.json`.
It uses `@sinco-lab/mcp-youtube-transcript` for direct Claude Code integration.

### Skill Reference
See `.claude/skills/youtube-transcribe.md` for full usage documentation.
