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


CAMERA="\u1F4F7"

isvalid = False
def confirm(button):
    global isvalid
    eml=app.getEntry("email")
    isvalid = validate_email(eml)
    if isvalid: app.setEntryValid("email")
    else:
        app.setEntryInvalid("email")
        app.updateEntryDefault("email","Enter Valid Email")
        isvalid = isvalid;
        isvalid = not isvalid;
     
clicked = False
def takepic(btn):
    if btn == "Press Me":
        global clicked
        if clicked:
            app.setEntryDefault("email","Sending...")
            sleep(1)
            with PiCamera() as camera:
                camera.resolution = (1080,1920)
                camera.image_effect = 'none'
                print(camera.image_effect)
                camera.start_preview()
                # Camera warm-up time
                sleep(2)
                camera.capture('/home/pi/Pictures/test_full.jpg')
                sleep(2)
                camera.capture('/home/pi/Pictures/test_small.gif',format = 'gif', resize=(432, 576)) 
                camera.stop_preview()
            app.setImage("clickme", "/home/pi/Pictures/test_small.gif")
            sleep(10)
            app.setImage("clickme", "/home/pi/PhotoBooth/SourceImages/pressme_new1.jpg")
            app.setEntryDefault("email","Enter Email Address")

        else: app.setImage("clickme", "/home/pi/PhotoBooth/SourceImages/pressme_new1.jpg")
        clicked = not clicked

# create a GUI variable called app
app = gui("MakerLab Photobooth by Darren", "480x640")
app.setBg("grey")
app.setFont(12)

app.addValidationEntry("email",0,1)
app.setEntryDefault("email","Enter Email Address")
app.setEntryMaxLength("email",50)
#app.setFocus("email")

# link the buttons to the function called press
app.addButton(CAMERA,confirm,0,2)

app.startLabelFrame("Picture", 1,0,3)
app.addImage("clickme", '/home/pi/PhotoBooth/SourceImages/pressme_new1.jpg')
#app.setImageSubmitFunction("clickme", takepic)
app.addButton("Press Me",takepic)
app.stopLabelFrame()

# start the GUI

app.showSplash("MakerLab Photobooth by Darren", fill='white', stripe='black', fg='white', font=44)
app.go()
