#!/usr/bin/env bash

if [[ -z "${APP_MIGRATIONS_CONFIG}" ]]; then
    APP_MIGRATIONS="skip"
else
    APP_MIGRATIONS="${APP_MIGRATIONS_CONFIG}"
fi

if [[ "$APP_MIGRATIONS" == 'init' ]]; then
    flask --app hostname_server.app db init
    flask --app hostname_server.app db migrate
    flask --app hostname_server.app db upgrade
    # # Sync ./migrations to ./app_migrations
    # rsync -av --delete ./migrations/ ./app_migrations/
fi

if [[ "$APP_MIGRATIONS" == 'migrate' ]]; then
    # # Sync ./app_migrations to ./migrations
    # mkdir -p ./migrations
    # rsync -av --delete ./app_migrations/ ./migrations/
    flask --app hostname_server.app db migrate
    flask --app hostname_server.app db upgrade
    # # Sync ./migrations to ./app_migrations
    # rsync -av --delete ./migrations/ ./app_migrations/
fi

# if [[ "$APP_MIGRATIONS" == 'skip' ]]; then
#     # Sync ./app_migrations to ./migrations  
# fi

if [[ "$APP_DEBUG" == 'true' ]]; then
    pip install debugpy -t /tmp && python /tmp/debugpy --wait-for-client --listen 0.0.0.0:5678 -m flask run --no-debugger --no-reload --host 0.0.0.0 --port 5000
else
    gunicorn -w 1 --bind "0.0.0.0:5000" "hostname_server.app:app"
fi