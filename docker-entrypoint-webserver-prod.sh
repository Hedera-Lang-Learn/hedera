#!/bin/bash

export AWS_SECRET_ACCESS_KEY=`aws ssm get-parameter --name /hedera/prod/aws_secret_access_key --with-decryption --output text --query Parameter.Value --region us-east-1`
export AWS_ACCESS_KEY_ID=`aws ssm get-parameter --name /hedera/prod/aws_access_key_id --with-decryption --output text --query Parameter.Value --region us-east-1`
export DATABASE_URL=`aws ssm get-parameter --name /hedera/prod/dj_database_url --with-decryption --output text --query Parameter.Value --region us-east-1`
export DB_HOST=`aws ssm get-parameter --name /hedera/prod/db_host --output text --query Parameter.Value --region us-east-1`
export DB_NAME=`aws ssm get-parameter --name /hedera/prod/db_name --output text --query Parameter.Value --region us-east-1`
export DB_PASSWORD=`aws ssm get-parameter --name /hedera/prod/db_password --with-decryption --output text --query Parameter.Value --region us-east-1`
export DB_PORT=`aws ssm get-parameter --name /hedera/prod/db_port --output text --query Parameter.Value --region us-east-1`
export DB_USER=`aws ssm get-parameter --name /hedera/prod/db_user --with-decryption --output text --query Parameter.Value --region us-east-1`
export DJANGO_SECRET_KEY=`aws ssm get-parameter --name /hedera/prod/django_secret_key --with-decryption --output text --query Parameter.Value --region us-east-1`
export AWS_STORAGE_BUCKET_NAME=`aws ssm get-parameter --name /hedera/prod/aws_storage_bucket_name --output text --query Parameter.Value --region us-east-1`
export EMAIL_BACKEND=`aws ssm get-parameter --name /hedera/email_backend --output text --query Parameter.Value --region us-east-1`
export EMAIL_HOST=`aws ssm get-parameter --name /hedera/email_host --output text --query Parameter.Value --region us-east-1`
export EMAIL_PORT=`aws ssm get-parameter --name /hedera/email_port --output text --query Parameter.Value --region us-east-1`
export EMAIL_HOST_USER=`aws ssm get-parameter --name /hedera/email_host_user --output text --query Parameter.Value --region us-east-1`
export EMAIL_HOST_PASSWORD=`aws ssm get-parameter --name /hedera/email_host_password --with-decryption --output text --query Parameter.Value --region us-east-1`
export DEFAULT_FROM_EMAIL=`aws ssm get-parameter --name /hedera/default_from_email --output text --query Parameter.Value --region us-east-1`
export SENTRY_DSN=`aws ssm get-parameter --name /hedera/sentry_dsn --output text --query Parameter.Value --region us-east-1`
export SENTRY_ENVIRONMENT=prod
export EMAIL_USE_TLS=True
export USE_S3=True
export SITE_ID=4
export REDIS_URL=`aws ssm get-parameter --name /hedera/prod/redis_url --output text --query Parameter.Value --region us-east-1`
export RQ_ASYNC=1


python manage.py makemigrations
python manage.py migrate
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
    --bind :80 \
    --log-level debug