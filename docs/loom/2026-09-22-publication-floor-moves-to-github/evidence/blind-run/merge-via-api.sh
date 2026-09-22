#!/bin/sh
# Ask GitHub to merge pull request $1 of the test repository (squash).
gh api -X PUT "repos/kouko/loom-floor-test/pulls/$1/merge" -f merge_method=squash 2>&1
echo "exit=$?"
