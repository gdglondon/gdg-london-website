#!/bin/bash

if [ ! -f "api.json" ];
then
   echo "Please create api.json before deploying to App Engine"
   exit 1
fi

# checkout submodules
git submodule init
git submodule update

# deploy to App Engine
appcfg.py update .