#!/bin/bash

/scripts/wait-for-it.sh -t 15 $DB_HOST:$DB_PORT

python /backend/manage.py collectstatic --noinput
python /backend/manage.py migrate --noinput
status=$?
if [ $status -ne 0 ]; then
    echo "Failed to migrate: $status"
    exit $status
fi

uwsgi
