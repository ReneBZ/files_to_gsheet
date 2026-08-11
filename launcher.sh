#!/bin/bash

# Determine the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Downloaded files carry a quarantine flag that blocks Automator from opening them.
for file in "$@"; do
    if [[ -f "$file" ]]; then
        xattr -d com.apple.quarantine "$file" 2>/dev/null || true
    fi
done

for file in "$@"; do
    ext="${file##*.}"
    ext="$(printf '%s' "$ext" | tr '[:upper:]' '[:lower:]')"
    case "$ext" in
        csv)
            "$DIR/.venv/bin/python3" "$DIR/csv_to_sheets.py" "$file"
            ;;
        xlsx|xls)
            "$DIR/.venv/bin/python3" "$DIR/xlsx_to_sheets.py" "$file"
            ;;
        *)
            echo "Unsupported file type: .$ext (expected .csv, .xlsx, or .xls)" >&2
            exit 1
            ;;
    esac
done
