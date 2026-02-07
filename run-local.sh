#!/bin/sh
# Run the Xenon Flask app locally for development
export FLASK_APP=xenon.app
export FLASK_ENV=development
export FLASK_DEBUG=1
pipenv run flask run --host=127.0.0.1 --port=5000
