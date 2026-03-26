#!/bin/bash

# process-feedback.sh - Process and organize code review feedback
# Usage: ./process-feedback.sh --input <feedback-file> [--output <output-file>]

set -e

# Default values
INPUT_FILE=""
OUTPUT_FILE="feedback-processed.md"
FORMAT="markdown"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --input)
            INPUT_FILE="$2"
            shift 2
            ;;
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --format)
            FORMAT="$2"
            shift 2
            ;;
        --help)
            cat << EOF
Usage: $0 --input <feedback-file> [--output <output-file>] [--format markdown|json]

Process and organize code review feedback.

Options:
  --input    Path to feedback file (required)
  --output   Path to output file (default: feedback-processed.md)
  --format   Output format: markdown (default) or json
  --help     Show this help message

Input Format:
  The script accepts feedback in various formats:
  - Plain text with comments
  - JSON with structured feedback
  - Markdown with review comments

Output:
  Organized feedback categorized by priority with action items.
EOF
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate input
if [[ -z "$INPUT_FILE" ]]; then
    echo "Error: --input is required"
    exit 1
fi

if [[ ! -f "$INPUT_FILE" ]]; then
    echo "Error: File not found: $INPUT_FILE"
    exit 1
fi

# Read feedback
FEEDBACK=$(cat "$INPUT_FILE")

# Detect feedback format and parse
detect_format() {
    if echo "$FEEDBACK" | jq -e . > /dev/null 2>&1; then
        echo "json"
    elif echo "$FEEDBACK" | grep -q "^#"; then
        echo "markdown"
    else
        echo "text"
    fi
}

FORMAT_DETECTED=$(detect_format)

# Categorize feedback by priority
categorize_feedback() {
    local content="$1"
    
    # Critical: bugs, security, breaking changes
    CRITICAL=$(echo "$content" | grep -iE "(bug|security|breaking|critical|error|crash|vulnerability)" || echo "")
    
    # Important: performance, best practices
    IMPORTANT=$(echo "$content" | grep -iE "(performance|best practice|maintainability|important|should|recommend)" || echo "")
    
    # Suggestions: style, minor improvements
    SUGGESTIONS=$(echo "$content" | grep -iE "(suggestion|style|minor|consider|optional|nit|minor)" || echo "")
    
    # General comments (remaining)
    GENERAL="$content"
}

# Generate output
generate_output() {
    cat << EOF
# Processed Code Review Feedback

*Generated on $(date)*

---

## 🔴 Critical Issues (Must Fix Before Merge)

EOF

    if [[ -n "$CRITICAL" ]]; then
        echo "$CRITICAL"
    else
        echo "✅ No critical issues found"
    fi

    cat << EOF

---

## 🟡 Important Issues (Should Fix)

EOF

    if [[ -n "$IMPORTANT" ]]; then
        echo "$IMPORTANT"
    else
        echo "✅ No important issues found"
    fi

    cat << EOF

---

## 🟢 Suggestions (Consider Fixing)

EOF

    if [[ -n "$SUGGESTIONS" ]]; then
        echo "$SUGGESTIONS"
    else
        echo "✅ No suggestions"
    fi

    cat << EOF

---

## 📋 Action Items

EOF

    # Generate action items based on feedback
    ACTION_COUNT=0
    
    if [[ -n "$CRITICAL" ]]; then
        echo "$CRITICAL" | while read -r line; do
            if [[ -n "$line" ]]; then
                ACTION_COUNT=$((ACTION_COUNT + 1))
                echo "- [ ] **Critical:** $line"
            fi
        done
    fi
    
    if [[ -n "$IMPORTANT" ]]; then
        echo "$IMPORTANT" | while read -r line; do
            if [[ -n "$line" ]]; then
                ACTION_COUNT=$((ACTION_COUNT + 1))
                echo "- [ ] **Important:** $line"
            fi
        done
    fi
    
    if [[ -n "$SUGGESTIONS" ]]; then
        echo "$SUGGESTIONS" | while read -r line; do
            if [[ -n "$line" ]]; then
                ACTION_COUNT=$((ACTION_COUNT + 1))
                echo "- [ ] **Suggestion:** $line"
            fi
        done
    fi

    cat << EOF

---

## 📊 Summary

| Priority | Count |
|----------|-------|
| 🔴 Critical | $(echo "$CRITICAL" | grep -c . || echo "0") |
| 🟡 Important | $(echo "$IMPORTANT" | grep -c . || echo "0") |
| 🟢 Suggestions | $(echo "$SUGGESTIONS" | grep -c . || echo "0") |

---

## 📝 Notes

- Address critical issues before merging
- Document your decisions when not addressing feedback
- Update this file as you resolve each item

EOF
}

# Main processing
echo "Processing feedback from: $INPUT_FILE"
echo "Detected format: $FORMAT_DETECTED"

categorize_feedback "$FEEDBACK"

case "$FORMAT" in
    markdown)
        generate_output > "$OUTPUT_FILE"
        echo "Output written to: $OUTPUT_FILE"
        ;;
    json)
        cat << EOF > "$OUTPUT_FILE"
{
  "critical": $(echo "$CRITICAL" | jq -Rs .),
  "important": $(echo "$IMPORTANT" | jq -Rs .),
  "suggestions": $(echo "$SUGGESTIONS" | jq -Rs .),
  "timestamp": "$(date -Iseconds)"
}
EOF
        echo "Output written to: $OUTPUT_FILE"
        ;;
    *)
        echo "Unknown format: $FORMAT"
        exit 1
        ;;
esac

echo ""
echo "✅ Feedback processing complete!"
echo ""
echo "Next steps:"
echo "1. Review the categorized feedback in $OUTPUT_FILE"
echo "2. Address critical issues first"
echo "3. Update the checklist as you resolve each item"