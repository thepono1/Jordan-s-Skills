#!/usr/bin/env python3
"""
Extract Jordan's writing samples from iMessages, Mail, and Notes.
Outputs representative samples for voice analysis.
"""

import sqlite3
import os
import subprocess
import re
import email
from pathlib import Path
from datetime import datetime, timedelta
import random

TWO_YEARS_AGO = datetime.now() - timedelta(days=730)
MIN_LENGTH = 40       # Minimum chars — filters "ok", "yes", emojis
SAMPLE_PER_SOURCE = 600  # Max samples per source
OUTPUT_FILE = Path.home() / ".claude/skills/ghostwriter/raw_samples.txt"

# ── iMessages ─────────────────────────────────────────────────────────────────
def extract_imessages():
    db_path = Path.home() / "Library/Messages/chat.db"
    if not db_path.exists():
        return []
    conn = sqlite3.connect(str(db_path))
    # Apple Cocoa epoch: nanoseconds since 2001-01-01. Unix cutoff conversion:
    cutoff_ns = (TWO_YEARS_AGO.timestamp() - 978307200) * 1_000_000_000
    rows = conn.execute("""
        SELECT text FROM message
        WHERE is_from_me = 1
          AND date > ?
          AND text IS NOT NULL
          AND cache_has_attachments = 0
          AND LENGTH(text) > ?
        ORDER BY date DESC
    """, (cutoff_ns, MIN_LENGTH)).fetchall()
    conn.close()
    messages = [r[0].strip() for r in rows if r[0]]
    # Filter out pure emoji/link-only messages
    messages = [m for m in messages if re.search(r'[a-zA-Z]{4,}', m)]
    random.shuffle(messages)
    return messages[:SAMPLE_PER_SOURCE]

# ── Apple Mail — Sent Messages ─────────────────────────────────────────────────
def extract_sent_mail():
    mail_root = Path.home() / "Library/Mail/V10"
    if not mail_root.exists():
        return []
    # Find all .emlx files in Sent folders across all accounts
    sent_files = []
    for pattern in ["**/[Ss]ent*/**/*.emlx", "**/[Ss]ent/**/*.emlx"]:
        sent_files.extend(mail_root.glob(pattern))
    # Filter by modification date (last 2 years)
    cutoff_ts = TWO_YEARS_AGO.timestamp()
    sent_files = [f for f in sent_files if f.stat().st_mtime > cutoff_ts]
    random.shuffle(sent_files)

    bodies = []
    for emlx_path in sent_files[:800]:  # Parse up to 800 files
        try:
            content = emlx_path.read_text(errors='ignore')
            # .emlx format: first line is plist size (integer), then email RFC2822
            lines = content.split('\n', 1)
            if len(lines) < 2:
                continue
            msg = email.message_from_string(lines[1])
            body = _extract_email_body(msg)
            if body and len(body) > MIN_LENGTH:
                bodies.append(body)
        except Exception:
            continue
    return bodies[:SAMPLE_PER_SOURCE]

def _extract_email_body(msg):
    """Extract plain text body from email, strip quoted reply chains."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                break
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body = payload.decode('utf-8', errors='ignore')
    # Strip reply chains (lines starting with >)
    lines = [l for l in body.split('\n') if not l.strip().startswith('>')]
    # Strip common email signatures
    sig_markers = ['--', '___', 'Sent from', 'Best,', 'Thanks,', 'Cheers,']
    clean_lines = []
    for l in lines:
        if any(l.strip().startswith(m) for m in sig_markers):
            break
        clean_lines.append(l)
    body = '\n'.join(clean_lines).strip()
    return body if len(body) > MIN_LENGTH else ""

# ── Apple Notes via SQLite (faster than AppleScript for large vaults) ──────────
def extract_notes():
    db_path = Path.home() / "Library/Group Containers/group.com.apple.notes/NoteStore.sqlite"
    if not db_path.exists():
        return []
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        # ZICCLOUDSYNCINGOBJECT holds note data; ZDATA is gzipped HTML
        # ZSNIPPET is plain-text preview — use it as it's already decoded
        cutoff_ts = TWO_YEARS_AGO.timestamp() - 978307200  # Cocoa epoch offset
        rows = conn.execute("""
            SELECT ZSNIPPET FROM ZICCLOUDSYNCINGOBJECT
            WHERE ZSNIPPET IS NOT NULL
              AND ZMODIFICATIONDATE1 > ?
              AND LENGTH(ZSNIPPET) > ?
            ORDER BY ZMODIFICATIONDATE1 DESC
        """, (cutoff_ts, MIN_LENGTH)).fetchall()
        conn.close()
        notes = [r[0].strip() for r in rows if r[0]]
        # Strip any remaining HTML tags
        notes = [re.sub(r'<[^>]+>', '', n).strip() for n in notes]
        notes = [n for n in notes if len(n) > MIN_LENGTH and re.search(r'[a-zA-Z]{4,}', n)]
        random.shuffle(notes)
        return notes[:SAMPLE_PER_SOURCE]
    except Exception as e:
        print(f"  Notes warning: {e}")
        return []

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    print("Extracting iMessages...")
    imessages = extract_imessages()
    print(f"  → {len(imessages)} messages")

    print("Extracting sent mail...")
    emails = extract_sent_mail()
    print(f"  → {len(emails)} emails")

    print("Extracting Apple Notes...")
    notes = extract_notes()
    print(f"  → {len(notes)} notes")

    # Write samples with source labels for analysis
    with open(OUTPUT_FILE, 'w') as f:
        f.write("=== iMESSAGES (casual voice) ===\n\n")
        for m in imessages:
            f.write(m + "\n---\n")
        f.write("\n=== SENT EMAIL (professional voice) ===\n\n")
        for e in emails:
            f.write(e + "\n---\n")
        f.write("\n=== APPLE NOTES (personal/thinking voice) ===\n\n")
        for n in notes:
            f.write(n + "\n---\n")

    total = len(imessages) + len(emails) + len(notes)
    print(f"\nDone. {total} samples written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
