# WatchLion - setup.py
# File creation: December 20, 2012
# Author: David Sperling
#
# This script is used for the initial setup of WatchLion. It is mostly used for
# getting user credentials.

import json

# Get the user's gmail credentials.
gmailName = raw_input('Enter your gmail username:')
gmailPass = raw_input('Enter your gmail password:')

# Open the json file to hold the credentials
jsonFile = open('gmailParser/.gmail.json', 'w+')

# Encode the credentials into json
jsonString = json.dumps({'gmailName': gmailName, 'gmailPass':gmailPass})

# Write the jsonString to the file
jsonFile.write(jsonString)
jsonFile.close()
