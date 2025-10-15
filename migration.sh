#!/bin/bash

host="$POSTGRES_HOST"
port="$POSTGRES_PORT"

echo "Waiting for $host:$port to be available..."
until nc -z "$host" "$port"; do
  >&2 echo "Waiting for $host:$port to be available..."
  sleep 1
done

>&2 echo "$host:$port is available, running migrations..."
export ALEMBIC_CONFIG=db/alembic.ini

alembic upgrade head


cd src/
fastapi run --reload --host 0.0.0.0 --port 8080 &

tail -f /dev/null
