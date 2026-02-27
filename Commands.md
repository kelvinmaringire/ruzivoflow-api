# Ruzivoflow Commands


```bash
docker network create ruzivoflow_net

docker stop $(docker ps -q)

rm -rf ruzivoflow-api

ssh-keygen -t rsa -b 4096 -C "$(whoami)@$(hostname)" -f ~/.ssh/github

cat /c/Users/User/.ssh/github

timedatectl set-timezone Africa/Johannesburg


```

```bash
docker compose run web wagtail start ruzivoflow .

docker compose run web python manage.py migrate

docker compose run web python manage.py createsuperuser

docker compose exec -T web pip freeze > requirements.txt
```

## VPS Start Commands

```bash
sudo apt update

sudo apt upgrade -y

sudo apt install ufw -y

sudo ufw enable

sudo ufw allow 80/tcp && sudo ufw allow 8000/tcp && sudo ufw allow 443/tcp && sudo ufw allow 22/tcp && sudo ufw allow 6379/tcp

sudo ufw reload

sudo ufw status
```

## Install Docker on VPS

```bash
sudo apt update && sudo apt install -y ca-certificates curl gnupg lsb-release

sudo install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update

sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin 

docker --version

sudo usermod -aG docker $USER

docker run hello-world
```

## Clone and Setup Wagtail Project

```bash
mkdir -p ~/srv

cd ~/srv

sudo git clone https://github.com/kelvinmaringire/ruzivoflow-api.git

cd ruzivoflow-api

nano .env   # (paste your environment variables here)

docker pull 7612/ruzivoflow-backend:0.1.0

docker compose up -d
```

## Unified Backup & Restore (Media + Database + .env → Google Drive)

### Setup rclone (One-time)

```bash
# Install rclone
curl https://rclone.org/install.sh | sudo bash

# Configure Google Drive remote
rclone config

# Follow the prompts:
# 1. Select "n" for new remote
# 2. Name it "gdrive" (or your preferred name)
# 3. Select "drive" (Google Drive)
# 4. Leave client_id and client_secret blank (uses defaults)
# 5. Choose scope (full access recommended for backups)
# 6. Complete OAuth authentication in browser
# 7. Verify configuration: rclone listremotes
```

### Service Account + Shared Drive (Required for service accounts)

Service accounts cannot write to My Drive (causes "storageQuotaExceeded" error). You must use a shared drive:

```bash
# 1. Add service account to shared drive (in Google Drive web UI)
#    - Open Shared drives > your-backups-drive > Share
#    - Add: your-service-account@project.iam.gserviceaccount.com (Editor)

# 2. Add team_drive to rclone config (run rclone config, or edit ~/.config/rclone/rclone.conf)
#    Under [gdrive] add: team_drive = <SHARED_DRIVE_ID>

# 3. Create Backups folder and test
rclone mkdir gdrive:Backups
bash scripts/backup.sh
```

### Backup (Media + Database + .env)

```bash
# Run backup script
bash scripts/backup.sh

# The script will:
# - Backup media files from container/volume
# - Backup PostgreSQL database (using credentials from .env)
# - Backup .env file
# - Create a timestamped .zip file (e.g. ruzivoflow_20240227_143022.zip)
# - Upload to Google Drive: gdrive:Backups/ruzivoflow/
# - Keep max 2 backups in the cloud (delete oldest when a 3rd is created)
```

**Folder structure on Google Drive:**
```
Backups/                    # Root for all apps
  ruzivoflow/               # This app's backups
    ruzivoflow_20240227_143022.zip
    ruzivoflow_20240227_020000.zip
```

**Configuration Options:**
```bash
# Customize rclone remote name (default: gdrive)
export RCLONE_REMOTE="gdrive"

# Customize root folder for all app backups (default: Backups)
export RCLONE_BASE="Backups"

# Customize app subfolder name (default: ruzivoflow)
export APP_NAME="ruzivoflow"

# Customize max backups to keep per app (default: 2)
export MAX_BACKUPS=3

# Then run backup
bash scripts/backup.sh
```

### Restore from Backup

```bash
# Restore latest backup
bash scripts/restore.sh latest

# Restore specific backup
bash scripts/restore.sh ruzivoflow_20240227_143022.zip

# The script will:
# - Download backup from Google Drive
# - Extract backup archive
# - Restore media files to container/volume
# - Drop and recreate database, then restore from dump (with confirmation)
# - Restore .env file (with confirmation, current backed up to .env.bak.<timestamp>)
```

**Restore Process:**
- Media files: Automatically copied to `ruzivoflow_web` container or volume
- Database: Requires confirmation before dropping/recreating (destructive operation)
- .env file: Requires confirmation before overwriting (previous .env backed up to `.env.bak.<timestamp>`)

### Scheduled Backups (Cron)

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * cd /home/user/srv/ruzivoflow-api && bash scripts/backup.sh >> backup.log 2>&1

# Or with custom environment variables
0 2 * * * cd /home/user/srv/ruzivoflow-api && RCLONE_REMOTE=gdrive RCLONE_BASE=Backups bash scripts/backup.sh >> backup.log 2>&1

# Verify cron job
crontab -l
```

### Manual Backup & Restore (Legacy Methods)

<details>
<summary>Click to expand manual backup/restore commands</summary>

#### Media Files Backup & Restore

```bash
# Backup Media Files
mkdir -p ./media
docker cp ruzivoflow_web:/app/media/. ./media

# Restore Media Files
docker cp ./media/. ruzivoflow_web:/app/media/
```

#### PostgreSQL Backup & Restore

```bash
# Backup Database
docker compose exec -T db pg_dump -U postgres -d ruzivoflow_db -F c > ./data_backup.dump

# Restore Database
docker compose exec -T db psql -U postgres -c "DROP DATABASE ruzivoflow_db;"
docker compose exec -T db psql -U postgres -c "CREATE DATABASE ruzivoflow_db;"
docker compose exec -T db pg_restore -U postgres -d ruzivoflow_db < data_backup.dump

chmod +x scripts/backup.sh scripts/restore.sh
```

</details>


