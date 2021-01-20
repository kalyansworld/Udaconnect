## Steps for Executing project

kubectl apply -f frontend/udaconnect-app.yaml
kubectl apply -f person_api/udaconnect-person-api.yaml
kubectl apply -f location_api/udaconnect-location-api.yaml
kubectl apply -f connection_api/udaconnect-connection-api.yaml
kubectl apply -f postgres/db-configmap.yaml
kubectl apply -f postgres/db-secret.yaml
kubectl apply -f postgres/postgres.yaml


## Steps for Playing around with grpc

python grpc/main.py
#grpc client
python grpc/writer.py


##Steps for playing around with Kafka(Used Dockerized Kafka)

docker pull spotify/kafka
docker run -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST=localhost --env ADVERTISED_PORT=9092 spotify/kafka
#Kafka Producer
kafka kafka/producer.py
#Kafka Consumer
kafka kafka/consumer.py