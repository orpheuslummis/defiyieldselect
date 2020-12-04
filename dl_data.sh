PROJECT=defiyieldoptimization
T=$(date +%s)
ssh -t equivos@45.56.67.145 "docker run --rm --volumes-from defiyieldoptimization_collect_orcadefi_1 -v /home/o/backup/:/backup/ ubuntu cp -r /data/ /backup/$PROJECT_$T/"
rsync -av equivos@45.56.67.145:backup/$PROJECT_$T/ data/