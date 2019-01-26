#!/usr/bin/env bash

source venv/bin/activate
python PodLockParser.py $1
deactivate