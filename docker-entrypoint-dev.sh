#!/bin/bash

export AWS_SECRET_ACCESS_KEY=`aws ssm get-parameter --name /hedera/dev/aws_secret_access_key --with-decryption --output text --query Parameter.Value --region us-east-1`
export AWS_ACCESS_KEY_ID=`aws ssm get-parameter --name /hedera/dev/aws_access_key_id --with-decryption --output text --query Parameter.Value --region us-east-1`
export DB_HOST=`aws ssm get-parameter --name /hedera/dev/db_host --output text --query Parameter.Value --region us-east-1`
export DB_NAME=`aws ssm get-parameter --name /hedera/dev/db_name --output text --query Parameter.Value --region us-east-1`
export DB_PASSWORD=`aws ssm get-parameter --name /hedera/dev/db_password --with-decryption --output text --query Parameter.Value --region us-east-1`
export DB_PORT=`aws ssm get-parameter --name /hedera/dev/db_port --output text --query Parameter.Value --region us-east-1`
export DB_USER=`aws ssm get-parameter --name /hedera/dev/db_user --with-decryption --output text --query Parameter.Value --region us-east-1`
export DJANGO_SECRET_KEY=`aws ssm get-parameter --name /hedera/dev/django_secret_key --with-decryption --output text --query Parameter.Value --region us-east-1`
export AWS_STORAGE_BUCKET_NAME=`aws ssm get-parameter --name /hedera/dev/aws_storage_bucket_name --output text --query Parameter.Value --region us-east-1`
export EMAIL_HOST=`aws ssm get-parameter --name /hedera/email_host --output text --query Parameter.Value --region us-east-1`
export EMAIL_PORT=`aws ssm get-parameter --name /hedera/email_port --output text --query Parameter.Value --region us-east-1`
export EMAIL_HOST_USER=`aws ssm get-parameter --name /hedera/email_host_user --output text --query Parameter.Value --region us-east-1`
export EMAIL_HOST_PASSWORD=`aws ssm get-parameter --name /hedera/email_host_password --with-decryption --output text --query Parameter.Value --region us-east-1`
export EMAIL_USE_TLS=True
export USE_S3=True
export SITE_ID=2


python manage.py migrate
python manage.py loaddata sites cana livy tolstoy gnt80 morphgnt-lemmatization
python manage.py collectstatic --noinput

sudo gunicorn hedera.wsgi:application \
    --env AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    --env AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    --env DB_HOST=$DB_HOST \
    --env DB_NAME=$DB_NAME \
    --env DB_PASSWORD=$DB_PASSWORD \
    --env DB_PORT=$DB_PORT \
    --env DB_USER=$DB_USER \
    --env DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY \
    --env AWS_STORAGE_BUCKET_NAME=$AWS_STORAGE_BUCKET_NAME \
    --env USE_S3=True \
    --env EMAIL_HOST=$EMAIL_HOST \
    --env EMAIL_PORT=$EMAIL_PORT \
    --env EMAIL_HOST_USER=$EMAIL_HOST_USER \
    --env EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD \
    --env EMAIL_USE_TLS=$EMAIL_USE_TLS \
    --env SITE_ID=$SITE_ID \
    --bind :80 \
    --log-level debug