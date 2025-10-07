#!/usr/bin/env bash
set -e

# wait for the DB
bash ./scripts/wait-for.sh db 5432 echo "db is up"

exec "$@"