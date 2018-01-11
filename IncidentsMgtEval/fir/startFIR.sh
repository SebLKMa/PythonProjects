#! /usr/bin/env bash
source ./env-FIR/bin/activate
cd FIR
./manage.py runserver 0.0.0.0:8000
