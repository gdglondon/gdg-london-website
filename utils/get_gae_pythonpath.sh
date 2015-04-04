#!/usr/bin/env bash
LINK=$(which dev_appserver.py)
REAL_GAE_PATH=$(python -c "import os; print os.path.realpath('$LINK')")

export PYTHONPATH=$(dirname $REAL_GAE_PATH)
GAE_PYTHONPATH=$(python -c 'import _python_runtime; print ":".join(_python_runtime.EXTRA_PATHS)')
echo $GAE_PYTHONPATH
