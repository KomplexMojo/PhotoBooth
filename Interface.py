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
import os
import string


winsize="800x474"
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
fileName = ""

def verifyemail(button):
    global isValid
    global emailFolder
    global match
    global folderPath
    global fileName

    addressToVerify = app.getEntry("emailtxt")
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
    #print(match.group())

    if match is None:
        app.setEntryInvalid("emailtxt")
    else:
        app.setEntryValid("emailtxt")
        fileName = re.sub('[^a-zA-Z0-9]', '_', match.group(0))
        folderPath = "/home/pi/Pictures/" + re.sub('[^a-zA-Z0-9]', '_', match.group(0)) + "/"
        print(folderPath)
        app.hideSubWindow("emailwin")
        app.showSubWindow("picwin")


def takepic(btn):
    if btn == "Picture One":
        takePic(fileName + "_small_1" + ".png", fileName + "_large_1" + ".png")
        app.hideButton("Picture One")
        app.reloadImage("img1", folderPath + fileName + "_small_1" + ".png")
        app.showImage("img1")
    elif btn == "Picture Two":
        takePic(fileName + "_small_2" + ".png", fileName + "_large_2" + ".png")
        app.hideButton("Picture Two")
        app.reloadImage("img2", folderPath + fileName + "_small_2" + ".png")
        app.showImage("img2")
    elif btn == "Picture Three":
        takePic(fileName + "_small_3" + ".png", fileName + "_large_3" + ".png")
        app.hideButton("Picture Three")
        app.reloadImage("img3", folderPath + fileName + "_small_3" + ".png")
        app.showImage("img3")
        sleep(3)
        resetInterface()
    else:
        print('end')


def resetInterface():
    app.clearEntry("emailtxt", callFunction=False, setFocus=True)
    app.showSubWindow("emailwin")
    app.hideSubWindow("picwin")
    app.reloadImage("img1", "/home/pi/PhotoBooth/SourceImages/default_small.png")
    app.reloadImage("img2", "/home/pi/PhotoBooth/SourceImages/default_small.png")
    app.reloadImage("img3", "/home/pi/PhotoBooth/SourceImages/default_small.png")



def takePic(imagePreview, imageName):

    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    with PiCamera() as camera:
        camera.resolution = (1080, 1920)
        camera.image_effect = 'none'
        camera.start_preview()
        # Camera warm-up timegit
        sleep(2)
        camera.capture(folderPath + imagePreview, format='png', resize=(216, 384))
        sleep(1)
        camera.capture(folderPath + imageName)
        camera.stop_preview()

# create a GUI variable called app
app = gui("MakerLab Photobooth by Darren", "fullscreen")
app.setBg("white")
#app.setFont(12)

#========= Start Picture Window ============#
app.startSubWindow("picwin", modal=False)
app.setGeometry(winsize)
app.setBg("white")

app.setSticky("ns")
app.startLabelFrame("Picture One", 0, 0)
app.setInPadding([btnPaddingX, btnPaddingY])
app.setPadding([sidePad, topPad])
app.setBg("white")
app.addIconButton("Picture One", takepic, "md-camera-photo")
app.addImage("img1", "/home/pi/PhotoBooth/SourceImages/default_small.png")
app.hideImage("img1")
app.stopLabelFrame()

app.setSticky("ns")
app.startLabelFrame("Picture Two", 0, 1)
app.setInPadding([btnPaddingX, btnPaddingY])
app.setPadding([sidePad, topPad])
app.setBg("white")
app.addIconButton("Picture Two", takepic, "md-camera-photo")
app.addImage("img2", "/home/pi/PhotoBooth/SourceImages/default_small.png")
app.hideImage("img2")
app.stopLabelFrame()

app.setSticky("ns")
app.startLabelFrame("Picture Three", 0, 2)
app.setInPadding([btnPaddingX, btnPaddingY])
app.setPadding([sidePad, topPad])
app.setBg("white")
app.addIconButton("Picture Three", takepic, "md-camera-photo")
app.addImage("img3", "/home/pi/PhotoBooth/SourceImages/default_small.png")
app.hideImage("img3")
app.stopLabelFrame()
app.stopSubWindow()
#========= Stop Picture Window ============#

#========= Start Email Window ============#
app.startSubWindow("emailwin","Enter Email Address", modal=True)
app.setGeometry(winsize)
app.setBg("white")
app.setSticky("nsew")

app.startLabelFrame("Email Frame", 0, 0)
app.setBg("white")

app.addValidationEntry("emailtxt", 0, 1)
app.getEntryWidget("emailtxt").config(font="Verdana 12 normal")
app.setEntryDefault("emailtxt", "Enter Email Address")
app.setEntryMaxLength("emailtxt", 100)
app.setEntryWidth("emailtxt", 50)
app.setEntryHeight("emailtxt", 12)

app.addIconButton("emailbtn", verifyemail, "mail", 0, 2)
app.setButtonPadding("emailbtn", [10, 10])

app.addLabel("step1", "Step 1 - Use the attached keyboard to enter your email address.", 1, 0, 2)
app.getLabelWidget("step1").config(font="Verdana 16 normal")
app.addLabel("step2", "Step 2 - Press the email button to confirm email address.", 2, 0, 2)
app.getLabelWidget("step2").config(font="Verdana 16 normal")
app.addLabel("step3", "Step 3 - In the next screen press a camera button (left to right).", 3, 0, 2)
app.getLabelWidget("step3").config(font="Verdana 16 normal")
app.addLabel("step4", "Step 4 - Pose for 3 seconds.", 4, 0, 2)
app.getLabelWidget("step4").config(font="Verdana 16 normal")
app.addLabel("step5", "When all three pictures are shown, a message will come up indicating the email was sent.", 5, 0, 2)
app.getLabelWidget("step5").config(font="Verdana 12 italic")
app.stopLabelFrame()

app.stopSubWindow()
#========= Stop Email Window ============#

# start the GUI
app.showSplash("MakerLab Photobooth by Darren", fill='white', stripe='black', fg='white', font=33)
app.go(startWindow="emailwin")
