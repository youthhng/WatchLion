# WatchLion - eLionAutomation.py
# File creation: December 2, 2012
# Author: David Sperling
#
# This is a module that uses selenium to automate the process of registering for
# a class on eLion (elion.psu.edu)

from selenium import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
import time

# Opens a Firefox browser and schedules the course with
# the schedule number, [courseNumber], during the [season] semester.
#
# Inputs:
# courseNumber - A 6-digit integer that is the schedule number of the course
# season       - The semester the coures is in. Either "SPRING", "SUMMER", or "FALL".
# userName     - The login name for eLion
# password     - The password for the eLion account with userName.
#
# Outputs: (success, message, complete)
# success  - Returns true if the course was successfully registered, else false
# message  - A string describing the final state of the function
# complete - Returns false if the script was interrupted part way through, else true
def registerForClass(courseNumber, season, userName, password):
    try:
        # Create a new instance of the Firefox driver.
        driver = webdriver.Firefox()
     
        ############################
        # Page 1: eLion login page #
        ############################
        # Go to the eLion login page.
        driver.get("https://webaccess.psu.edu/?cosign-elion.psu.edu&https://elion.psu.edu/cgi-bin/elion-student.exe/launch/ELionMainGUIForCosign/Student")
        # Type the user name in the login box.
        WebDriverWait(driver,10).until(lambda d: d.find_element_by_name("login"))
        loginInputElement = driver.find_element_by_name("login")
        loginInputElement.send_keys(userName)
        # Type the password in the password box.
        passwordInputElement = driver.find_element_by_name("password")
        passwordInputElement.send_keys(password)
        # Submit the form.
        passwordInputElement.submit()

        ###########################
        # Page 2: eLion home page #
        ###########################
        # Go to the course registration page
        driver.get("https://elion.psu.edu/cgi-bin/elion-student.exe/submit/goRegistration")

        ##############################
        # Page 3: semester selection #
        ##############################
        # Find the name of the radio button.
        statusPattern = re.compile("Registration and Drop/Add")
        waitCondition = lambda d: re.search(statusPattern, d.page_source)
        WebDriverWait(driver, 10).until(waitCondition)
        radioPattern = re.compile('<input type="RADIO" value="1@1" name="(\w*)" />\s*%s' % season)
        semesterRadioSearch = re.search(radioPattern, driver.page_source)
        # Click the radio button.
        WebDriverWait(driver,10).until(lambda d: d.find_element_by_name(semesterRadioSearch.group(1)))
        semesterRadioButton = driver.find_element_by_name(semesterRadioSearch.group(1))
        semesterRadioButton.click()
        # Find the name of the continue button.
        continueButtonPattern = re.compile('<input type="SUBMIT" value="Continue" name="(\w*)" />')
        continueButtonSearch = re.search(continueButtonPattern, driver.page_source)
        # Click the continue button.
        continueButton = driver.find_element_by_name(continueButtonSearch.group(1))
        continueButton.click()

        #################################
        # Page 4: password confirmation #
        #################################
        # find the name of the second password field
        password2FieldPattern = re.compile('<input type="password" autocomplete="off" value="" size="25" name="(\w*)" />')
        password2FieldSearch = re.search(password2FieldPattern, driver.page_source)
        # Type the password in the second password box
        WebDriverWait(driver,10).until(lambda d: d.find_element_by_name(password2FieldSearch.group(1)))
        password2InputElement = driver.find_element_by_name(password2FieldSearch.group(1))
        password2InputElement.send_keys(password)
        # Find the OK button
        password2SubmitPattern = re.compile('<input type="SUBMIT" value="   OK   " onclick="//slowOpen\(\);" name="(\w*)" />')
        password2SubmitSearch = re.search(password2SubmitPattern, driver.page_source)
        # Submit the form
        password2SubmitButton = driver.find_element_by_name(password2SubmitSearch.group(1))
        password2SubmitButton.click()
        
        ########################
        # Page 5: registration #
        ########################
        # Type the course number into the input field and submit
        statusPattern = re.compile("Registration and Drop/Add")
        waitCondition = lambda d: re.search(statusPattern, d.page_source)
        WebDriverWait(driver, 10).until(waitCondition)
        WebDriverWait(driver,10).until(lambda d: d.find_element_by_name("InitCourseTextbox1"))
        courseTextbox = driver.find_element_by_name("InitCourseTextbox1")
        courseTextbox.send_keys(courseNumber)
        registrationSubmitPattern = re.compile('<input type="SUBMIT" value="Continue" name="(\w*)" />')
        registrationSubmitSearch = re.search(registrationSubmitPattern, driver.page_source)
        WebDriverWait(driver,10).until(lambda d: d.find_element_by_name(registrationSubmitSearch.group(1)))
        registrationSubmitButton = driver.find_element_by_name(registrationSubmitSearch.group(1))
        registrationSubmitButton.click()

        ########################
        # Page 6: confirmation #
        ########################
        # We have to wait for the page to refresh until either "Error Message"
        # or "Confirmation Message" appears on the page.
        statusPattern = re.compile("(Error Message)|(Confirmation Message)")
        waitCondition = lambda d: re.search(statusPattern, d.page_source)
        WebDriverWait(driver, 10).until(waitCondition)
        src = driver.page_source
        endPattern = re.compile("(Error Message)|(Confirmation Message)")
        endStatus = re.search(endPattern, driver.page_source)
        if endStatus.group(1) == "Error Message":
            failureReasonPattern = re.compile("Error Message.*\n.*<p>(.*)</p>")
            failureReasonSearch = re.search(failureReasonPattern, src)
            driver.quit()
            return (False, failureReasonSearch.group(1), True)
        else:
            driver.quit()
            return (True, "Success!", True)
    except TimeoutException:
        driver.quit()
        return (False, "Timed out", False)
    except:
        driver.quit()
        return (False, "Unexpected error", False)
        
    
