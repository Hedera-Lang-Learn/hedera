#!/bin/bash

python manage.py rqworker ${RQ_QUEUES:-default}