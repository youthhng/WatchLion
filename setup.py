# WatchLion - setup.py
# File creation: December 20, 2012
# Author: David Sperling
#
# This script is used for the initial setup of WatchLion. It is mostly used for
# getting user credentials.

import json
import getpass
from subprocess import call

# create the default configuration file
call(["cp", ".defaultConfig", "config"])

# Get the user's gmail credentials.
gmailName = raw_input('Enter your gmail username:')
gmailPass = getpass.getpass('Enter your gmail password:')
eLionName = raw_input('Enter your eLion username:')
eLionPass = getpass.getpass('Enter your eLion password:')

# Open the json file to hold the credentials
jsonFile = open('etc/.credentials.json', 'w+')

# Encode the credentials into json
jsonString = json.dumps({'gmailName':gmailName,'gmailPass':gmailPass,'eLionName':eLionName,'eLionPass':eLionPass})

# Write the jsonString to the file
jsonFile.write(jsonString)
jsonFile.close()
