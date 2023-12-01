#!/bin/bash

podman login -u omarzen -p 11410120206130 quay.io

podman pull quay.io/omarzen/clinic-mysql-db:1.0

podman pull quay.io/omarzen/clinic-messaging-mq:1.0

podman pull quay.io/omarzen/clinic-backend:1.0

podman pull quay.io/omarzen/clinic-frontend:1.0

podman images

echo "Images are pulled successfully!"
