# WatchLion - parseGmail.py
# File creation: December 20, 2012
# Author: David Sperling
#
# This is a module that is intended to grab messages from gmail and display some
# information about them. Its initial draft is heavily influenced by the thread:
# http://stackoverflow.com/questions/7314942/python-imaplib-to-get-gmail-inbox-subjects-titles-and-sender-name

import email
import imaplib
import json
import re

def parseGmail():
    # Set default variables
    verbose = 0

    # Set some variables from a config file
    for line in open('config'):
        splitLine = line.split()
        if len(splitLine) == 2:
            if splitLine[0] == 'verbose':
                verbose = int(splitLine[1])
                if verbose >= 3 : print "verbose = %d" % verbose

    # Read the users gmail credentials from .gmail.json
    credentialJsonString = ""
    try:        
        # Read the JSON string from the JSON file
        credentialFile = open('gmailParser/.gmail.json')
        credentialJsonString = credentialFile.read()
        credentialFile.close()
    except IOError as e:
        print("({})".format(e))
        print("Try running 'python setup.py' in WatchLion's main directory.")
        exit()
    credentials = json.loads(credentialJsonString)


    if verbose >= 2 : print "Logging into gmail as %s..." % (credentials['gmailName'])

    # Log in and select the inbox
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(credentials['gmailName'], credentials['gmailPass'])
    mail.list()
    mail.select('inbox')

    # Get the messages sent by REGISTRAR
    if verbose >= 2 : print 'Reading messages sent by "REGISTRAR"'
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
            if verbose >= 1 : print searchResult.group(0)
            courseNumber = int(searchResult.group(1))
            if verbose >= 1 : print "Attempting to schedule course number %d..." % (courseNumber)
            return courseNumber
        
    mail.close()
    mail.logout()
    return -1
