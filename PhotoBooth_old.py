#!/usr/bin/env python

# Darren's Python Photobooth
# Uses Adafruit capacative touch senson to change cameral effects, then take photos.
# It uploads those photos to dropbox and creates a share based on an email address entered by the user.
# Pin 0 is setup
# Pin 10 is Tweet last photo
# Pin 11 is Quit the Program.
# October 16th, 2016


import sys
import time
import pygame
import copy
import logging
import os
import Adafruit_MPR121.MPR121 as MPR121
from time import sleep
from validate_email import validate_email
import uuid
from GmailSender import *
from DropBoxUploader import *
from PictureTaker import *
from Tweeter import *


# PROD Dropbox API KEY
TWO_RIVERS_TOKEN = 'h3rwB9np_CAAAAAAAAAADsqUcPNmBPxGy23OSdLqpOOEzUelYtrkMTFJ56qr_7f-'

# DON'T CHANGE THESE production twitter keys
PROD_2RG_TWITTER_API_KEY = 'OffsCI8Mopb1CpqHhvyvp6EIY' # changed 6El  to 6EI
PROD_2RG_TWITTER_API_SECRET = 'FAEapHzOV6PcejBXkQmOXkKlWhS7Erc2PLYC0O32o019R4ixYQ'
PROD_2RG_TWITTER_ACCESS_TOKEN = '790087781385023488-l4oGWbM18Jfr3ul7hXUc0wEVvXPXVP7' # changed 3ul to 3uI, filed changed back to 3ul
PROD_2RG_TWITTER_ACCESS_TOKEN_SECRET = '4kzBIYaQbT2GFzMEGSY5T82IGxHQhJqa5OA8wFZ1AifV6'
PROD_TWEET_TEXT = 'Halloween Fun at Menagerie at the Two Rivers Gallery' # text you want to accompanie the tweet
PROD_TWEET_HASHTAG = '#menagerie2rg' # hashtag or tags you want to associate wit the tweet.
DEFAULT_PICTURE_LOCATION = "/home/pi/Pictures/"


# DON'T CHANGE THESE test twitter keys
TEST_2RG_TWITTER_API_KEY = 'CLTfXVREV4hJZ7pE83nLfA1if'
TEST_2RG_TWITTER_API_SECRET = 'huqZn2P48VnupXcdLVU71CGQBvfWliE8Gu9aEcZV2zH8nNhDVx'
TEST_2RG_TWITTER_ACCESS_TOKEN = '790060894298382336-ZANslvQlcJdGAizTCC5J4hKCjj7wmgK'
TEST_2RG_TWITTER_ACCESS_TOKEN_SECRET = 'XFFTp9kD2tbFwyRI9TPdn97o3L7hdbQcZWiKfNpVCdgt0'
TEST_TWEET_TEXT = '2RG Menagerie Test Tweet' # text you want to accompanie the tweet
TEST_TWEET_HASHTAG = '#menagerie2rgtest' # hashtag or tags you want to associate wit the tweet.

# Input pin connected to the capacitive touch sensor's IRQ output.
# For the capacitive touch HAT this should be pin 26!
IRQ_PIN = 26

# Don't change the below values unless you know what you're doing.  These help
# adjust the load on the CPU vs. responsiveness of the key detection.
#MAX_EVENT_WAIT_SECONDS = 0.5
#EVENT_WAIT_SLEEP_SECONDS = 0.1
TOUCH_THRESHOLD = 100 # between 0 - 255
RELEASE_THRESHOLD = 100 # between 0 - 255

# Set up detailed logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# logging to file in current dir
fh = logging.FileHandler('log.txt')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)

# logging to interface
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

ch.setFormatter(formatter)
logger.addHandler(ch)

# Create MPR121 instance.
cap = MPR121.MPR121()

# Initialize communication with MPR121 using default I2C bus of device, and
# default I2C address (0x5A).  On BeagleBone Black will default to I2C bus 0.
if not cap.begin():
    logger.critical('Error initializing MPR121.  Check your wiring! Exiting Code')
    sys.exit(1)


# Clear any pending interrupts by reading touch state.
cap.touched()

def main():
    email1 = "darren.ditto@alumni.unbc.ca"
    email2 = "darren.ditto@alumni.unbc.ca"
    local_file_name = ""
    totalPictures = 0
    mirrorTime = 4
    scrambledPathName = ""
    full_local_path = ""

    # upload to a dropbox account, connction parameters in class file
    uploader = DropBoxUploader(TWO_RIVERS_TOKEN)

    # email to Gmail account, connection paramaters in class file
    #emailSender = GmailSender()

    # picture taker
    boothCamera = PictureTaker('auto')

    tweeter = Tweeter(TEST_2RG_TWITTER_API_KEY,TEST_2RG_TWITTER_API_SECRET,TEST_2RG_TWITTER_ACCESS_TOKEN,TEST_2RG_TWITTER_ACCESS_TOKEN_SECRET, TEST_TWEET_TEXT, TEST_TWEET_HASHTAG, logger)
    
    while email1 != email2:
        email1 = raw_input("Please Enter your Email Address: ")
        email2 = raw_input("Please Confirm your Email Address: ")

        if email1 == email2:
            if validate_email(email2) is True:
				logger.info("Valid email address structure provided.")
				scrambledPathName= str(uuid.uuid4())[0:12]
				logger.info("Created scrambled name: %s" % scrambledPathName)                             				

				full_local_path = os.path.join(DEFAULT_PICTURE_LOCATION, scrambledPathName)
				logger.info("Create the local path: %s" % full_local_path)
				
				if not os.path.exists(full_local_path):
					os.makedirs(full_local_path)
					
				logger.info("Create the dropbox path.")
				uploader.generateShare('/' + scrambledPathName, email2, logger)
				break
            else:
                logger.critical('Email Address INVALID')
                continue
        else:
            logger.critical('The email addresses are different.')
            continue

    last_touched = cap.touched()
    
    #logger.info('Setting Thresholds - Touch: %s, Release %s' % (TOUCH_THRESHOLD, RELEASE_THRESHOLD))
    #cap.set_thresholds(TOUCH_THRESHOLD,	RELEASE_THRESHOLD)
    #logger.info('Resetting')
    #cap._reset()
    
    while True:
        current_touched = cap.touched()
        # Check each pin's last and current state to see if it was pressed or released.
        for i in range(12):

            # Each pin is represented by a bit in the touched value.  A value of 1
            # means the pin is being touched, and 0 means it is not being touched.
            pin_bit = 1 << i
            # First check if transitioned from not touched to touched.
            if current_touched & pin_bit and not last_touched & pin_bit:
                logger.info('+++Press Pin Bit: %s' % i)
                 
                # if one of the status bit are hit 0 = start, 10 = tweet, 11 = kill
                if ( i < 10 ):
                    local_file_name = str(uuid.uuid4())[0:8] +".jpg"
                    full_local_file_location = os.path.join(full_local_path, local_file_name)

                logger.info("Going to create file: %s" % full_local_file_location)
                
                if ( i == 0 ):
                    boothCamera.none(full_local_file_location, logger)
                    totalPictures += 1

                elif ( i == 1 ):
                    boothCamera.watercolour(full_local_file_location, logger)
                    totalPictures += 1

                elif ( i == 2 ):
                    boothCamera.solarize(full_local_file_location, logger)
                    totalPictures += 1

                elif ( i == 3 ):
                    boothCamera.gpen(full_local_file_location, logger)
                    totalPictures += 1

                elif ( i == 4 ):
                    boothCamera.emboss(full_local_file_location, logger)
                    totalPictures += 1

                elif ( i == 5 ):
                    boothCamera.oilpaint(full_local_file_location, logger)
                    totalPictures += 1

                elif ( i == 6 ):
                    boothCamera.hatch(full_local_file_location, logger)
                    totalPictures += 1
                    
                elif ( i == 7 ):
                    boothCamera.cartoon(full_local_file_location, logger)
                    totalPictures += 1

                elif ( i == 8 ):
                    boothCamera.colorswap(full_local_file_location, logger)
                    totalPictures += 1

                # pin sensor 9 does not have a pin attached for some reason???  skip it.
                elif ( i == 9 ):
                    pass

                elif ( i == 10 ):
                    if (totalPictures > 0):
                        logger.info("File to tweet: %s" % full_local_file_location)
                        with open(full_local_file_location) as f:
                            tweeter.TweetIt(f, logger)
                else:
                    logger.info("Exit Pin Hit...")
                    sys.exit(1)
                 
                logger.info('Total pictures taken in this session: %s ' % totalPictures )
                    
            # Next check if transitioned from touched to not touched.
            if not current_touched & pin_bit and last_touched & pin_bit:
                logger.info('---DePress Pin Bit: %s' % i)
                
                if (i < 10 ):
                    try:        
                        full_dest_path = os.path.join("/" + scrambledPathName, local_file_name)                        
                        with open(full_local_file_location) as f:
                            uploader.upload(f, full_dest_path, logger)
                    except Exception as err:
                        logger.critical("Failed to upload %s\n%s" % (full_source_path, err))
                    else:
                        logger.info("Exiting Upload.")
                
        # Update last state and wait a short period before repeating.
        last_touched = current_touched
        time.sleep(.1)

if  __name__ =='__main__':
    main()

