# greenthink-library (c) 2013 Ian Dennis Miller

- Makefile: direct action in the working directory, executes locally
- manage.py: application administrative tasks, including databases
- fabfile.py: coordinates deployment, actions execute remotely

# Makefile

## to install

    make install

## to launch an interactive session

    make shell

## to start the dev server locally

    make server

## to test the package locally

    make test

## to watch files for changes and repeatedly re-run tests

    make watch

## to generate documentation

    make doc

## to create and deploy a migration

    export SETTINGS=../etc/dev.conf
    bin/manage.py db migrate -m "description of changes"
    bin/manage.py db upgrade

# fabfile

## to deploy to example.com

fab -H example.com rsync setup

# TODO
