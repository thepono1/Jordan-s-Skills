---
name: tap
description: Transcribe a video URL, analyze deeply, and store expertise in local knowledge vault
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - mcp__memory__memory_store
  - mcp__memory__memory_recall
  - mcp__memory__vault_write
  - mcp__memory__vault_search
  - mcp__memory__vault_list
---

# /tap - Transcribe, Analyze, Preserve

You are an expert knowledge extractor. Given a video URL, you will download, transcribe, analyze, and store deep expertise in the local memory vault.

## Input

Video URL: $ARGUMENTS

If no URL is provided, ask the user for one.

## Process

### Step 1: Extract Video ID and Download Audio

**CRITICAL: Use a UNIQUE temp file per video to allow parallel taps.**

Extract a short ID from the URL to create a unique filename:
- YouTube: use the video ID (e.g., `PjigwAmhiT0` from `watch?v=PjigwAmhiT0`)
- Other platforms: use the last 11 chars of an md5 hash of the URL

Set `VID` to this ID, then use `/tmp/tap_${VID}.mp3` as the temp file path.

```bash
cd ~/transcriber
source .venv/bin/activate
# Remove any existing file for this video ID
rm -f "/tmp/tap_${VID}.mp3" "/tmp/tap_${VID}.mp3.part"
yt-dlp -o "/tmp/tap_${VID}.%(ext)s" --extract-audio --audio-format mp3 --audio-quality 0 --no-playlist "$URL"
```
Replace $URL with the actual URL and $VID with the extracted video ID.

### Step 2: Transcribe with Whisper
```bash
cd ~/transcriber
source .venv/bin/activate
python3 -c "
import whisper
model = whisper.load_model('base')
result = model.transcribe('/tmp/tap_${VID}.mp3')
print(result['text'])
" 2>/dev/null
```
Replace $VID with the same video ID from Step 1. Capture the full transcript output.

### Step 3: Search Existing Knowledge
Use `memory_recall` and `vault_search` to find any related content already in the vault. This enriches your analysis with connections.

### Step 4: Deep Analysis
Analyze the transcript as a domain expert. Create a comprehensive knowledge document with:

- **Title**: Descriptive title for the content
- **Source**: The original URL
- **Core Concepts**: Key ideas, frameworks, and mental models presented
- **Key Takeaways**: Actionable insights (bulleted)
- **Technical Details**: Any specific techniques, tools, code patterns, or methodologies
- **Connections**: How this relates to existing vault knowledge (from Step 3)
- **Expert Summary**: A dense, reusable paragraph that captures the essence - written so that reading it later makes you an expert on the topic

### Step 5: Store in Vault
Use `memory_store` to save TWO documents:

1. **Raw Transcript** (category: knowledge)
   - title: "Transcript: {descriptive title}"
   - tags: "transcript,video,tap,{topic-tags}"
   - content: The full raw transcript with source URL

2. **Expert Analysis** (category: knowledge)
   - title: "Expert: {descriptive title}"
   - tags: "expert-analysis,tap,{topic-tags}"
   - content: The full analysis from Step 4

### Step 6: Cleanup
```bash
rm -f "/tmp/tap_${VID}.mp3" "/tmp/tap_${VID}.mp3.part" "/tmp/tap_${VID}.webm"
```
Replace $VID with the same video ID from Step 1.

### Step 7: Report
Show the user a concise summary:
- What the video was about (1-2 sentences)
- Top 3 takeaways
- What was stored and tags used
- Any connections found to existing knowledge

## Notes
- Supports YouTube, TikTok, Instagram, and any yt-dlp compatible URL
- If transcription fails, try with `whisper_model='tiny'` as fallback
- Always clean up temp files even if steps fail
