# FIXME docker is depecrated in kubernetes 1.20. how to build otherwise? 
# assuming a remote kubernetes context is active
docker build -t gcr.io/equivos-main/bowhead-dfo .
docker push gcr.io/equivos-main/bowhead-dfo
kubectl apply -f kubernetes-manifests/bowhead-dfo-deployment.yaml