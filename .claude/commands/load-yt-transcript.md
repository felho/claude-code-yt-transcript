---
description: Load YouTube video transcript into context for AI-assisted analysis and processing
argument-hint: <url> [--list-languages] [--lang CODE] [--output FILE]
allowed-tools: Bash(yt-transcript:*), Bash(./yt-transcript.py:*), Bash(/usr/local/bin/yt-transcript:*)
---

You are helping the user load a YouTube video transcript into Claude Code's context for analysis and processing.

# Task Overview

Execute the yt-transcript.py script to download a YouTube video transcript and load it into the conversation context.

# Arguments Provided

Arguments: $ARGUMENTS

# Execution Steps

1. **Parse arguments**:

   - Extract URL/video ID from first argument
   - Check for flags: --list-languages, --lang, --output

2. **Construct the command**:

   - Try `yt-transcript` first (if installed globally via symlink)
   - Fall back to `/usr/local/bin/yt-transcript` if in PATH
   - Fall back to `./yt-transcript.py` if executing from project directory
   - Add any flags from remaining arguments

3. **Execute the script** using the Bash tool

4. **Handle the output**:

   **If --list-languages flag is present**:

   - Display available languages to the user
   - Suggest using `--lang CODE` to load a specific language

   **Otherwise**:

   - Capture the transcript output from stdout (script prints to stdout by default)
   - Parse the first line to extract language information
   - Count the lines to estimate transcript length
   - Calculate approximate duration from timestamps if possible
   - Provide a summary to the user:
     ```
     ✅ Loaded YouTube transcript into context
     • Video ID: [extracted from URL]
     • Language: [from transcript]
     • Duration: [estimated from timestamps]
     • Lines: [count]
     ```
   - If --output file was specified, note where it was saved
   - Ask the user what they'd like to do with the transcript
   - Keep the transcript output in context for further operations

5. **Error handling**:
   - If the script fails, display the error message from stderr
   - Common errors:
     - Invalid URL/video ID
     - Transcripts disabled for video
     - Requested language not available
     - Video unavailable/private
   - Provide helpful suggestions based on the error

# Important Notes

- Be concise in your response
- The transcript output is automatically in context from stdout
- Always extract and display metadata (language, duration, line count)
- Be ready to perform analysis, summarization, translation, or extraction tasks on the loaded transcript
