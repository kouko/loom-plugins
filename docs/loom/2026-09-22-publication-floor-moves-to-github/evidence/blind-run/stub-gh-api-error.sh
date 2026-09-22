#!/bin/sh
# Stand-in gh whose API calls fail as a server error would.
echo "gh: Server Error (HTTP 502)" >&2
exit 1
