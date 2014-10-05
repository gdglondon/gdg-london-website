#!/bin/bash

if [ ! -f "api.json" ];
then
  echo "Please create api.json before deploying to App Engine"
  exit 1
fi

# checkout submodules
if [ ! -d "static/web-starter-kit" ] || [ ! -d "static/devfest-2014" ];
then
  git submodule init
  git submodule update
fi

# build devfest site
jekyll build --source static/devfest-2014 --destination static/devfest

# deploy to App Engine
appcfg.py -v update .
