#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  PhotoBoothConfig.py
#  
#  Copyright 2016  <pi@camerabox>
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
##

import ConfigParser
import uuid
import os

class PhotoBoothConfigurator:

	def __init__ (self, fullLocalPath, isProd, logger):
		try:
			self.config = ConfigParser.RawConfigParser()
			self.isProd = isProd
			self.logger = logger
			self.fullLocalPath = fullLocalPath
		except Exception as err:
			self.logger.log_critical("Could not create configuration parser.")
			sys.exit(1)

	def writeConfig(self, fullLocalPath, logger):
		try:		
			# Twitter Test
			self.config.add_section('TwitterTest')
			self.config.set('TwitterTest', '; test twitter account', '')
			self.config.set('TwitterTest','TwitterAPIKey','CLTfXVREV4hJZ7pE83nLfA1if')
			self.config.set('TwitterTest','TwitterAPISecret','huqZn2P48VnupXcdLVU71CGQBvfWliE8Gu9aEcZV2zH8nNhDVx')
			self.config.set('TwitterTest','TwitterAccessToken','790060894298382336-ZANslvQlcJdGAizTCC5J4hKCjj7wmgK')
			self.config.set('TwitterTest','TwitterAccessTokenSecret','XFFTp9kD2tbFwyRI9TPdn97o3L7hdbQcZWiKfNpVCdgt0')
			self.config.set('TwitterTest','TwitterDefaultText', '2RG Menagerie Test Tweet')
			self.config.set('TwitterTest','TwitterHashTag','#menagerie2rgtest')

			# Twitter Prod
			self.config.add_section('TwitterProd')
			self.config.set('TwitterProd', '; production twitter account', '')
			self.config.set('TwitterProd','TwitterAPIKey','OffsCI8Mopb1CpqHhvyvp6EIY')
			self.config.set('TwitterProd','TwitterAPISecret','FAEapHzOV6PcejBXkQmOXkKlWhS7Erc2PLYC0O32o019R4ixYQ')
			self.config.set('TwitterProd','TwitterAccessToken','790087781385023488-l4oGWbM18Jfr3ul7hXUc0wEVvXPXVP7')
			self.config.set('TwitterProd','TwitterAccessTokenSecret','4kzBIYaQbT2GFzMEGSY5T82IGxHQhJqa5OA8wFZ1AifV6')
			self.config.set('TwitterProd','TwitterDefaultText', 'Halloween Fun at Menagerie at the Two Rivers Gallery')
			self.config.set('TwitterProd','TwitterHashTag','#menagerie2rg')

			# Primary Drop Box
			self.config.add_section('PrimaryDropBox')
			self.config.set('PrimaryDropBox', '; dropbox only allows 40 shares in a 24 hour period', '')
			self.config.set('PrimaryDropBox','Token','h3rwB9np_CAAAAAAAAAADsqUcPNmBPxGy23OSdLqpOOEzUelYtrkMTFJ56qr_7f-')
			self.config.set('PrimaryDropBox','ShareText','Your Two Rivers Gallery Menagerie 2016 Photos are Available for Download and Sharing.')
			self.config.set('PrimaryDropBox','ShareTimeout',14)

			# Secondary Drop Box
			self.config.add_section('SecondaryDropBox')				
			self.config.set('SecondaryDropBox', '; dropbox only allows 40 shares in a 24 hour period, set a secondary up in case', '')
			self.config.set('SecondaryDropBox','Token','KUnAr8DSGqAAAAAAAAAACT6ZEw11acsKoh0ttcgucVhuHpcX-DvZkXVxu949tPXB')
			self.config.set('SecondaryDropBox','ShareText','Your Two Rivers Gallery Menagerie 2016 Photos are Available for Download and Sharing.')
			self.config.set('SecondaryDropBox','ShareTimeout',7)

			# Picture Location
			self.config.add_section('PictureLocation')				
			self.config.set('PictureLocation', '; location where pictures are stored locally', '')
			self.config.set('PictureLocation','LocalPictureLocation','/home/pi/Pictures/')

			# Picture Resolution
			self.config.add_section('PictureResolution')				
			self.config.set('PictureResolution', '; location where pictures are stored locally', '')
			self.config.set('PictureResolution','Horizontal',1920)			
			self.config.set('PictureResolution','Vertical',1080)			

			self.config.add_section('PhotoEffectCount')
			self.config.set('PhotoEffectCount', '; one entry for each photo effect you want activated', '')
			self.config.set('PhotoEffectCount','normal',1)
			self.config.set('PhotoEffectCount','watercolor',0)
			self.config.set('PhotoEffectCount','solarize', 0)
			self.config.set('PhotoEffectCount','sketch', 0)
			self.config.set('PhotoEffectCount','denoise', 0)
			self.config.set('PhotoEffectCount','negative', 0)
			self.config.set('PhotoEffectCount','emboss', 0)
			self.config.set('PhotoEffectCount','oilpaint', 0)
			self.config.set('PhotoEffectCount','hatch', 0)
			self.config.set('PhotoEffectCount','gpen', 0)
			self.config.set('PhotoEffectCount','pastel', 0)
			self.config.set('PhotoEffectCount','film', 0)
			self.config.set('PhotoEffectCount','blur', 0)
			self.config.set('PhotoEffectCount','saturation', 0)        
			self.config.set('PhotoEffectCount','colorswap', 0)
			self.config.set('PhotoEffectCount','washedout', 0)
			self.config.set('PhotoEffectCount','posterise', 0)
			self.config.set('PhotoEffectCount','cartoon', 0)

			self.config.add_section('PhotoCountDown')
			self.config.set('PhotoCountDown', '; options for countdown are 10, 5, 3 ', '')
			self.config.set('PhotoCountDown','long',0 )
			self.config.set('PhotoCountDown','medium',0 )
			self.config.set('PhotoCountDown','fast',1 )

			self.config.add_section('PictureRoulette')
			self.config.set('PictureRoulette', '; are we going to randomly tweet something ', '')
			self.config.set('PictureRoulette','enableroulette', 1)

			self.config.add_section('Sounds')
			self.config.set('Sounds', '; various sounds used in the program ', '')
			self.config.set('Sounds','click','/home/pi/Music/shutter.wav')
			self.config.set('Sounds','upload','/home/pi/Music/upload.wav')
			self.config.set('Sounds','creation','/home/pi/Music/mail.wav')
			self.config.set('Sounds','tweet','/home/pi/Music/tweet.wav')
			self.config.set('Sounds','tensecondcount','/home/pi/Music/countdown10.wav')
			self.config.set('Sounds','fivesecondcount','/home/pi/Music/countdown5.wav')
			self.config.set('Sounds','threesecondcount','/home/pi/Music/countdown3.wav')

			self.config.add_section('Email')
			self.config.set('Email', '; send photos through email the following are the setting', '')
			self.config.set('Email', 'enableemail', 1)
			self.config.set('Email', 'from', '2rgmenagerie@gmail.com')
			self.config.set('Email', 'subject', 'Photos from event.')
			self.config.set('Email', 'body', 'Link to your photos')
			self.config.set('Email', '; \/ Do Not Change These \/','')
			self.config.set('Email', 'smtp', 'smtp.gmail.com')
			self.config.set('Email', 'connectport', '587')
			self.config.set('Email', '; ^^^ Do Not Change These ^^^','')
			self.config.set('Email', 'username','2rgmenagerie@gmail.com')
			self.config.set('Email', 'password','makerlab1')

			with open(self.fullLocalPath, 'wb') as configfile:
				self.config.write(configfile)
				self.logger.log("Wrote .ini file, sucessfully.")

		except Exception as err:
			self.logger.log_critical("Could not write configuration file: %s" % self.fullLocalPath)
			pass

	def configSectionMap(self, section):
		self.config.read(self.fullLocalPath)
		dict1 = {}
		options = self.config.options(section)

		for option in options:
			try:
				dict1[option] = self.config.get(section, option)
				if dict1[option] == -1:
					self.logger.log("skip: %s" % option)
			except Exception as err:
				self.logger.log_critical("exception on %s\n%s" % (option,err))
				dict1[option] = None

		return dict1

	def get_TwitterAPIKey(self):
		if self.isProd is True:
			return self.configSectionMap("TwitterProd")['twitterapikey']
		else:
			return self.configSectionMap("TwitterTest")['twitterapikey']

	def get_TwitterAPISecret(self):
		if self.isProd is True:
			return self.configSectionMap("TwitterProd")['twitterapisecret']
		else:
			return self.configSectionMap("TwitterTest")['twitterapisecret']
		
	def get_TwitterAccessToken(self):
		if self.isProd is True:
			return self.configSectionMap("TwitterProd")['twitteraccesstoken']
		else:
			return self.configSectionMap("TwitterTest")['twitteraccesstoken']
		
	def get_TwitterAccessTokenSecret(self):
		if self.isProd is True:
			return self.configSectionMap("TwitterProd")['twitteraccesstokensecret']		
		else:
			return self.configSectionMap("TwitterTest")['twitteraccesstokensecret']		
		
	def get_TwitterDefaultText(self):
		if self.isProd is True:
			return self.configSectionMap("TwitterProd")['twitterdefaulttext']		
		else:
			return self.configSectionMap("TwitterTest")['twitterdefaulttext']		
		
	def get_TwitterHashTag(self):
		if self.isProd is True:
			return self.configSectionMap("TwitterProd")['twitterhashtag']
		else:
			return self.configSectionMap("TwitterTest")['twitterhashtag']	
			
	def get_DefaultPictureLocation(self):
		return self.configSectionMap("PictureLocation")['localpicturelocation']
		
	def get_DropBoxToken(self):
		if self.isProd is True:
			return self.configSectionMap("PrimaryDropBox")['token']
		else:
			return self.configSectionMap("SecondaryDropBox")['token']	

	def get_DefaultDropBoxText(self):
		if self.isProd is True:
			return self.configSectionMap("PrimaryDropBox")['sharetext']
		else:
			return self.configSectionMap("SecondaryDropBox")['sharetext']

	def get_DefaultDropboxTimeout(self):
		if self.isProd is True:
			return int(self.configSectionMap("PrimaryDropBox")['sharetimeout'])
		else:
			return int(self.configSectionMap("SecondaryDropBox")['sharetimeout'])

	def get_DefaultRootFilePath(self):
		return self.configSectionMap("PictureLocation")['localpicturelocation']

	def get_FullLocalPath(self, folderName):
		return os.path.join(self.get_DefaultRootFilePath(), folderName)

	def get_RandomFileName(self):
		return str(uuid.uuid4())[0:8] + ".jpg"

	def get_RandomFolderName(self):
		return str(uuid.uuid4())[0:12]

	def get_FullLocalPathAndFileName(self, folderName):
		return os.path.join(self.get_DefaultRootFilePath() + folderName, self.get_RandomFileName() )

	def get_DefaultHorizontal(self):
		return int(self.configSectionMap("PictureResolution")['horizontal'])

	def get_DefaultVertical(self):
		return int(self.configSectionMap("PictureResolution")['vertical'])

	def get_PictureRouletteStatus(self):
		return int(self.configSectionMap("PictureRoulette")['enableroulette'])

	# effects
	def get_NormalEffectCount(self):
		return int(self.configSectionMap("PhotoEffectCount")['normal'])

	def get_WatercolorEffectCount(self):
		return int(self.configSectionMap("PhotoEffectCount")['watercolor'])

	def get_SolarizeEffectCount(self):
		return int(self.configSectionMap("PhotoEffectCount")['solarize'])

	def get_SketchEffectCount(self):
		return int(self.configSectionMap("PhotoEffectCount")['sketch'])

	def get_DenoiseEffectCount(self):
		return int(self.configSectionMap("PhotoEffectCount")['denoise'])

	def get_NegativeEffectCount(self):
		return int(self.configSectionMap("PhotoEffectCount")['negative'])

	def get_EmbossEffectCount(self):
		return int(self.configSectionMap("PhotoEffectCount")['emboss'])

	def get_OilpaintEffectCount(self):
		return int(self.configSectionMap("PhotoEffectCount")['oilpaint'])

	def get_HatchEffectCount(self):
		return int(self.configSectionMap("PhotoEffectCount")['hatch'])

	def get_GpenEffectCount(self):
		return int(self.configSectionMap("PhotoEffectCount")['gpen'])

	def get_PastelEffectCount(self):
		return int(self.configSectionMap("PhotoEffectCount")['pastel'])

	def get_FilmEffectCount(self):
		return int(self.configSectionMap("PhotoEffectCount")['film'])

	def get_BlurEffectCount(self):
		return int(self.configSectionMap("PhotoEffectCount")['blur'])

	def get_SaturationEffectCount(self):
		return int(self.configSectionMap("PhotoEffectCount")['saturation'])

	def get_ColorswapEffectCount(self):
		return int(self.configSectionMap("PhotoEffectCount")['colorswap'])

	def get_WashedoutEffectCount(self):
		return int(self.configSectionMap("PhotoEffectCount")['washedout'])

	def get_PosteriseEffectCount(self):
		return int(self.configSectionMap("PhotoEffectCount")['posterise'])

	def get_CartoonEffectCount(self):
		return int(self.configSectionMap("PhotoEffectCount")['cartoon'])

	def get_ClickSound(self):
		return self.configSectionMap("Sounds")['click']

	def get_UploadSound(self):
		return self.configSectionMap("Sounds")['upload']

	def get_CreationSound(self):
		return self.configSectionMap("Sounds")['creation']

	def get_TweetSound(self):
		return self.configSectionMap("Sounds")['tweet']

	def get_TenSecondCountSound(self):
		return self.configSectionMap("Sounds")['tensecondcount']

	def get_FiveSecondCountSound(self):
		return self.configSectionMap("Sounds")['fivesecondcount']

	def get_ThreeSecondCountSound(self):
		return self.configSectionMap("Sounds")['threesecondcount']

	def get_CountdownTime(self):
		if (int(self.configSectionMap("PhotoCountDown")['long']) == 1):
			return 10
		elif (int(self.configSectionMap("PhotoCountDown")['medium']) == 1):
			return 5
		else:
			return 3

	def get_EmailEnable(self):
		return int(self.configSectionMap("Email")['enableemail'])

	def get_From(self):
		return self.configSectionMap("Email")['from']

	def get_Subject(self):
		return self.configSectionMap("Email")['subject']

	def get_Body(self):
		return self.configSectionMap("Email")['body']

	def get_SMTP(self):
		return self.configSectionMap("Email")['smtp']

	def get_Port(self):
		return int(self.configSectionMap("Email")['port'])

	def get_Username(self):
		return self.configSectionMap("Email")['username']

	def get_Password(self):
		return self.configSectionMap("Email")['password']

