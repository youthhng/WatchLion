# WatchLion - parseGmail.py
# File creation: December 20, 2012
# Author: David Sperling
#
# This is a script that is intended to grab messages from gmail and display some
# information about them. Its initial draft is heavily influenced by the thread:
# http://stackoverflow.com/questions/7314942/python-imaplib-to-get-gmail-inbox-subjects-titles-and-sender-name

import email
import imaplib
import json
import os, sys
import re

# Read the users gmail credentials from .gmail.json
credentialJsonString = ""
try:
    # Get the directory that this script is in, and use it to get an absolute
    # path to the JSON file.
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    credentialFileName = os.path.join(dirname, '.gmail.json')
    
    # Read the JSON string from the JSON file
    credentialFile = open(credentialFileName)
    credentialJsonString = credentialFile.read()
    credentialFile.close()
except IOError as e:
    print("({})".format(e))
    print("Try running 'python setup.py' in WatchLion's main directory.")
    exit()
credentials = json.loads(credentialJsonString)


print "Logging into gmail as %s..." % (credentials['gmailName'])

# Log in and select the inbox
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(credentials['gmailName'], credentials['gmailPass'])
mail.list()
mail.select('inbox')

# Get the messages sent by REGISTRAR
print 'Reading messages sent by "REGISTRAR"'
typ, data = mail.search(None, 'FROM', '"REGISTRAR"')

# Create a regular expression looking for a watch list notice.
pattern = re.compile("\((\d+)\) has a seat opening.")

# Iterate through all of REGISTRAR's messages
for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822)')
    
    # Read the message envelope and data into a string for parsing.
    messageString = data[0][1]
    
    # Run the regular expression on the message.
    searchResult = re.search(pattern, messageString)

    # If the pattern was matched, and a seat was open...
    if searchResult:
        # Alert the user
        print num
        print searchResult.group(0)
        courseNumber = int(searchResult.group(1))
        print "Attempting to schedule course number %d..." % (courseNumber)
    
mail.close()
mail.logout()
