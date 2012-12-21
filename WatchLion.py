# WatchLion - parseGmail.py
# File creation: December 20, 2012
# Author: David Sperling
#
# This is the main script in the WatchLion software. It repeatedly checks an
# email account using gmailParser, and when a notification email from the
# course watch list is found, it will start the web automation used to schedule
# the course.

import math
import time
from lib import gmailParser

# Set default variables
refreshDelay = 10
verbose = 0

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
except IOError as e:
        print("({})".format(e))
        print("Try running 'python setup.py' in WatchLion's main directory.")
        exit()

            
timeOfLastRefresh = 0;
running = True;
while running:
    while time.time() - timeOfLastRefresh < refreshDelay:
        time.sleep(time.clock())
    timeOfLastRefresh = time.time()
    courseNumber = gmailParser.parseGmail()
    if courseNumber > 0:
        # Try to schedule the course
        if verbose >= 1 : print "Attempting to schedule course number %d..." % (courseNumber)
    
