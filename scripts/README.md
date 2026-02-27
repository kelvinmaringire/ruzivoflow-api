# Ruzivoflow Backup & Restore Scripts

Backup and restore database, media files, and `.env` to/from Google Drive via rclone.

## Prerequisites

- **rclone** configured with a Google Drive remote (default: `gdrive`)
- **Docker** with `ruzivoflow_db` and `ruzivoflow_media` volumes
- **.env** file in project root with `POSTGRES_USER`, `POSTGRES_DB`, `POSTGRES_PASSWORD`
- **zip** (for backup) and **unzip** (for restore); install with `apt install zip unzip` on Debian/Ubuntu

## Usage

### Backup

```bash
bash scripts/backup.sh
```

Creates a timestamped zip (e.g. `ruzivoflow_20240227_143022.zip`) containing:
- `db.dump` – PostgreSQL dump
- `media/` – Uploaded media files
- `.env` – Environment variables

Uploads to `gdrive:Backups/ruzivoflow/` and keeps a maximum of 2 backups (deletes oldest when a 3rd is created).

### Restore

```bash
# Restore latest backup
bash scripts/restore.sh latest

# Restore specific backup
bash scripts/restore.sh ruzivoflow_20240227_143022.zip
```

Prompts for confirmation before restoring database and `.env`.

## Environment Variables

| Variable        | Default      | Description                    |
|----------------|--------------|--------------------------------|
| `RCLONE_REMOTE`| `gdrive`     | rclone remote name             |
| `RCLONE_BASE`  | `Backups`    | Root folder for all app backups |
| `APP_NAME`     | `ruzivoflow` | App subfolder name             |
| `MAX_BACKUPS`  | `2`          | Max backups to keep per app     |

## Folder Structure

```
Backups/                    # Shared root (multiple apps)
  ruzivoflow/               # This app's backups
    ruzivoflow_20240227_143022.zip
    ruzivoflow_20240227_020000.zip
```
