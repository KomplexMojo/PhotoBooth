#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#
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

# import the library
from appJar import gui
from picamera import PiCamera
from time import sleep
from validate_email import validate_email

#handle button events.
def reset(button):
    app.setFocus("Email:")
    app.setEntry("Email:", "", callFunction=False)

def confirm(button):
    eml=app.getEntry("Email:")
    is_valid = validate_email(eml)
    print (is_valid)
    
def picture(button):
    with PiCamera() as camera:
        camera.resolution = (1920,1080)
        camera.image_effect = 'none'
        camera.start_preview()
        # Camera warm-up time
        sleep(2)
        camera.capture('/home/pi/Pictures/test.jpg') 
        camera.stop_preview()		

# create a GUI variable called app
app = gui("Login Window", "1024x600")
app.setBg("grey")
app.setFont(18)

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "MakerLab - Photo Booth")
app.setLabelBg("title", "black")
app.setLabelFg("title", "white")


app.addLabelEntry("Email:")

# link the buttons to the function called press
app.addButton("Reset",reset)
app.addButton("Confirm",confirm)
app.addButton("Picture",picture)

app.setFocus("Email:")

# start the GUI
app.go()
