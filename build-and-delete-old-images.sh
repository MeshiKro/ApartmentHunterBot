#!/bin/bash

# Stop and remove all running containers
CONTAINERS=$(docker ps -aq)
if [ -n "$CONTAINERS" ]; then
    docker stop $CONTAINERS
    docker rm -f $CONTAINERS
fi

# Remove only images related to apartment-hunter-bot
IMAGE_IDS=$(docker images apartment-hunter-bot -q)
if [ -n "$IMAGE_IDS" ]; then
    docker rmi -f $IMAGE_IDS
else
    echo "No images found for apartment-hunter-bot, skipping removal."
fi

# Build the new image
# docker build --cache-from=apartment-hunter-bot -f dockerfile -t apartment-hunter-bot .
# Build the new image without using cache
# docker build --no-cache -f dockerfile -t apartment-hunter-bot .
docker build -f dockerfile -t apartment-hunter-bot .



# Remove all dangling images (images with <none> tag) after the build process
DANGLING_IMAGES=$(docker images -f "dangling=true" -q)
if [ -n "$DANGLING_IMAGES" ]; then
    docker rmi -f $DANGLING_IMAGES
fi

# Run the new container
docker run -p 5001:5000 apartment-hunter-bot
