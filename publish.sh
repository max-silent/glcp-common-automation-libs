#!/bin/bash
cd automation_libs
poetry config repositories.publish-jfrog https://aruba.jfrog.io/aruba/api/pypi/pypi-local

poetry version ${version}

poetry publish -r publish-jfrog --username $JFROG_USERNAME --password $JFROG_PASSWORD
