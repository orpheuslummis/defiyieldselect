PROJECT=defiyieldoptimization
rsync -av --exclude .venv \
    --exclude .git \
    --exclude __pycache__ \
    --exclude results \
    . equivos@qbit:apps/$PROJECT
ssh -t equivos@qbit "cd \$HOME/apps/$PROJECT && docker-compose up --build -d"
# ssh -t equivos@qbit "cd \$HOME/apps/$PROJECT && docker-compose logs -tf"