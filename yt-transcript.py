#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "youtube-transcript-api",
# ]
# ///

"""
YouTube Transcript Downloader

Self-contained script to download YouTube video transcripts with intelligent
language fallback using UV inline script dependencies.
"""

import argparse
import sys
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)


def extract_video_id(url_or_id):
    """
    Extract video ID from various YouTube URL formats.

    Supports:
    - Full URL: https://www.youtube.com/watch?v=VIDEO_ID
    - Short URL: https://youtu.be/VIDEO_ID
    - Video ID only: VIDEO_ID
    """
    # Already a video ID (11 characters, alphanumeric and some symbols)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
        return url_or_id

    # Extract from full URL
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',
    ]

    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)

    return None


def list_available_languages(video_id):
    """Display all available transcript languages for a video."""
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        print(f"Available transcripts for video {video_id}:")

        for transcript in transcript_list:
            type_label = "auto-generated" if transcript.is_generated else "manual"
            print(f"  - {transcript.language_code} ({transcript.language}) [{type_label}]")

    except TranscriptsDisabled:
        print("Error: Transcripts are disabled for this video", file=sys.stderr)
        sys.exit(1)
    except VideoUnavailable:
        print("Error: Video is private, deleted, or unavailable", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def get_transcript(video_id, language_code=None):
    """
    Retrieve transcript with smart fallback strategy.

    Returns: (transcript_data, language_info)
    """
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        if language_code:
            # Explicit language requested
            try:
                transcript = transcript_list.find_transcript([language_code])
                transcript_data = transcript.fetch()
                lang_type = "auto-generated" if transcript.is_generated else "manual"
                return transcript_data, f"{transcript.language} ({lang_type})"
            except NoTranscriptFound:
                print(f"Error: Transcript not available in '{language_code}'", file=sys.stderr)
                print("\nAvailable languages:", file=sys.stderr)
                for t in transcript_list:
                    type_label = "auto-generated" if t.is_generated else "manual"
                    print(f"  - {t.language_code} ({t.language}) [{type_label}]", file=sys.stderr)
                sys.exit(1)
        else:
            # Default behavior: Try English first, prefer manual over auto-generated
            try:
                transcript = transcript_list.find_transcript(['en'])
                transcript_data = transcript.fetch()
                lang_type = "auto-generated" if transcript.is_generated else "manual"
                return transcript_data, f"English ({lang_type})"
            except NoTranscriptFound:
                # English not available, use first available
                first_transcript = next(iter(transcript_list))
                transcript_data = first_transcript.fetch()
                lang_type = "auto-generated" if first_transcript.is_generated else "manual"
                fallback_msg = f"{first_transcript.language} ({lang_type}, English unavailable)"
                return transcript_data, fallback_msg

    except TranscriptsDisabled:
        print("Error: Transcripts are disabled for this video", file=sys.stderr)
        sys.exit(1)
    except VideoUnavailable:
        print("Error: Video is private, deleted, or unavailable", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def format_timestamp(seconds):
    """Convert seconds to [HH:MM:SS] format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"[{hours:02d}:{minutes:02d}:{secs:02d}]"


def format_transcript(transcript_data, language_info):
    """Format transcript with timestamps."""
    lines = [f"ℹ️  Retrieved transcript: {language_info}", "---"]

    for entry in transcript_data:
        timestamp = format_timestamp(entry.start)
        text = entry.text.strip()
        lines.append(f"{timestamp} {text}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Download YouTube video transcripts with smart language fallback",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://www.youtube.com/watch?v=dQw4w9WgXcQ
  %(prog)s dQw4w9WgXcQ --lang hu
  %(prog)s https://youtu.be/dQw4w9WgXcQ --output transcript.txt
  %(prog)s dQw4w9WgXcQ --list-languages
        """
    )

    parser.add_argument(
        'url',
        help='YouTube video URL or video ID'
    )

    parser.add_argument(
        '--lang',
        metavar='CODE',
        help='Language code (e.g., en, hu, de, fr)'
    )

    parser.add_argument(
        '--list-languages',
        action='store_true',
        help='List available transcript languages and exit'
    )

    parser.add_argument(
        '--output', '-o',
        metavar='FILE',
        help='Save transcript to file instead of stdout'
    )

    args = parser.parse_args()

    # Extract video ID
    video_id = extract_video_id(args.url)
    if not video_id:
        print("Error: Invalid YouTube URL or video ID", file=sys.stderr)
        print("\nSupported formats:", file=sys.stderr)
        print("  - https://www.youtube.com/watch?v=VIDEO_ID", file=sys.stderr)
        print("  - https://youtu.be/VIDEO_ID", file=sys.stderr)
        print("  - VIDEO_ID", file=sys.stderr)
        sys.exit(1)

    # List languages mode
    if args.list_languages:
        list_available_languages(video_id)
        return

    # Get transcript
    transcript_data, language_info = get_transcript(video_id, args.lang)

    # Format output
    output = format_transcript(transcript_data, language_info)

    # Write to file or stdout
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"ℹ️  Transcript saved to {args.output}", file=sys.stderr)
        except PermissionError:
            print(f"Error: Permission denied writing to {args.output}", file=sys.stderr)
            sys.exit(1)
        except OSError as e:
            print(f"Error: Failed to write file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output)


if __name__ == '__main__':
    main()
