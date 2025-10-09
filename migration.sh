#!/bin/bash

fastapi run --reload &

# Arguments: host and port
host="$POSTGRES_HOST"
port="$POSTGRES_PORT"

# Wait for the specified host and port to be available
until nc -z "$host" "$port"; do
  >&2 echo "Waiting for $host:$port to be available..."
  sleep 1
done

>&2 echo "$host:$port is available, running migrations..."

# Run Alembic migrations
alembic upgrade head

# Start the Flask application
# python app.py
