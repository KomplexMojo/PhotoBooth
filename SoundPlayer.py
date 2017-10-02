#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  SoundPlayer.py - plays a static set of sounds to support the photobooth
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

import pygame

class SoundPlayer:

	def __init__ (self, shareCreationSound, defaultClickSound, defaultUploadSound, defaultTweetSound, defaultTenSecondSound, defaultFiveSecondSound, defaultThreeSecondSound, logger):
		self.logger = logger
		self.logger.log("SoundPlayer - Initializing the Sound Player")
		pygame.mixer.pre_init(44100, -16, 12, 512)
		pygame.init()
		self.shareCreationSound = shareCreationSound
		self.defaultClickSound = defaultClickSound
		self.defaultUploadSound = defaultUploadSound
		self.defaultTweetSound = defaultTweetSound
		self.defaultTenSecondSound = defaultTenSecondSound
		self.defaultFiveSecondSound = defaultFiveSecondSound
		self.defaultThreeSecondSound = defaultThreeSecondSound

	def onShareCreation(self):
		self.playSound(self.shareCreationSound)
		pass

	def onPicture(self):
		self.playSound(self.defaultClickSound)
		pass

	def onUpload(self):
		self.playSound(self.defaultUploadSound)
		pass

	def onTweet(self):
		self.playSound(self.defaultTweetSound)
		pass

	def onEmail(self):
		self.playSound(self.shareCreationSound)
		pass

	def tenSecondCountDown(self):
		self.playSound(self.defaultTenSecondSound)
		pass

	def fiveSecondCountDown(self):
		self.playSound(self.defaultFiveSecondSound)
		pass

	def threeSecondCountDown(self):
		self.playSound(self.defaultThreeSecondSound)
		pass

	def playSound(self, sound):
		pygame.mixer.music.load(sound)
		pygame.mixer.music.play()

		while pygame.mixer.music.get_busy() == True:
			continue
		pass
