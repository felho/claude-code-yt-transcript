# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**yt-transcript** is a single-file UV-based Python script for downloading YouTube video transcripts. The entire project consists of one executable script (`yt-transcript.py`) with zero external configuration files.

### UV Inline Script Architecture

This project uses UV's inline script dependency system - **no virtual environments, no requirements.txt, no pyproject.toml**. Dependencies are declared directly in the script header:

```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "youtube-transcript-api",
# ]
# ///
```

On first run, UV automatically:
1. Fetches dependencies
2. Creates isolated environment
3. Executes script

Subsequent runs use cached dependencies.

## Development Commands

### Claude Code Integration (Recommended)

This project includes a Claude Code slash command for seamless transcript loading:

```bash
# Load transcript into Claude Code context
/load-yt-transcript "https://www.youtube.com/watch?v=VIDEO_ID"

# List available languages
/load-yt-transcript "VIDEO_ID" --list-languages

# Load specific language
/load-yt-transcript "VIDEO_ID" --lang es

# Load and save to file
/load-yt-transcript "VIDEO_ID" --output transcript.txt
```

**Command location**: `.claude/commands/load-yt-transcript.md`

**Benefits**: Automatically loads transcript into conversation context for immediate AI-assisted analysis, summarization, translation, or other processing.

See `spec.md` for complete command documentation and workflow examples.

### Testing the Script Directly

```bash
# Basic usage - download transcript
./yt-transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Alternative: using uv run directly
uv run yt-transcript.py "VIDEO_ID"

# List available languages
./yt-transcript.py "VIDEO_ID" --list-languages

# Download specific language
./yt-transcript.py "VIDEO_ID" --lang es

# Save to file
./yt-transcript.py "VIDEO_ID" --output transcript.txt
```

### URL Format Support

The script accepts three formats:
- Full URL: `https://www.youtube.com/watch?v=VIDEO_ID`
- Short URL: `https://youtu.be/VIDEO_ID`
- Video ID only: `VIDEO_ID`

### Making Changes

Since dependencies are inline, modifications to the script don't require any environment setup:

1. Edit `yt-transcript.py`
2. Run `./yt-transcript.py <test-url>` - UV handles everything

To add new dependencies, update the `# dependencies = [...]` section in the script header.

## Code Architecture

### Core Components

**`extract_video_id(url_or_id)`**
- Handles three YouTube URL formats using regex patterns
- Returns 11-character video ID or None

**`list_available_languages(video_id)`**
- Uses `YouTubeTranscriptApi().list()` to retrieve transcript metadata
- Displays language codes, names, and type (manual/auto-generated)

**`get_transcript(video_id, language_code=None)`**
- Smart fallback: English (manual preferred) → first available
- Uses `api.list()` + `transcript_list.find_transcript()` + `transcript.fetch()`
- Returns tuple: (transcript_data, language_info)

**`format_transcript(transcript_data, language_info)`**
- Accesses FetchedTranscriptSnippet attributes: `.start`, `.text`, `.duration`
- Formats timestamps as `[HH:MM:SS]`
- NOT dict-based - uses dataclass attributes

### youtube-transcript-api Usage Pattern

**Critical**: This library uses instance methods, not class methods:

```python
# CORRECT
api = YouTubeTranscriptApi()
transcript_list = api.list(video_id)
transcript = transcript_list.find_transcript(['en'])
data = transcript.fetch()  # Returns FetchedTranscript (iterable of FetchedTranscriptSnippet objects)

# Access snippet attributes
for snippet in data:
    timestamp = snippet.start  # NOT snippet['start']
    text = snippet.text        # NOT snippet['text']
```

### Error Handling Strategy

Uses specific exception types from `youtube_transcript_api._errors`:
- `TranscriptsDisabled` - Transcripts disabled for video
- `NoTranscriptFound` - Requested language unavailable
- `VideoUnavailable` - Video private/deleted/restricted

All error messages go to stderr, exit codes indicate failure.

## Important Notes

### Project Structure

```
claude-code-yt-transcript/
├── .claude/
│   └── commands/
│       └── load-yt-transcript.md    # Claude Code slash command
├── CLAUDE.md                        # This file
├── spec.md                          # Complete specification
└── yt-transcript.py                 # Main executable script
```

### Single-File Core

The core functionality is intentionally a single executable file. Do NOT create:
- ❌ `requirements.txt`
- ❌ `pyproject.toml`
- ❌ Virtual environment directories
- ❌ Separate config files (except Claude Code commands in `.claude/`)

### Shebang Requirement

The script must start with `#!/usr/bin/env -S uv run --script` to be directly executable. The `--script` flag prevents recursive invocation when run via symlink. Maintain execute permissions with `chmod +x yt-transcript.py`.

### Testing Changes

Always test with actual YouTube videos. The API behavior differs from mock data, particularly:
- FetchedTranscriptSnippet is a dataclass, not a dict
- Transcript lists are iterable objects with specific methods
- Language metadata structure varies

See `spec.md` for complete functional requirements and success criteria.
