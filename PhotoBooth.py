#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  PhotoBoothSimple.py - validates email, takes pictures, uploads them 
#                        to dropbox, and tweets random picutures.
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

import sys
import time
import pygame
import copy
import logging
#import Adafruit_MPR121.MPR121 as MPR121
from time import sleep
#from validate_email_address import validate_email
from GmailSender import *
from DropBoxUploader import *
from PictureTaker import *
from Tweeter import *
from random import randint
from Logger import *
from PhotoBoothConfigurator import *
from string import *

class PhotoBooth:

	def __init__ (self):
		local_file_name = ""
		totalPictures = 0
		scrambledFolderName = ""
		full_local_path = ""
		pictureToTweet = ""
		completeFileLists = []

		logger = Logger()

		#upload the config file.
		config = PhotoBoothConfigurator("/home/pi/config.ini", False, logger)

		#config.writeConfig("/home/pi/config.ini", logger)
		soundPlayer = SoundPlayer(config.get_CreationSound(), config.get_ClickSound(), config.get_UploadSound(), config.get_TweetSound(), config.get_TenSecondCountSound(), config.get_FiveSecondCountSound(), config.get_ThreeSecondCountSound(),logger)

		# upload to a dropbox account, connction parameters in class file
		uploader = DropBoxUploader(config.get_DropBoxToken(), config.get_DefaultDropBoxText(), config.get_DefaultDropboxTimeout(), soundPlayer, logger)
		tweeter = Tweeter(config.get_TwitterAPIKey(),config.get_TwitterAPISecret(),config.get_TwitterAccessToken(),config.get_TwitterAccessTokenSecret(), config.get_TwitterDefaultText(), config.get_TwitterHashTag(), soundPlayer, logger)

		# picture taker
		boothCamera = PictureTaker('auto', config.get_DefaultHorizontal(), config.get_DefaultVertical(), config.get_CountdownTime(), soundPlayer, logger)

		emailer = GmailSender(config.get_From(), config.get_Subject(), config.get_Body(), config.get_SMTP(), config.get_Port(), config.get_Username(), config.get_Password(), soundPlayer, logger)

	def validateEmail(self, email):
		return validate_email(email)

	def boothIt(self, email):
		logger.log("*** START OF PICTURE SET FOR %s" % email)

		scrambledFolderName = config.get_RandomFolderName()
		logger.log("main() - Created scrambled name: %s" % scrambledFolderName)

		full_local_path = config.get_FullLocalPath(scrambledFolderName)
		logger.log("main() - Created the local path: %s" % full_local_path)

		if not os.path.exists(full_local_path):
			os.makedirs(full_local_path)

		uploader.generateShare('/' + scrambledFolderName, email)
		logger.log("main() - Created the dropbox path.")

		if ( config.get_NormalEffectCount() > 0 ):
			completeFileLists.append(boothCamera.normal(config.get_FullLocalPathAndFileName(scrambledFolderName), config.get_NormalEffectCount()))

		if ( config.get_WatercolorEffectCount() > 0 ):
           completeFileLists.append(boothCamera.watercolor(config.get_FullLocalPathAndFileName(scrambledFolderName), config.get_WatercolorEffectCount()))

	if ( config.get_SolarizeEffectCount() > 0 ):
            completeFileLists.append(boothCamera.solarize(config.get_FullLocalPathAndFileName(scrambledFolderName), config.get_SolarizeEffectCount()))

	if ( config.get_SketchEffectCount() > 0 ):
            completeFileLists.append(boothCamera.sketch(config.get_FullLocalPathAndFileName(scrambledFolderName), config.get_SketchEffectCount()))

	if ( config.get_DenoiseEffectCount() > 0 ):
            completeFileLists.append(boothCamera.denoise(config.get_FullLocalPathAndFileName(scrambledFolderName), config.get_DenoiseEffectCount()))

	if ( config.get_NegativeEffectCount() > 0 ):
            completeFileLists.append(boothCamera.negative(config.get_FullLocalPathAndFileName(scrambledFolderName), config.get_NegativeEffectCount()))

	if ( config.get_EmbossEffectCount() > 0 ):
            completeFileLists.append(boothCamera.emboss(config.get_FullLocalPathAndFileName(scrambledFolderName), config.get_EmbossEffectCount()))

	if ( config.get_OilpaintEffectCount() > 0 ):
            completeFileLists.append(boothCamera.oilpaint(config.get_FullLocalPathAndFileName(scrambledFolderName), config.get_OilpaintEffectCount()))

	if ( config.get_HatchEffectCount() > 0 ):
            completeFileLists.append(boothCamera.hatch(config.get_FullLocalPathAndFileName(scrambledFolderName), config.get_HatchEffectCount()))

	if ( config.get_GpenEffectCount() > 0 ):
            completeFileLists.append(boothCamera.gpen(config.get_FullLocalPathAndFileName(scrambledFolderName), config.get_GpenEffectCount()))

	if ( config.get_PastelEffectCount() > 0 ):
            completeFileLists.append(boothCamera.pastel(config.get_FullLocalPathAndFileName(scrambledFolderName), config.get_PastelEffectCount()))

	if ( config.get_FilmEffectCount() > 0 ):
            completeFileLists.append(boothCamera.film(config.get_FullLocalPathAndFileName(scrambledFolderName), config.get_FilmEffectCount()))

	if ( config.get_BlurEffectCount() > 0 ):
            completeFileLists.append(boothCamera.blur(config.get_FullLocalPathAndFileName(scrambledFolderName), config.get_BlurEffectCount()))

	if ( config.get_SaturationEffectCount() > 0 ):
            completeFileLists.append(boothCamera.saturation(config.get_FullLocalPathAndFileName(scrambledFolderName), config.get_SaturationEffectCount()))

	if ( config.get_ColorswapEffectCount() > 0 ):
            completeFileLists.append(boothCamera.colorswap(config.get_FullLocalPathAndFileName(scrambledFolderName), config.get_ColorswapEffectCount()))

	if ( config.get_WashedoutEffectCount() > 0 ):
            completeFileLists.append(boothCamera.washedout(config.get_FullLocalPathAndFileName(scrambledFolderName), config.get_WashedoutEffectCount()))

	if ( config.get_PosteriseEffectCount() > 0 ):
            completeFileLists.append(boothCamera.posterise(config.get_FullLocalPathAndFileName(scrambledFolderName), config.get_PosteriseEffectCount()))

	if ( config.get_CartoonEffectCount() > 0 ):
            completeFileLists.append(boothCamera.cartoon(config.get_FullLocalPathAndFileName(scrambledFolderName), config.get_CartoonEffectCount()))

            logger.log('main() - Total pictures taken in this session: %s ' % len(completeFileLists) )

            logger.log('main() - Pictures locations taken in this session: %s ' % completeFileLists )

            # upload to dropbox
            soundPlayer.onUpload()
            flatList = []

            for outer in completeFileLists:
                for inner in outer:
                    uploader.upload(inner, "/" + replace(inner, config.get_DefaultRootFilePath(),""))
                    flatList.append(inner)

	    if ( config.get_PictureRouletteStatus() == 1 ):
                tweeter.TweetIt( flatList[randint(0, len(flatList)-1)] )

            if ( config.get_EmailEnable() == 1 ):
                emailer.sendEmail(email, flatList)
