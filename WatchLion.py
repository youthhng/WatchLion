# WatchLion - parseGmail.py
# File creation: December 20, 2012
# Author: David Sperling
#
# This is the main script in the WatchLion software. It repeatedly checks an
# email account using gmailParser, and when a notification email from the
# course watch list is found, it will start the web automation used to schedule
# the course.

import json
import math
import time
from lib import gmailParser
from lib import eLionAutomation

# Set default variables
refreshDelay = 10
verbose = 0

credentialJsonString = ""
try:
    # Set some variables from a config file.
    for line in open('config'):
        splitLine = line.split()
        if len(splitLine) == 2:
            if splitLine[0] == 'refreshDelay':
                refreshDelay = float(splitLine[1])
                if verbose >= 3 : print "refreshDelay = %f" % refreshDelay
            if splitLine[0] == 'verbose':
                verbose = int(splitLine[1])
                if verbose >= 3 : print "verbose = %d" % verbose
                     
    # Read the users credentials from .credentials.json
    credentialFile = open('etc/.credentials.json')
    credentialJsonString = credentialFile.read()
    credentialFile.close()
    
except IOError as e:
        print("({})".format(e))
        print("Try running 'python setup.py' in WatchLion's main directory.")
        exit()
credentials = json.loads(credentialJsonString)

            
timeOfLastRefresh = 0;
running = True;
while running:
    while time.time() - timeOfLastRefresh < refreshDelay:
        time.sleep(time.clock())
    timeOfLastRefresh = time.time()
    semester, courseNumber = gmailParser.parseGmail(credentials['gmailName'], credentials['gmailPass'])
    if courseNumber > 0:
        # Try to schedule the course
        if verbose >= 1 : print "Attempting to schedule course number %d..." % (courseNumber)
        didRegister, message = eLionAutomation.registerForClass(courseNumber, semester, credentials['eLionName'], credentials['eLionPass'])
        if didRegister:
            print "Registration successful!"
        else:
            print "Registration failed."
            print message
        
    
