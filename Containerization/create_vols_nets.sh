#!/bin/bash

podman volume create clinic-vol

podman volume create rabbitmq-vol

podman volume ls


podman network create ui-net

podman network create api-net

podman network create messaging-net

podman network ls

echo "Volumes and Networks are created successfully"

