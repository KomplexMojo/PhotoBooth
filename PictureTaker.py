#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  PictureTaker.py - takes a picture based on predefined camera effects
#                    saves it to local file
#  
#  Copyright 2016 Darren Ditto
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
import itertools
from picamera import PiCamera
from SoundPlayer import *

class PictureTaker:

	def __init__ (self, mode, defaultHorizontal, defaultVertical, photoCountdown, soundPlayer, logger):
		self.mode = mode
		self.soundPlayer = soundPlayer
		self.logger = logger
		self.defaultHorizontal = defaultHorizontal
		self.defaultVertical = defaultVertical
		self.photoCountdown = photoCountdown

	def click(self, effect, destination):      
		with PiCamera() as camera:
			self.logger.log('PictureTaker- Initializing Camera')
			camera.resolution = (self.defaultHorizontal, self.defaultVertical)
			camera.image_effect = effect
			camera.start_preview()

			if ( self.photoCountdown == 10 ):
				self.soundPlayer.tenSecondCountDown()
			elif ( self.photoCountdown == 5 ):
				self.soundPlayer.fiveSecondCountDown()
			else:
				self.soundPlayer.threeSecondCountDown()

			time.sleep(.5)
			camera.capture(destination) 
			self.soundPlayer.onPicture()
			camera.stop_preview()

			self.logger.log("PictureTaker- Picture Taken: %s with effect: %s"  % (destination,effect))

	def normal(self, destination, count):
		fileList = []
		for i in range(count):
			self.click('none', destination)
			fileList.append(destination)
		return fileList

	def watercolor(self, destination, count):
		fileList = []
		for i in range(count):
			self.click('watercolor', destination)
			fileList.append(destination)
		return fileList

	def solarize(self, destination, count):
		fileList = []
		for i in range(count):
			self.click('solarize', destination)
			fileList.append(destination)
		return fileList

	def sketch(self, destination, count):
		fileList = []
		for i in range(count):
			self.click('sketch', destination)
			fileList.append(destination)
		return fileList

	def denoise(self, destination, count):
		fileList = []
		for i in range(count):
			self.click('denoise', destination)
			fileList.append(destination)
		return fileList

	def negative(self, destination, count):
		fileList = []
		for i in range(count):
			self.click('negative', destination)
			fileList.append(destination)
		return fileList

	def emboss(self, destination, count):
		fileList = []
		for i in range(count):
			self.click('emboss', destination)
			fileList.append(destination)
		return fileList

	def oilpaint(self, destination, count):
		fileList = []
		for i in range(count):
			self.click('oilpaint', destination)
			fileList.append(destination)
		return fileList

	def hatch(self, destination, count):
		fileList = []
		for i in range(count):
			self.click('hatch', destination)
			fileList.append(destination)
		return fileList

	def gpen(self, destination, count):
		fileList = []
		for i in range(count):
			self.click('gpen', destination)
			fileList.append(destination)
		return fileList

	def pastel(self, destination, count):
		fileList = []
		for i in range(count):
			self.click('pastel', destination)    
			fileList.append(destination)
		return fileList

	def film(self, destination, count):
		fileList = []
		for i in range(count):
			self.click('film', destination)
			fileList.append(destination)
		return fileList

	def blur(self, destination, count):
		fileList = []
		for i in range(count):
			self.click('blur', destination)
			fileList.append(destination)
		return fileList

	def saturation(self, destination, count):
		fileList = []
		for i in range(count):
			self.click('saturation', destination)        
			fileList.append(destination)
		return fileList

	def colorswap(self, destination, count):
		fileList = []
		for i in range(count):
			self.click('colorswap', destination)
			fileList.append(destination)
		return fileList

	def washedout(self, destination, count):
		fileList = []
		for i in range(count):
			self.click('washedout', destination)
			fileList.append(destination)
		return fileList

	def posterise(self, destination, count):
		fileList = []
		for i in range(count):
			self.click('posterise', destination)
			fileList.append(destination)
		return fileList

	def cartoon(self, destination, count):
		fileList = []
		for i in range(count):
			self.click('cartoon', destination)
			fileList.append(destination)
		return fileList
