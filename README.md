# YouTube Transcript Loader for Claude Code

A Claude Code slash command that downloads YouTube video transcripts and loads them directly into your conversation context for AI-assisted analysis.

## What This Does

- Downloads transcripts from any YouTube video
- Loads the transcript text into Claude Code automatically
- Supports multiple languages
- Works with a simple `/load-yt-transcript` command

Perfect for: summarizing videos, translating content, extracting insights, or analyzing spoken content with AI assistance.

## Prerequisites

You need these installed on your computer:

1. **Claude Code** - [Download from claude.ai/code](https://claude.ai/code)
2. **UV** - Python package installer ([installation instructions](https://docs.astral.sh/uv/getting-started/installation/))

### Installing UV (Quick Guide)

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Installation

### Option 1: Quick Install (Copy Files)

1. **Download this repository** (click the green "Code" button → "Download ZIP")

2. **Locate your Claude Code global commands folder:**
   - **macOS/Linux:** `~/.claude/commands/`
   - **Windows:** `%USERPROFILE%\.claude\commands\`

3. **Copy the command file:**
   ```bash
   # Create the directory if it doesn't exist
   mkdir -p ~/.claude/commands/

   # Copy the command file
   cp .claude/commands/load-yt-transcript.json ~/.claude/commands/
   ```

4. **Copy the script to your path:**
   ```bash
   # macOS/Linux - choose one location:
   sudo cp yt-transcript.py /usr/local/bin/yt-transcript
   # OR
   cp yt-transcript.py ~/bin/yt-transcript

   # Make it executable
   chmod +x /usr/local/bin/yt-transcript  # or ~/bin/yt-transcript
   ```

   ```powershell
   # Windows - copy to a location in your PATH
   # Example: C:\Users\YourName\bin\
   copy yt-transcript.py %USERPROFILE%\bin\yt-transcript.py
   ```

### Option 2: Git Clone (For Developers)

```bash
# Clone the repository
git clone https://github.com/yourusername/claude-code-yt-transcript.git
cd claude-code-yt-transcript

# Create global commands directory
mkdir -p ~/.claude/commands/

# Symlink the command (automatically updates with git pulls)
ln -s "$(pwd)/.claude/commands/load-yt-transcript.json" ~/.claude/commands/

# Install script globally
sudo ln -s "$(pwd)/yt-transcript.py" /usr/local/bin/yt-transcript
chmod +x yt-transcript.py
```

## Usage

### In Claude Code

Once installed, use the command anywhere in Claude Code:

```bash
# Load a transcript into the conversation
/load-yt-transcript "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Just the video ID works too
/load-yt-transcript "dQw4w9WgXcQ"

# List available languages first
/load-yt-transcript "VIDEO_ID" --list-languages

# Load a specific language
/load-yt-transcript "VIDEO_ID" --lang es

# Save to a file (and load into context)
/load-yt-transcript "VIDEO_ID" --output transcript.txt
```

After the transcript loads, you can ask Claude to:
- "Summarize this video"
- "Translate this to Spanish"
- "Extract the key points"
- "Create a blog post from this content"

### Standalone Script

You can also use the script directly in your terminal:

```bash
# Download and display transcript
yt-transcript "https://www.youtube.com/watch?v=VIDEO_ID"

# List available languages
yt-transcript "VIDEO_ID" --list-languages

# Download specific language
yt-transcript "VIDEO_ID" --lang es

# Save to file
yt-transcript "VIDEO_ID" --output transcript.txt
```

## Troubleshooting

### Command not found in Claude Code

1. Check that the file is in the correct location:
   ```bash
   ls ~/.claude/commands/load-yt-transcript.json
   ```

2. Restart Claude Code

3. Verify the JSON file is valid:
   ```bash
   cat ~/.claude/commands/load-yt-transcript.json | python -m json.tool
   ```

### Script not found (`yt-transcript: command not found`)

1. Check if the script is in your PATH:
   ```bash
   which yt-transcript
   ```

2. Make sure it's executable:
   ```bash
   chmod +x /usr/local/bin/yt-transcript
   ```

3. Verify UV is installed:
   ```bash
   uv --version
   ```

### No transcripts available

Some videos don't have transcripts. Try:
- Videos with auto-generated captions (most English videos)
- Videos with manual captions/subtitles
- Use `--list-languages` to see what's available

### Permission denied

On macOS/Linux, you might need to use `sudo`:
```bash
sudo cp yt-transcript.py /usr/local/bin/yt-transcript
```

Or use a user-writable location like `~/bin/` (make sure it's in your PATH).

## How It Works

1. The Claude Code command runs the Python script
2. The script uses `youtube-transcript-api` to fetch transcripts
3. The transcript text is automatically loaded into your Claude Code conversation
4. You can immediately ask questions or request analysis

**No configuration files needed** - dependencies are managed automatically by UV inline script system.

## Features

- ✅ Zero configuration - works immediately after installation
- ✅ Automatic dependency management (UV handles everything)
- ✅ Multiple language support
- ✅ Smart fallback (English → first available)
- ✅ Direct integration with Claude Code
- ✅ Standalone script also works in terminal

## Files

- **`.claude/commands/load-yt-transcript.json`** - Claude Code slash command definition
- **`yt-transcript.py`** - Main Python script (UV inline dependencies)
- **`spec.md`** - Complete technical specification
- **`CLAUDE.md`** - Development guide for Claude Code

## Contributing

See `CLAUDE.md` for development guidelines and architecture details.

## License

MIT License - feel free to use and modify as needed.
