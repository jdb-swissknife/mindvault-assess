#!/bin/bash
# Generate AI Assessment Report from transcript
# Usage: generate_report /path/to/transcript.txt

if [ -z "$1" ]; then
    echo "Usage: generate_report <transcript_file>"
    exit 1
fi

TRANSCRIPT_FILE="$1"

if [ ! -f "$TRANSCRIPT_FILE" ]; then
    echo "Error: File not found: $TRANSCRIPT_FILE"
    exit 1
fi

echo "Generating report from: $TRANSCRIPT_FILE"
cat "$TRANSCRIPT_FILE"
