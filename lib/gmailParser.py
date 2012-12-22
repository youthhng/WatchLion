# WatchLion - parseGmail.py
# File creation: December 20, 2012
# Author: David Sperling
#
# This is a module that is intended to grab messages from gmail and display some
# information about them. Its initial draft is heavily influenced by the thread:
# http://stackoverflow.com/questions/7314942/python-imaplib-to-get-gmail-inbox-subjects-titles-and-sender-name

import email
import imaplib
import re
import time

# Parses the gmail account looking for notifications from the course watch list
# If a notification is found, the function returns the course number
# If no notifications are found, the function returns -1
# For other errors, the function returns -2
# userName is the gmail userName to use
# password is the password for the userName
def parseGmail(userName, password):
    # Set default variables
    verbose = 0

    # Set some variables from a config file
    try:
        for line in open('config'):
            splitLine = line.split()
            if len(splitLine) == 2:
                if splitLine[0] == 'verbose':
                    verbose = int(splitLine[1])
                    if verbose >= 3 : print "verbose = %d" % verbose
    except IOError as e:
        print("({})".format(e))
        print("Try running 'python setup.py' in WatchLion's main directory.")
        return -2

    if verbose >= 2 : print "Logging into gmail as %s..." % (credentials['gmailName'])

    # Log in and select the inbox
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(userName, password)
    mail.list()
    mail.select('inbox')

    # Get the messages sent by REGISTRAR
    if verbose >= 2 : print 'Reading messages sent by "REGISTRAR"'
    typ, data = mail.search(None, 'FROM', '"REGISTRAR"')

    # Create a regular expression looking for a watch list notice.
    pattern = re.compile("\w+ \d+ section \d+ for (\w+) \d+ \((\d+)\) has a seat opening.")

    # Iterate through all of REGISTRAR's messages
    for num in data[0].split():
        typ, data = mail.fetch(num, '(RFC822)')
        
        # Read the message envelope and data into a string for parsing.
        messageString = data[0][1]
        
        # Run the regular expression on the message.
        searchResult = re.search(pattern, messageString)

        # If the pattern was matched, and a seat was open...
        if searchResult:
            # Check the time the email was sent
            datePattern = re.compile("DATE: (.*) EST")
            dateSearch = re.search(datePattern, messageString)
            if dateSearch:
                if verbose >= 3: print dateSearch.group(0)
                print dateSearch.group(1)
                sentDate = time.strptime(dateSearch.group(1), "%a, %d %b %Y %H:%M:%S")
                currentTime = time.time()
                emailTime = time.mktime(sentDate)
                diffTime = ((currentTime - emailTime)/60)
                if verbose >= 2:
                    if diffTime > 119:
                        print "Recieved %d hours ago" % (diffTime/60)
                    else:
                        print "Recieved %d minutes ago" % diffTime
        
            # Alert the user
            if verbose >= 3 : print "%s\n\n" % messageString
            if verbose >= 1 : print searchResult.group(0)
            return (searchResult.group(1), int(searchResult.group(2)))
        
    mail.close()
    mail.logout()
    return ("", -1)
