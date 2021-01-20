docker build -t gcr.io/equivos-main/bowhead-dfo .
docker run --env-file env.list -t gcr.io/equivos-main/bowhead-dfo