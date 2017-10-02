#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  DropBoxUploader.py - create a DB share and uploads files to it.
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

import dropbox
import datetime
from SoundPlayer import *

#upload
class DropBoxUploader:
    #SHARE_MESSAGE="Your Two Rivers Gallery Menagerie 2016 Photos are Available for Download and Sharing." # custom share message.
    #DEFAULT_SHARE_EXPIRY_DAYS = 14 # expire the share after 14 days.

	def __init__ (self, token, shareMessage, shareExpiry, soundPlayer, logger):
		self.dbx = dropbox.Dropbox(token)
		self.soundPlayer = soundPlayer
		self.logger = logger
		self.shareMessage = shareMessage
		self.shareExpiry = shareExpiry

# ggenerate the URL
	def generateShare(self, shareName, emailAddress):
		try:
			expires = datetime.datetime.utcnow() + datetime.timedelta(days=self.shareExpiry)
			shared_link_settings = dropbox.sharing.SharedLinkSettings(expires=expires)

			launch = self.dbx.sharing_share_folder('/' + shareName)

			meta_data = launch.get_complete()
			self.logger.log('DropBoxUploader - meta data: %s' % meta_data)

			member_select = dropbox.sharing.MemberSelector.email(emailAddress)
			self.logger.log('DropBoxUploader - member_select data: %s' % member_select)

			access_level = dropbox.sharing.AccessLevel.viewer
			self.logger.log('DropBoxUploader - acess_level: %s' % access_level)

			add_member = dropbox.sharing.AddMember(member_select, access_level)
			self.logger.log('DropBoxUploader - added_member: %s' % add_member)

			self.logger.log("DropBoxUploader - Shared Folder Id: %s" % meta_data.shared_folder_id)
			self.dbx.sharing_add_folder_member(meta_data.shared_folder_id, [add_member], custom_message=self.shareMessage)

		except dropbox.exceptions.ApiError as err:
			self.logger.log_critical("DropBoxUploader - Failed to get share path %s\n%s" % (shareName, err))
		else:
			self.logger.log('DropBoxUploader - Generating Share Sucessful')
			self.soundPlayer.onShareCreation()

	# upload a single file
	def upload(self, fullLocalPath, fullDestinationPath):
		print('Uploading, Please Wait...')
		self.logger.log("DropBoxUploader - Ready to Upload to Dropbox...")
		
		try:
			with open(fullLocalPath) as f:
				self.dbx.files_upload(f,fullDestinationPath)
		except Exception as err:
			self.logger.log_critical("DropBoxUploader - Failed to upload to DropBox folder %s\n===%s" % (fullDestinationPath, err))
		else:
			self.logger.log('DropBoxUploader - Date Modified: ' + self.dbx.files_get_metadata(fullDestinationPath).server_modified.strftime("%Y-%m-%d %H:%M:%S"))
			#self.soundPlayer.onUpload()
			print('Finished Uploading.')
