#!/bin/bash -ex
cd automation_libs

poetry config http-basic.jfrog $JFROG_USERNAME $JFROG_PASSWORD

poetry version ${version}
poetry install --no-dev

poetry build
