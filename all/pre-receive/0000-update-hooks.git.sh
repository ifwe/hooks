#!/bin/bash -ex

#
# Make server repositories receiving pushes first update their hooks directory.
#

GIT_HOOKS_DIR=`git rev-parse --git-dir`/hooks
echo "Updating hooks in $GIT_HOOKS_DIR..."
pushd $GIT_HOOKS_DIR
git fetch origin
git reset --hard origin/master
popd
echo "done"
