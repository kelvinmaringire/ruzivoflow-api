# Ruzivoflow Commands


```bash
docker network create ruzivoflow_net

docker stop $(docker ps -q)

rm -rf ruzivoflow-api

docker exec ruzivoflow_web python manage.py test

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
mkdir -p ~/webapps

cd ~/webapps

sudo git clone https://github.com/kelvinmaringire/ruzivoflow-api.git

cd ruzivoflow-api

nano .env   # (paste your environment variables here)

chmod +x entrypoint.sh

docker compose up -d
```

## Media Files Backup & Restore

### Backup Media Files

```bash
# 1️⃣ Make sure local backup folder exists
mkdir -p ./media

# 2️⃣ Copy all media files from container to local backup folder
docker cp ruzivoflow_web:/app/media/. ./media
```

### Restore Media Files

```bash
# 1️⃣ Copy media files from local backup to container
docker cp ./media/. ruzivoflow_web:/app/media/
```

## PostgreSQL Backup & Restore

### Backup Database

```bash
# Backup inside container
# Backup Database (Windows-compatible)
docker compose exec -T db pg_dump -U postgres -d ruzivoflow_db -F c > ./data_backup.dump

# Copy backup to local machine
docker cp ruzivoflow_db:/var/lib/postgresql/data/data_backup.dump ./data_backup.dump
```

### Restore Database

```bash
docker cp ./data_backup.dump ruzivoflow_db:/tmp/data_backup.dump

docker compose exec db bash

psql -U postgres -c "DROP DATABASE ruzivoflow_db;"

psql -U postgres -c "CREATE DATABASE ruzivoflow_db;"

exit

docker compose exec -T db pg_restore -U postgres -d buybuddy_db < data_backup.dump
```


