PROJECT=defiyieldoptimization
rsync -av --exclude .venv \
    --exclude .git \
    --exclude __pycache__ \
    --exclude data \
    --exclude tmp \
    --exclude results \
    . equivos@45.56.67.145:apps/$PROJECT
ssh -t equivos@45.56.67.145 "cd \$HOME/apps/$PROJECT && docker-compose up --build -d"