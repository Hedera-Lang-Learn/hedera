#!/bin/bash
gunicorn basic.wsgi:application --bind 127.0.0.1:8001 --daemon
service nginx start