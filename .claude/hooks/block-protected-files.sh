#!/bin/bash
# ONLY allow edits to game/mod/ directory
# Block ALL other modifications in the game directory

# Read JSON input from stdin (PreToolUse format)
input=$(cat)

# Extract the file path being edited
file_path=$(echo "$input" | jq -r '.tool_input.file_path')

GAME_DIR="/mnt/c/Program Files (x86)/Steam/steamapps/common/Europa Universalis V"
ALLOWED_DIR="$GAME_DIR/game/mod/"

# If the file is in the game directory, it MUST be in game/mod/
if [[ "$file_path" == "$GAME_DIR/"* ]]; then
    if [[ "$file_path" != "$ALLOWED_DIR"* ]]; then
        echo "ERROR: Can only modify files in game/mod/" >&2
        echo "Attempted to edit: $file_path" >&2
        echo "" >&2
        echo "To modify base game files:" >&2
        echo "1. Create mod directory: game/mod/<mod_name>/" >&2
        echo "2. Copy the file: cp <source> game/mod/<mod_name>/..." >&2
        echo "3. Edit the copy in game/mod/" >&2
        exit 2  # Exit code 2 = block the operation
    fi
fi

# Allow edits outside game directory (e.g., .claude/ config files)
exit 0
