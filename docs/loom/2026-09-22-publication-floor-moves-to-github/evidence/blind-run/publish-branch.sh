#!/bin/sh
# Publish branch $2 of the clone at $1 to the test repository's origin.
cd "$1" && git push -q origin "$2"
