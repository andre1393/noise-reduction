#!/usr/bin/env bash

set -e

COMMAND=${1:-"web"}

case "$COMMAND" in
 web)
   exec gunicorn -c gunicorn.py --log-level 'info' --timeout 120 noise_reduction.api.app:app
   ;;
 *)
   exec sh -c "$*"
   ;;
esac