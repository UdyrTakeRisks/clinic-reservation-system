#!/bin/bash

# Script to run containers

# To run a Bash script on Linux:

# ./run_containers.sh

# To run a Bash script on Windows using Git:

# bash run_containers.sh

# Step 1: Run Databse MySQL container

podman run -d --name clinic-db-app -p 3306:3306 -e MYSQL_USER='ahmed' -e MYSQL_PASSWORD='123' -e MYSQL_DATABASE='clinicdb' -e MYSQL_ROOT_PASSWORD='123' --network api-net -v clinic-vol:/var/lib/mysql/data -v sqlfile:/tmp/clinic-db quay.io/omarzen/clinic-mysql-db:1.0

# Step 2: Run RabbitMq Messaging container

podman run -d --name clinic-rabbitmq --net messaging-net -p 5672:5672 -v rabbitmq-vol:/var/lib/rabbitmq quay.io/omarzen/clinic-messaging-mq:1.0

# Step 3: Run Backend container

podman run -d --name clinic-backend-app -e DB_HOST=clinic-db-app -p 5000:5000 --network api-net,ui-net,messaging-net quay.io/omarzen/clinic-backend:1.0 

# Step 4: Run Frontend container

podman run -d --name clinic-frontend-app -e BACKEND_HOST=clinic-backend-app -p 4200:4200 --net ui-net quay.io/omarzen/clinic-frontend:1.0

# Step 5: Verify Containers are Running

podman ps

echo "Containers runs successfully!"

