#!/bin/bash

set -eu

export PYTHONBUFFERED=true

VIRTUALENV=./.venv

if [ ! -d $VIRTUALENV ]; then
python3 -m venv $VIRTUALENV
fi


if [! -f $VIRTUALENV/bin/pip]; then
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/pip/3.7/get-pip.py -o get-pip.py | $VIRTUALENV/bin/python
fi

$VIRTUALENV/bin/python -m pip install --upgrade pip
$VIRTUALENV/bin/python -m pip install -r requirements.txt   

$VIRTUALENV/bin/python manage.py makemigrations
$VIRTUALENV/bin/python manage.py migrate


$VIRTUALENV/bin/python manage.py runserver
