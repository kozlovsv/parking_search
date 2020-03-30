#!/bin/bash
name="parking"
app="kozlovsv78/"${name}
docker stop ${name}
docker build -t ${app} .
docker run -d -p 80:80 \
  --name=${name} \
  --rm \
  -v "d:\dev\parking":"/app" \
  ${app}