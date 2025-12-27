#!/bin/sh
set -e

if [ -f /app/.env ]; then
  set -a
  . /app/.env
  set +a
fi

python -m security_papers.run_job
