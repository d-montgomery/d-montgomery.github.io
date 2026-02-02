#!/bin/bash

## This will open up http://localhost:4000 and continuously update 
## Use docker stop or docker kill to end

open http://localhost:4000 &

docker run --rm \
  -v "$PWD:/srv/jekyll" \
  -v "$PWD/.bundle:/usr/local/bundle" \
  -p 4000:4000 \
  jekyll/builder:latest \
  bash -lc "bundle install && bundle exec jekyll serve --watch --host 0.0.0.0"



