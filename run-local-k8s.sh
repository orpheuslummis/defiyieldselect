# assuming a local kubernetes context is active
echo "~~~ running once more! ~~~"
kubectl create configmap bowhead-dfo-config --from-file=
kubectl delete --grace-period=1 -f kubernetes-manifests/ 
docker build -t gcr.io/equivos-main/bowhead-dfo .
kubectl apply -f bowhead-dfo.yaml
kubectl rollout status deployment bowhead-dfo-deployment
kubectl port-forward --pod-running-timeout=1m service/bowhead-dfo-service 8000