#!/usr/bin/env bash
DIR=$(dirname $0)

stat $DIR/../api.json >/dev/null 2>&1
if [ "$?" != "0" ]; then
  echo "Error: ./api.json not found."
  echo
  echo "  It is required for Google+ integration."
  echo "  See ./api.example.json for instructions."
  exit 1
fi

which pylint >/dev/null 2>&1
if [ "$?" != "0" ]; then
  echo "Error: pylint not found."
  echo
  echo "  pip install -r requirements.txt"
  exit 1
fi

which dev_appserver.py >/dev/null 2>&1
if [ "$?" != "0" ]; then
  echo "Error: dev_appserver.py not found."
  echo
  echo "  You can install AppEngine Launcher via Homebrew (Cask):"
  echo "    brew install Caskroom/homebrew-cask/googleappengine"
  echo "  See https://cloud.google.com/appengine/downloads for more."
  exit 1
fi