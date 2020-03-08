#!/bin/bash
rsync -av --exclude=.venv --exclude=rsync_git.sh --exclude=.idea ~/workspace/quaternionphysics/Physics/Webapps/rotations_only/ ~/Documents/Github/rotations_only/
