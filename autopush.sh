#!/bin/bash

git add .
if [ "$1" ]; then
#  git commit -m \""$@"\"
  git commit -m "$(echo \""$@"\")"
else
  git commit -m "autopush"
fi
git push
