# YouTube Transcript Downloader - Specification

## Overview

Self-contained Python script using UV inline script dependencies to download YouTube video transcripts with intelligent language fallback.

## Purpose

Command-line tool that downloads transcripts from YouTube videos without requiring manual Python virtual environment management or dependency installation.

## UV Tool Integration

### Why UV?

- **Self-contained**: Dependencies declared in script header using inline metadata
- **No virtual env management**: UV handles isolation automatically
- **Single file deployment**: Script + dependencies declared in one file
- **Portable**: Works anywhere UV is installed
- **Fast**: Rust-based dependency resolver
- **Zero setup**: No pip install, no requirements.txt, no venv commands

### UV Inline Script Format

```python
#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "youtube-transcript-api",
# ]
# ///
```

## Core Functionality

1. Accept YouTube URL as command-line parameter
2. Retrieve transcript with smart language fallback strategy
3. Output transcript to stdout or file
4. Report which language was retrieved for transparency
5. List available languages on request

## Technical Requirements

- **Tool**: UV (installed globally on system)
- **Language**: Python 3.x
- **Dependencies**: Declared inline via UV script metadata block
- **Primary Library**: youtube-transcript-api
- **Execution**: `./yt-transcript.py <url>` or `uv run yt-transcript.py <url>`
- **Standard Library**: argparse (CLI), sys (exit codes)

## User Interface

### Basic Usage

```bash
# Download transcript (English with auto-fallback)
./yt-transcript.py <youtube-url>

# Explicit language selection
./yt-transcript.py <youtube-url> --lang hu

# List available transcript languages
./yt-transcript.py <youtube-url> --list-languages

# Save to file instead of stdout
./yt-transcript.py <youtube-url> --output transcript.txt
```

### Input Format

**Supported URL formats**:
- Full URL: `https://www.youtube.com/watch?v=VIDEO_ID`
- Short URL: `https://youtu.be/VIDEO_ID`
- Video ID only: `VIDEO_ID`

## Language Handling Strategy

### Smart Fallback Chain

1. **Default behavior** (no `--lang` flag):
   - Try English (prefer manual over auto-generated)
   - If English unavailable, use first available language
   - Report which language was actually retrieved

2. **Explicit language** (`--lang <code>`):
   - Request specific language code (e.g., `hu`, `de`, `fr`)
   - Error if requested language unavailable
   - Show available languages in error message

3. **Language discovery** (`--list-languages`):
   - Display all available transcript languages
   - Show whether manual or auto-generated
   - Exit without downloading

### Transparency

Always inform user which language was retrieved:
```
ℹ️  Retrieved transcript: English (auto-generated)
ℹ️  Retrieved transcript: Hungarian (English unavailable)
```

## Output Format

### Standard Output (stdout)

```
ℹ️  Retrieved transcript: English (manual)
---
[00:00:00] Welcome to this video...
[00:00:15] Today we'll discuss...
```

### File Output (--output)

Same format written to specified file.

### Language List Output (--list-languages)

```
Available transcripts for video VIDEO_ID:
  - en (English) [auto-generated]
  - hu (Hungarian) [manual]
  - de (German) [auto-generated]
```

## Success Criteria

- ✅ UV inline dependencies work without manual setup
- ✅ Script executable directly with shebang (`chmod +x`)
- ✅ Valid YouTube URL → transcript downloaded
- ✅ English unavailable → automatic fallback + notification
- ✅ `--list-languages` → display all available transcripts
- ✅ `--lang <code>` → retrieve specific language
- ✅ `--output <file>` → save to file instead of stdout
- ✅ Clear error messages for all failure cases

## Error Handling

### Installation Errors
- **UV not installed**: Clear installation instructions
  ```
  Error: UV not found. Install with:
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### Input Errors
- **No URL provided**: Usage message with examples
- **Invalid YouTube URL**: Clear validation error message
- **Malformed URL**: Suggest correct format

### Transcript Errors
- **No transcripts available**: "No transcripts available for this video"
- **Requested language unavailable**: Show available languages
- **Video not accessible**: "Video is private, deleted, or unavailable"

### Network Errors
- **API errors**: Meaningful error message with retry suggestion
- **Connection failures**: Network connectivity error

### Output Errors
- **File write permission**: Clear permission error
- **Disk space**: Storage error message

## Dependencies

### External (UV-managed)
- `youtube-transcript-api`: Core transcript retrieval functionality

### Standard Library
- `argparse`: Command-line argument parsing
- `sys`: Exit codes and stderr output
- `pathlib`: File path handling (if needed)

## Installation Requirements

### User Prerequisites
- UV installed on system
- No Python virtual environment needed
- No pip install commands
- No manual dependency management

### First Run Experience
1. User runs `./yt-transcript.py <url>`
2. UV automatically fetches dependencies
3. UV creates isolated environment
4. Script executes with all dependencies available

Subsequent runs use cached dependencies (fast execution).

## Advantages of UV Approach

- **Zero setup**: No venv, no pip install, no requirements.txt
- **Reproducible**: Dependencies locked in script metadata
- **Portable**: Share single file, works anywhere with UV
- **Fast**: UV's Rust-based resolver (10-100x faster than pip)
- **Isolated**: Each script has its own environment
- **Version controlled**: Single file to track in git

## Project Structure

```
yt-transcript/
├── spec.md              # This specification
└── yt-transcript.py     # Self-contained executable script
```

**No additional files needed**:
- ❌ No `requirements.txt`
- ❌ No `pyproject.toml`
- ❌ No `venv/` directory
- ❌ No `.gitignore` for Python artifacts

## Claude Code Integration

### Slash Command: `/load-yt-transcript`

**Purpose**: Load YouTube video transcript into Claude Code context for AI-assisted analysis and processing.

**Description**: Downloads a YouTube video transcript using `yt-transcript.py` and automatically loads it into the active conversation context, enabling immediate analysis, summarization, translation, or other AI-powered operations without manual file management.

### Command Features

**Core Functionality**:
1. **Load into context**: Download transcript and load into conversation for immediate analysis
2. **List languages**: Display all available transcript languages for a video
3. **Specify language**: Download transcript in a specific language (e.g., Spanish, Hungarian, German)
4. **Save to file**: Optionally save transcript to a file while loading into context

### Usage Examples

```bash
# Load transcript into context (English with auto-fallback)
/load-yt-transcript https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Load transcript with video ID only
/load-yt-transcript dQw4w9WgXcQ

# List available transcript languages
/load-yt-transcript https://www.youtube.com/watch?v=dQw4w9WgXcQ --list-languages

# Load specific language transcript
/load-yt-transcript https://www.youtube.com/watch?v=dQw4w9WgXcQ --lang es

# Load transcript and save to file
/load-yt-transcript https://www.youtube.com/watch?v=dQw4w9WgXcQ --output transcript.txt

# Load Spanish transcript and save to file
/load-yt-transcript dQw4w9WgXcQ --lang es --output spanish-transcript.txt
```

### Command Arguments

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `url` | Yes | YouTube URL or video ID | `https://www.youtube.com/watch?v=dQw4w9WgXcQ` or `dQw4w9WgXcQ` |
| `--list-languages` | No | List available transcript languages and exit | `--list-languages` |
| `--lang CODE` | No | Download specific language (e.g., en, es, hu, de, fr) | `--lang hu` |
| `--output FILE` | No | Save transcript to file (still loads into context) | `--output transcript.txt` |

### Workflow Examples

**Basic Usage - Load and Analyze**:
```
User: /load-yt-transcript https://www.youtube.com/watch?v=dQw4w9WgXcQ
Claude: ✅ Loaded YouTube transcript into context
        • Video ID: dQw4w9WgXcQ
        • Language: English (auto-generated)
        • Duration: ~8 minutes (156 lines)

        What would you like me to do with this transcript?

User: Summarize the main points in 3 bullet points
Claude: [Provides concise summary from loaded transcript]
```

**Check Available Languages**:
```
User: /load-yt-transcript dQw4w9WgXcQ --list-languages
Claude: Available transcripts for video dQw4w9WgXcQ:
        • en (English) [auto-generated]
        • es (Spanish) [auto-generated]
        • hu (Hungarian) [manual]
        • de (German) [auto-generated]

        Use --lang CODE to load a specific language.
```

**Load Specific Language**:
```
User: /load-yt-transcript dQw4w9WgXcQ --lang hu
Claude: ✅ Loaded Hungarian transcript into context
        • Video ID: dQw4w9WgXcQ
        • Language: Hungarian (manual)
        • Duration: ~8 minutes (143 lines)

        Ready for analysis, translation, or any other task.
```

**Load and Save to File**:
```
User: /load-yt-transcript dQw4w9WgXcQ --lang es --output spanish-transcript.txt
Claude: ✅ Loaded Spanish transcript into context
        💾 Saved to: spanish-transcript.txt
        • Video ID: dQw4w9WgXcQ
        • Language: Spanish (auto-generated)
        • Duration: ~8 minutes (149 lines)

        Transcript is now available in context and saved to file.
```

### Benefits

- **Zero friction**: No manual download/upload/file management steps
- **Context persistence**: Transcript stays loaded for multiple operations
- **Language flexibility**: List available languages, choose specific language
- **File preservation**: Optionally save transcript while keeping it in context
- **Flexible analysis**: Summarize, translate, extract, compare, annotate
- **Seamless integration**: Full feature parity with underlying `yt-transcript.py` script

### Technical Implementation

- **Command definition**: `.claude/commands/load-yt-transcript.md`
- **Script execution**: Calls `yt-transcript.py` via Bash tool with appropriate arguments
- **Context loading**: Uses Read tool to load transcript into conversation context
- **Feature parity**: Supports all flags from underlying Python script:
  - `--list-languages`: Display available transcripts
  - `--lang CODE`: Specify language
  - `--output FILE`: Save to file
- **Error handling**: Propagates clear error messages from script (unavailable video, missing language, etc.)

### Use Cases

1. **Content Analysis**: Summarize video content without watching
2. **Translation**: Translate transcript to other languages
3. **Quote Extraction**: Find and extract specific quotes or statements
4. **Technical Documentation**: Extract code examples, commands, or technical details
5. **Language Learning**: Analyze content in non-native languages
6. **Accessibility**: Convert video content to readable text format
7. **Research**: Analyze multiple video transcripts for patterns or themes
8. **SEO/Content**: Extract keywords, topics, and themes from video content

## Future Enhancements (Out of Scope v1)

- Subtitle format options (SRT, VTT, JSON)
- Batch processing multiple URLs (`/load-yt-transcript video1,video2,video3`)
- Timestamp formatting options
- Translation between languages within command
- Authentication for private videos
- Progress indicators for long videos
- `/compare-yt-transcripts` command for multi-video analysis
- Automatic chapter detection and per-section summarization
- Export analyzed content to various formats (Markdown, PDF, etc.)

## References

- UV Documentation: https://docs.astral.sh/uv/
- UV Inline Scripts: https://docs.astral.sh/uv/guides/scripts/
- youtube-transcript-api: https://github.com/jdepoix/youtube-transcript-api
- Claude Code Custom Commands: https://docs.claude.com/en/docs/claude-code/custom-commands
