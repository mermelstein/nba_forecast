#!/usr/bin/env bash
set -e

source ./env_variables.sh

docker build --no-cache -t nbaforecast:v1 .
docker run --env-file env.list --rm -v $(pwd):/nba_forecast -w /nba_forecast nbaforecast:v1
docker image prune -a -f