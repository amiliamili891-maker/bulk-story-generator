#!/usr/bin/env python3
"""YouTube Video Transcription Tool

Fetches transcripts/subtitles from YouTube videos for analysis.
Supports manual captions, auto-generated subtitles, and translation.

Usage:
    python3 tools/youtube_transcribe.py <youtube_url_or_video_id> [options]

Options:
    --lang LANG        Preferred language code (default: en)
    --translate LANG   Translate transcript to this language
    --format FORMAT    Output format: text, json, srt (default: text)
    --timestamps       Include timestamps in text output
    --list-langs       List available transcript languages
    --output FILE      Write output to file instead of stdout
"""

import sys
import json
import re
import argparse
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter


def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from various YouTube URL formats or raw ID."""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url_or_id}")


def list_available_languages(video_id: str) -> list[dict]:
    """List all available transcript languages for a video."""
    ytt = YouTubeTranscriptApi()
    transcript_list = ytt.list(video_id)
    languages = []
    for transcript in transcript_list:
        languages.append({
            "language": transcript.language,
            "language_code": transcript.language_code,
            "is_generated": transcript.is_generated,
            "is_translatable": transcript.is_translatable,
        })
    return languages


def fetch_transcript(video_id: str, lang: str = "en", translate_to: str = None) -> list[dict]:
    """Fetch transcript for a video, with optional translation."""
    ytt = YouTubeTranscriptApi()
    transcript_list = ytt.list(video_id)

    # Try to find the requested language
    try:
        transcript = transcript_list.find_transcript([lang])
    except Exception:
        # Fall back to any available transcript
        try:
            transcript = transcript_list.find_transcript(["en"])
        except Exception:
            # Get the first available transcript
            transcript = next(iter(transcript_list))

    # Translate if requested
    if translate_to:
        transcript = transcript.translate(translate_to)

    fetched = transcript.fetch()
    return fetched.to_raw_data()


def format_as_text(transcript_data: list[dict], include_timestamps: bool = False) -> str:
    """Format transcript as plain readable text."""
    lines = []
    for entry in transcript_data:
        if include_timestamps:
            start = entry["start"]
            minutes = int(start // 60)
            seconds = int(start % 60)
            lines.append(f"[{minutes:02d}:{seconds:02d}] {entry['text']}")
        else:
            lines.append(entry["text"])
    return "\n".join(lines)


def format_as_json(transcript_data: list[dict]) -> str:
    """Format transcript as JSON."""
    return json.dumps(transcript_data, indent=2, ensure_ascii=False)


def format_as_srt(transcript_data: list[dict]) -> str:
    """Format transcript as SRT subtitle format."""
    lines = []
    for i, entry in enumerate(transcript_data, 1):
        start = entry["start"]
        end = start + entry.get("duration", 0)
        lines.append(str(i))
        lines.append(f"{_srt_time(start)} --> {_srt_time(end)}")
        lines.append(entry["text"])
        lines.append("")
    return "\n".join(lines)


def _srt_time(seconds: float) -> str:
    """Convert seconds to SRT time format HH:MM:SS,mmm."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    parser = argparse.ArgumentParser(
        description="Fetch YouTube video transcripts for analysis"
    )
    parser.add_argument(
        "video",
        help="YouTube URL or video ID"
    )
    parser.add_argument(
        "--lang", default="en",
        help="Preferred language code (default: en)"
    )
    parser.add_argument(
        "--translate",
        help="Translate transcript to this language code"
    )
    parser.add_argument(
        "--format", choices=["text", "json", "srt"], default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--timestamps", action="store_true",
        help="Include timestamps in text output"
    )
    parser.add_argument(
        "--list-langs", action="store_true",
        help="List available transcript languages"
    )
    parser.add_argument(
        "--output",
        help="Write output to file"
    )

    args = parser.parse_args()

    try:
        video_id = extract_video_id(args.video)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # List languages mode
    if args.list_langs:
        try:
            languages = list_available_languages(video_id)
            print(f"Available transcripts for video {video_id}:\n")
            for lang in languages:
                generated = " (auto-generated)" if lang["is_generated"] else ""
                translatable = " [translatable]" if lang["is_translatable"] else ""
                print(f"  {lang['language_code']:>5}  {lang['language']}{generated}{translatable}")
        except Exception as e:
            print(f"Error listing languages: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # Fetch transcript
    try:
        transcript_data = fetch_transcript(video_id, args.lang, args.translate)
    except Exception as e:
        print(f"Error fetching transcript: {e}", file=sys.stderr)
        sys.exit(1)

    # Format output
    if args.format == "json":
        output = format_as_json(transcript_data)
    elif args.format == "srt":
        output = format_as_srt(transcript_data)
    else:
        output = format_as_text(transcript_data, args.timestamps)

    # Write output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Transcript written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
