#!/bin/bash

## This will open up http://localhost:4000 and continuously update 
## Use docker stop <docker_id> or docker kill <docker_id> to end

set -e

PORT=4000
URL="http://localhost:$PORT"
BUNDLE_DIR="$PWD/.bundle-cache"

echo "Checking gem cache..."

if [ ! -d "$BUNDLE_DIR" ]; then
    echo "Creating gem cache..."
    mkdir -p "$BUNDLE_DIR"
fi

# Stop any container using port 4000
RUNNING=$(docker ps -q --filter "publish=$PORT")

if [ ! -z "$RUNNING" ]; then
    echo "Stopping existing container..."
    docker stop $RUNNING >/dev/null
fi

# Open browser ONLY if not already open
if ! lsof -i :$PORT >/dev/null 2>&1; then
    echo "Opening browser..."
    open "$URL"
fi

echo "Starting Jekyll..."

docker run --rm \
  -v "$PWD:/srv/jekyll" \
  -v "$BUNDLE_DIR:/usr/local/bundle" \
  -p $PORT:4000 \
  jekyll/builder:latest \
  bash -lc '
    bundle check || bundle install
    bundle exec jekyll serve \
      --host 0.0.0.0 \
      --force_polling \
      --incremental
  '





