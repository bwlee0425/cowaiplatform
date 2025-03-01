# PowerShell 스크립트 시작

# docker-compose down 실행
Write-Host "Shutting down containers..."
docker compose -f docker-compose.db.yml down

# docker-compose up -d 실행
Write-Host "Starting containers in detached mode..."
docker compose -f docker-compose.db.yml up -d

# update_env.sh 실행
#Write-Host "Running update_env.sh to update .env file with new container IPs..."
#bash ./update_env.sh

#Write-Host "Docker containers are up and .env file is updated."