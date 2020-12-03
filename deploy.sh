PROJECT=defiyieldoptimization
rsync -av --exclude .venv \
    --exclude .git \
    --exclude __pycache__ \
    . o@linda:apps/$PROJECT
ssh -t o@linda "cd /home/o/apps/$PROJECT && docker-compose up --build -d"