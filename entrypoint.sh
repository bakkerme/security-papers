#!/bin/sh
CRON_SCHEDULE=${CRON_SCHEDULE:-"0 * * * *"} 

echo "$CRON_SCHEDULE /usr/local/bin/run-job.sh" > /etc/crontabs/root

echo "Starting cron with schedule: $CRON_SCHEDULE"

exec crond -f -l 2
