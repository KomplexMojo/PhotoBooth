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
import re
import string


emailwinsize="800x480"
btnPaddingX=100
btnPaddingY=120
topPad=0
sidePad=0
picSmall=""
picLarge=""

isValid = False
emailFolder = ""
match = None
folderPath = ""

def verifyemail(button):
    global isValid
    global emailFolder
    global match
    global folderPath

    addressToVerify = app.getEntry("email")
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
    #print(match.group())

    if match is None:
        app.setEntryInvalid("email")
    else:
        app.setEntryValid("email")
        print(addressToVerify)
        folderPath = addressToVerify({ord(c): "_" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
        print(folderPath)
        app.hideSubWindow("emailwin")
        app.showSubWindow("mainwin")


def takepic(btn):
    if btn == "Picture One":
        takePic("image_small1.gif", "image_large1.gif")
        app.hideButton("Picture One")
        app.reloadImage("img1", "image_small1.gif")
        app.showImage("img1")
    elif btn == "Picture Two":
        takePic("image_small2.gif", "image_large2.jpg")
        app.hideButton("Picture Two")
        app.reloadImage("img2", "image_small2.gif")
        app.showImage("img2")
    elif btn == "Picture Three":
        takePic("image_small3.gif", "image_large3.jpg")
        app.hideButton("Picture Three")
        app.reloadImage("img3", "image_small3.gif")
        app.showImage("img3")
    else:
        print('end')


def takePic(imagePreview, imageName):
    with PiCamera() as camera:
        camera.resolution = (1080, 1920)
        camera.image_effect = 'none'
        print(camera.image_effect)
        camera.start_preview()
        # Camera warm-up time
        sleep(2)
        camera.capture(imageName)
        sleep(2)
        camera.capture(imagePreview, format='gif', resize=(216, 384))
        camera.stop_preview()


# create a GUI variable called app
app = gui("MakerLab Photobooth by Darren", "fullscreen")
app.setBg("white")
app.setFont(12)

#========= Start Picture Window ============#
app.startSubWindow("mainwin", modal=False)
app.setGeometry(800,480)
app.setBg("white")

app.setSticky("ns")
app.startLabelFrame("Picture One", 0, 0)
app.setInPadding([btnPaddingX, btnPaddingY])
app.setPadding([sidePad, topPad])
app.setBg("white")
app.addIconButton("Picture One", takepic, "md-camera-photo")
app.addImage("img1", "image_small.gif")
app.hideImage("img1")
app.stopLabelFrame()

app.setSticky("ns")
app.startLabelFrame("Picture Two", 0, 1)
app.setInPadding([btnPaddingX, btnPaddingY])
app.setPadding([sidePad, topPad])
app.setBg("white")
app.addIconButton("Picture Two", takepic, "md-camera-photo")
app.addImage("img2", "image_small.gif")
app.hideImage("img2")
app.stopLabelFrame()

app.setSticky("ns")
app.startLabelFrame("Picture Three", 0, 2)
app.setInPadding([btnPaddingX, btnPaddingY])
app.setPadding([sidePad, topPad])
app.setBg("white")
app.addIconButton("Picture Three", takepic, "md-camera-photo")
app.addImage("img3", "image_small.gif")
app.hideImage("img3")
app.stopLabelFrame()
app.stopSubWindow()
#========= Stop Picture Window ============#


#========= Start Email Window ============#
app.startSubWindow("emailwin","Enter Email Address", modal=True)
app.setGeometry(800,480)
app.setBg("white")
app.setSticky("nsew")
app.startLabelFrame("Email Frame", 0, 2)
app.setBg("white")
app.setGeometry(emailwinsize)
app.addValidationEntry("email", 0, 0)
app.setEntryDefault("email", "Enter Email Address")
app.setEntryMaxLength("email", 50)
app.addIconButton("Email", verifyemail, "mail", 0, 1)
app.stopLabelFrame()
app.stopSubWindow()
#========= Stop Email Window ============#

# start the GUI
app.showSplash("MakerLab Photobooth by Darren", fill='white', stripe='black', fg='white', font=33)
app.go(startWindow="emailwin")
