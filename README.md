# Project 1 — Dockerised Flask App with Postgres

## What this project does
A Python Flask web app connected to a Postgres database,
containerised with Docker and orchestrated via docker-compose.

## Why I built this
At Salesken, our microservices run in containers connected to
managed databases. I built this to understand how containerised
apps communicate with databases, how health checks work, and
how environment variables are used for configuration.

## Architecture
- Flask app (Python) → container on port 5000
- Postgres 15 → container with persistent volume
- docker-compose manages both containers and their network

## How to run
docker compose up -d

## Endpoints
- GET /          → service status
- GET /health    → database connectivity check
- GET /visits    → insert + count visits (tests DB read/write)

## What I learned
- Dockerfile layer caching (COPY requirements before code)
- depends_on with health checks (app waits for DB to be ready)
- Named volumes for data persistence
- Container networking (app reaches db by service name, not IP)# CI/CD enabled
# webhook test
#checking jenkins scm
# poll test
# testing poll scm
# poll scm fixed
webhook test
poll test
