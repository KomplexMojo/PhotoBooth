#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Tweeter.py - tweets a picture with text to a provided account.
#  
#  Copyright 2016  Darren Ditto
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


import time
import subprocess
from twython import Twython
from SoundPlayer import *

# Tweet a photo with a hashtag.
class Tweeter:

	def __init__ (self, apiKey, apiSecret, accessToken, accessTokenSecret, tweetText, tweetHashtag, soundPlayer, logger):
		self.logger = logger
		self.logger.log("Tweeter - Initializing the Twitter")
		self.api = Twython(apiKey,apiSecret,accessToken,accessTokenSecret)
		self.tweetText = tweetText
		self.tweetHashtag = tweetHashtag
		self.soundPlayer = soundPlayer

	def TweetIt(self, fullLocalPath):
		self.logger.log('Tweeter- Uploading photo to twitter')
		print("Tweeting photo, please wait...")

		try:
			with open(fullLocalPath) as photo:
				media_status = self.api.upload_media(media=photo)
				time_now = time.strftime("%I:%M:%S") # get current time
				date_now =  time.strftime("%d/%m/%Y") # get current date
				tweet_txt = " " + self.tweetText + " " + self.tweetHashtag + " " + time_now + " on " + date_now
				self.logger.log("Tweeter- Posting tweet _ %s _ with picture" % tweet_txt)
				self.api.update_status(media_ids=[media_status['media_id']], status=tweet_txt)
		except Exception as err:
			self.logger.log_critical("Tweeter- Failed to tweet %s\n%s" % (photo, err))
		else:
			self.logger.log("Tweeter- Exiting Tweet.")
			self.soundPlayer.onTweet()
			print('Tweeting Complete.')

