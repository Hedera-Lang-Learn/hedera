#!/bin/bash -ex

python manage.py rqworker ${RQ_QUEUES:-default}
