#!/bin/bash

# Ruzivoflow rclone Shared Drive Setup
# Helps configure rclone to use the ruzivoflow-backups shared drive (required for service accounts)

set -e

RCLONE_REMOTE="${RCLONE_REMOTE:-gdrive}"
RCLONE_CONFIG="${RCLONE_CONFIG:-$HOME/.config/rclone/rclone.conf}"

echo "=========================================="
echo "rclone Shared Drive Setup"
echo "=========================================="
echo ""
echo "Service accounts cannot write to My Drive (storage quota error)."
echo "You must configure rclone to use the 'ruzivoflow-backups' shared drive."
echo ""

# Step 1: Get shared drive ID
echo "Step 1: Fetching shared drive ID..."
echo ""

DRIVE_JSON=$(rclone lsjson "$RCLONE_REMOTE:" --drive-shared-with-me 2>/dev/null || true)

if [ -z "$DRIVE_JSON" ]; then
    echo "ERROR: Could not list shared drives. Ensure:"
    echo "  - rclone remote '$RCLONE_REMOTE' is configured"
    echo "  - Your service account has been added to the 'ruzivoflow-backups' shared drive (Share > Add member > Editor)"
    echo ""
    echo "Run: rclone lsjson $RCLONE_REMOTE: --drive-shared-with-me"
    exit 1
fi

# Extract ID for ruzivoflow-backups (try jq, then python3)
SHARED_DRIVE_ID=""
if command -v jq &>/dev/null; then
    SHARED_DRIVE_ID=$(echo "$DRIVE_JSON" | jq -r '.[] | select(.Name=="ruzivoflow-backups" or .name=="ruzivoflow-backups") | .ID // .id // empty' 2>/dev/null)
fi
if [ -z "$SHARED_DRIVE_ID" ] && command -v python3 &>/dev/null; then
    SHARED_DRIVE_ID=$(echo "$DRIVE_JSON" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    for item in (data if isinstance(data, list) else [data]):
        name = item.get('Name') or item.get('name') or ''
        if name == 'ruzivoflow-backups':
            print(item.get('ID') or item.get('id') or '')
            break
except: pass
" 2>/dev/null)
fi

if [ -z "$SHARED_DRIVE_ID" ]; then
    echo "ERROR: Could not find 'ruzivoflow-backups' in shared drives."
    echo ""
    echo "Raw output (look for ID in the JSON):"
    echo "$DRIVE_JSON" | (python3 -m json.tool 2>/dev/null || cat)
    echo ""
    echo "Alternative: Get ID from Google Drive URL when opening the shared drive:"
    echo "  https://drive.google.com/drive/u/0/folders/0ABCD...  <- the part after 'folders/'"
    echo ""
    echo "Ensure the service account is a member of the shared drive:"
    echo "  1. Open Google Drive > Shared drives > ruzivoflow-backups"
    echo "  2. Right-click > Share"
    echo "  3. Add: YOUR_SERVICE_ACCOUNT@project.iam.gserviceaccount.com (Editor)"
    exit 1
fi

echo "Found shared drive ID: $SHARED_DRIVE_ID"
echo ""

# Step 2: Add to rclone config
echo "Step 2: Add team_drive to rclone config"
echo ""
echo "Option A - Interactive (easiest):"
echo "  Run: rclone config"
echo "  -> e) Edit existing remote"
echo "  -> Select: $RCLONE_REMOTE"
echo "  -> When asked 'Configure this as a Shared Drive?' choose y and pick ruzivoflow-backups"
echo "  -> Or: t) Edit advanced config -> team_drive -> Enter: $SHARED_DRIVE_ID"
echo ""
echo "Option B - Edit config file directly:"
echo "  Add this line under [$RCLONE_REMOTE] in $RCLONE_CONFIG:"
echo ""
echo "  team_drive = $SHARED_DRIVE_ID"
echo ""

echo ""
echo "Step 3: Create RuzivoflowBackups folder (if needed)"
echo "  Run: rclone mkdir $RCLONE_REMOTE:RuzivoflowBackups"
echo ""
echo "Step 4: Test backup"
echo "  bash scripts/backup.sh"
echo ""
echo "=========================================="
