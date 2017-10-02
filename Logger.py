#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Logger.py - logs events to a file and stream.
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

import datetime
import logging


#Logger
class Logger:

	LOGGER_FILE = "log.txt"

	def __init__ (self):
		logger = logging.getLogger()
		#self.level = level
		logger.setLevel(logging.INFO)
		formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

		# logging to file in current dir
		fh = logging.FileHandler(self.LOGGER_FILE)
		fh.setLevel(logging.INFO)
		fh.setFormatter(formatter)
		logger.addHandler(fh)

		# logging to interface
		ch = logging.StreamHandler()
		ch.setLevel(logging.WARNING)
		ch.setFormatter(formatter)
		logger.addHandler(ch)

	# default is a message.
	def log(self, message):
		logging.info(message)

	def log_critical(self, message):
		logging.critical(message)
		
	def log_warning(self, message):
		logging.warning(message)

