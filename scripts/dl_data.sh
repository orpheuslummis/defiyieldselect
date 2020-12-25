PROJECT=defiyieldoptimization
T=$(date +%s)
ssh -t equivos@qbit "docker run --rm --volumes-from defiyieldoptimization_collect_orcadefi_1 -v \$HOME/backup/:/backup/ ubuntu cp -r /data/ /backup/$PROJECT_$T/"
rsync -av equivos@qbit:backup/$PROJECT_$T/ data/