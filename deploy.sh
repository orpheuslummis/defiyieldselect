PROJECT=defiyieldoptimization
rsync -av --exclude .venv \
    --exclude .git \
    --exclude __pycache__ \
    --exclude data \
    . equivos@45.56.67.145:apps/$PROJECT
ssh -t equivos@45.56.67.145 "cd /home/equivos/apps/$PROJECT && docker-compose up --build -d"