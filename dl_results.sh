# PROJECT="defiyieldoptimization"
# T=$(date +%s)
# ssh -t equivos@45.56.67.145 "docker run --rm --volumes-from defiyieldoptimization_forecasting_1 ubuntu mkdir -p \$HOME/results/$PROJECT/$T/ && cp -r /results/ \$HOME/results/$PROJECT/$T/"
# rsync -av equivos@45.56.67.145:results/ results_dl/

ssh -t equivos@45.56.67.145 "docker run --rm --volumes-from defiyieldoptimization_forecasting_1 ubuntu ls /results/"
