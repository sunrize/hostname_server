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


gunicorn -w 1 --bind "0.0.0.0:5000" "hostname_server.app:app"