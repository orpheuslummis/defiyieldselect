PROJECT=defiyieldoptimization
T=$(date +%s)
ssh -t equivos@45.56.67.145 "docker run --rm --volumes-from defiyieldoptimization_forecasting_1 -v /home/equivos/backup/:/backup/ ubuntu cp -r /results/ /backup/$PROJECT_$T/"
rsync -av equivos@45.56.67.145:backup/$PROJECT_$T/ results_dl/