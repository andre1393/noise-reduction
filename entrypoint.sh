#!/usr/bin/env bash

set -e

COMMAND=${1:-"web"}

case "$COMMAND" in
 web)
   exec gunicorn -c gunicorn.py --log-level 'info' --timeout 120 audio_processor.api.app:app
   ;;
 *)
   exec sh -c "$*"
   ;;
esac