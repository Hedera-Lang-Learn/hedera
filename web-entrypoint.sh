#!/bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata sites
python manage.py collectstatic --noinput
sudo gunicorn hedera.wsgi:application \
    --env AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    --env AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    --env DATABASE_URL=$DATABASE_URL \
    --env DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY \
    --env AWS_STORAGE_BUCKET_NAME=$AWS_STORAGE_BUCKET_NAME \
    --env USE_S3=True \
    --env EMAIL_BACKEND=$EMAIL_BACKEND \
    --env EMAIL_HOST=$EMAIL_HOST \
    --env EMAIL_PORT=$EMAIL_PORT \
    --env EMAIL_HOST_USER=$EMAIL_HOST_USER \
    --env EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD \
    --env DEFAULT_FROM_EMAIL=$DEFAULT_FROM_EMAIL \
    --env EMAIL_USE_TLS=$EMAIL_USE_TLS \
    --env SITE_ID=$SITE_ID \
    --env REDIS_URL=$REDIS_URL \
    --env RQ_ASYNC=$RQ_ASYNC \
    --env SENTRY_DSN="$SENTRY_DSN" \
    --env SENTRY_ENVIRONMENT=$SENTRY_ENVIRONMENT \
    --env DJANGO_DEBUG=$DJANGO_DEBUG \
    --env CONSUMER_KEY=$CONSUMER_KEY \
    --env LTI_SECRET=$LTI_SECRET \
    --env PDF_SERVICE_ENDPOINT=$PDF_SERVICE_ENDPOINT \
    --env PDF_SERVICE_TOKEN=$PDF_SERVICE_TOKEN \
    --env IS_LTI=$IS_LTI \
    --bind :80 \
    --log-level debug