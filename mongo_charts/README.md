# Mongo Charts Deployment

### Requirements:
1. Docker
2. MongoDB



###Setup

1. Login to GCE
    ```bash
    gcloud beta compute ssh --zone "us-central1-a" "mongo-charts-instance" --project "breakout-rl-255903"
    ```

2. Create Firewall rules
    ```bash
    # Allow for charts
    gcloud compute firewall-rules create mongo-charts --allow tcp:80
    
    # Allow for DB
    gcloud compute firewall-rules create mongo-db --allow tcp:25043
    ```

3. Charts Deployment
    ```bash
    docker swarm init
    docker stack rm mongodb-charts
    docker run --rm quay.io/mongodb/charts:19.12.1 charts-cli test-connection mongodb://104.251.210.60:27017
    docker secret rm charts-mongodb-uri
    echo mongodb://104.251.210.60:27017 | docker secret create charts-mongodb-uri -
    docker stack deploy -c charts-docker-swarm-19.12.1.yml mongodb-charts
    docker service ls
    docker stack rm mongodb-charts
    ```
4. Create Users

    ```bash
    docker exec -it \
      $(docker container ls --filter name=_charts -q) \
      charts-cli add-user --first-name "Admin" --last-name "WPI" \
      --email "admin@wpi.com" --password "wpi@123" \
      --role "UserAdmin"
    
     docker exec -it \
      $(docker container ls --filter name=_charts -q) \
      charts-cli add-user --first-name "User" --last-name "WPI" \
      --email "user@wpi.com" --password "wpi@123" \
      --role "User"
    ```

### Launch / Init Scripts
```bash
# 1. Mongo Daemon
mongod -f /home/prathyushsp/Git/covid19_research/mongo_charts/mongo-gce.conf &

sleep 10

# 2. Docker Charts Deploymnent  
docker stack deploy -c /home/prathyushsp/Git/covid19_research/mongo_charts/charts-docker-swarm-19.12.1.yml mongodb-charts
```

### Resources
 
 1. [Install Docker](https://docs.docker.com/engine/install/ubuntu/)
 2. [Install Mongodb](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)
 
 