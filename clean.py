# WatchLion - setup.py
# File creation: December 21, 2012
# Author: David Sperling
#
# This script removes all of the various files that are created during
# WatchLion's use.

from subprocess import call

# remove files
call(["rm", "etc/.gmail.json"])
call(["rm", "config"])
