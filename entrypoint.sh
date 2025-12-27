#!/bin/sh
set -e

env | grep -v "=" > /dev/null 2>&1 || true

ENV_FILE="/app/.env"
rm -f "$ENV_FILE"

env | while IFS= read -r line; do
  echo "$line" >> "$ENV_FILE"
done

CRON_SCHEDULE=${CRON_SCHEDULE:-"0 * * * *"}

echo "$CRON_SCHEDULE /usr/local/bin/run-job.sh" > /etc/crontabs/root

exec crond -f -l 2
