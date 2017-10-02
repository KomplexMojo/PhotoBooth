#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  GmailSender.py - sends email via gmail with pictures as attachments.
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
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.MIMEBase import MIMEBase
from email import Encoders
import os

class GmailSender:
	def __init__ (self, from_addr, msg_subject, msg_body, SMTP, port, username, password, soundPlayer, logger):
		self.from_addr = from_addr
		self.msg_subject = msg_subject
		self.msg_body = msg_body
		self.username = username
		self.password = password
		self.soundPlayer = soundPlayer
		self.logger = logger
		#self.SMTP = SMTP
		#self.port = port
		self.server = smtplib.SMTP(SMTP, port)
		self.logger.log("GmailSender - Connected to server: %s / %s" % (SMTP, port))

	def sendEmail(self, to_addr, fileList):

		# set up the message
		msg = MIMEMultipart()
		msg['From'] = self.from_addr
		msg['To'] = to_addr
		msg['Subject'] = self.msg_subject
		msg.attach(MIMEText(self.msg_body, 'html'))

		# try the send
		try:
			self.server.ehlo()
			self.server.starttls()
			self.server.ehlo()
			self.server.login(self.username, self.password)
			self.logger.log("GmailSender - Logging in as: %s" % self.username)

			for x in fileList:
				img_data = open(x, 'rb')
				image = MIMEImage(img_data.read(), name=os.path.basename(x))
				img_data.close()
				msg.attach(image)
				self.logger.log("GmailSender - Addarched File: %s" % x)

			self.server.sendmail(self.from_addr, to_addr, msg.as_string())
			self.server.quit()

		except Exception as err:
			self.logger.log_critical("GmailSender - Could not send email to: %s - %s" % (to_addr, err))
		else:
			self.logger.log("GmailSender - Sent email: %s" % to_addr)
			self.soundPlayer.onEmail()
