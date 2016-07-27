#!/bin/sh

REPO_TAG=$(git describe --dirty --always);

set -uex

# Pull image to save build time
docker pull csesoc/showcse

# Actually do the build.
docker build -t csesoc/showcse:$REPO_TAG .

# Login and push
docker login -e="$DOCKER_EMAIL" -u="$DOCKER_USERNAME" -p="$DOCKER_PASSWORD";
docker push csesoc/showcse:$REPO_TAG

if [ "$TRAVIS_BRANCH" = "master" ]; then
    docker tag docker tag csesoc/showcse:$REPO_TAG csesoc/showcse:latest;
    docker push csesoc/showcse:latest;
fi
