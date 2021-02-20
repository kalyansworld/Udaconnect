## Steps for Executing project
```s
kubectl apply -f frontend/udaconnect-app.yaml
kubectl apply -f person_api/udaconnect-person-api.yaml
kubectl apply -f location_api/udaconnect-location-api.yaml
kubectl apply -f connection_api/udaconnect-connection-api.yaml
kubectl apply -f postgres/db-configmap.yaml
kubectl apply -f postgres/db-secret.yaml
kubectl apply -f postgres/postgres.yaml
```

## Steps for turning on grpc server 
```s
python -m pip install grpcio
python -m pip install grpcio-tools
python grpc/server.py

```

## Steps for running Kafka Broker
```s
docker pull spotify/kafka
docker run --ti -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST=kafka --env ADVERTISED_PORT=9092 spotify/kafka
```
## Steps for running Kafka Consumer
```s
docker build -t kafka-listener kafka/
docker run -d --name kafka-listener
```
