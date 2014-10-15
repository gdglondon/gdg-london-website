#!/bin/bash

if [ ! -f "api.json" ];
then
  echo "Please create api.json before deploying to App Engine"
  exit 1
fi

# checkout submodules
if [ ! -d "static/web-starter-kit" ];
then
  git submodule init
  git submodule update
fi

# deploy to App Engine
appcfg.py -v update .
