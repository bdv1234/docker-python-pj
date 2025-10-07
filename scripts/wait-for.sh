#!/usr/bin/env bash
set -e

host="$1"
port="$2"
shift 2
cmd="$@"

until bash -c "</dev/tcp/$host/$port" >/dev/null 2>&1; do
    echo "Waiting for $host:$port"
    sleep 1
done

exec $cmd