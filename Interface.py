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
import uuid
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from PIL import Image
import string


winsize="800x470"
btnPaddingX=50
btnPaddingY=50
topPad=0
sidePad=5
picSmall=""
picLarge=""
largeImageWidth=1080
largeImageHeight=1920

isValid = False
emailFolder = ""
match = None
folderPath = ""
fileName = ""
addressToVerify = ""
files = []
sendingEmailAddress="2rgmenagerie@gmail.com"
emailSubject="TwoRiversGallery Menagerie 2017 - Banished to the Bayou"
emailHTMLBody= """\
<html>
  <head></head>
  <body>
    <p>Thank you for attending the TwoRiversGallery Menagerie 2017 - Banished to the Bayou</p>
  </body>
</html>
"""

def verifyemail(button):
    global isValid
    global emailFolder
    global match
    global folderPath
    global fileName
    global addressToVerify

    addressToVerify = app.getEntry("Email Checker")
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
    addressToVerify = match.group(0)

    if match is None:
        app.setEntryInvalid("Email Checker")
    else:
        app.setEntryValid("Email Checker")
        fileName = re.sub('[^a-zA-Z0-9]', '_', match.group(0))
        folderPath = "/home/pi/Pictures/" + re.sub('[^a-zA-Z0-9]', '_', match.group(0)) + "_" + str(uuid.uuid4())[:4] + "/"
        app.hideSubWindow("emailwin")
        app.showSubWindow("Picture Viewer")


def takepic(btn):
    global files

    largePicFile = str(uuid.uuid4())[:4]
    smallPicFile = str(uuid.uuid4())[:4]
    sequence = ""

    if btn == "Picture One":
        sequence = "1"
        camera(largePicFile + sequence + ".png")
        resize(largePicFile + sequence + ".png", smallPicFile + sequence + ".gif")
        app.hideButton("Picture One")
        app.reloadImage("img1", folderPath + smallPicFile + sequence + ".gif")
        app.showImage("img1")
    elif btn == "Picture Two":
        sequence = "2"
        camera(largePicFile + sequence + ".png")
        resize(largePicFile + sequence + ".png", smallPicFile + sequence + ".gif")
        app.hideButton("Picture Two")
        app.reloadImage("img2", folderPath + smallPicFile + sequence + ".gif")
        app.showImage("img2")
    elif btn == "Picture Three":
        sequence = "3"
        camera(largePicFile + sequence + ".png")
        resize(largePicFile + sequence + ".png", smallPicFile + sequence + ".gif")
        app.hideButton("Picture Three")
        app.reloadImage("img3", folderPath + smallPicFile + sequence + ".gif")
        app.showImage("img3")
        app.showSubWindow("resetwin")
    else:
        print('end')


def resetwins(btn):
    global files

    sendmail(sendingEmailAddress, addressToVerify, emailSubject, emailHTMLBody, files)
    app.showSubWindow("emailwin")
    app.hideSubWindow("Picture Viewer")
    app.clearEntry("Email Checker", callFunction=False, setFocus=True)
    app.hideImage("img1")
    app.hideImage("img2")
    app.hideImage("img3")
    app.showButton("Picture One")
    app.showButton("Picture Two")
    app.showButton("Picture Three")
    files[:] = []


def resize(original, small):
    image = Image.open(folderPath + original)
    image.thumbnail((int(largeImageWidth*.2), int(largeImageHeight*2)), Image.ANTIALIAS)
    image.save(folderPath + small, 'GIF', quality=50)


def camera(imageName):
    global files

    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    with PiCamera() as camera:
        camera.resolution = (largeImageWidth, largeImageHeight)
        camera.image_effect = 'none'
        camera.start_preview()
        sleep(3)
        camera.capture(folderPath + imageName)
        files.append(folderPath + imageName)
        camera.stop_preview()


def sendmail(send_from, send_to, subject, text, files=None, server="smtp.gmail.com"):

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(emailHTMLBody, 'html'))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )

         # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    smtp = smtplib.SMTP(server, 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login("2rgmenagerie@gmail.com", "makerlab1")
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

# create a GUI variable called app
app = gui("MakerLab Photobooth by Darren", "fullscreen")
app.setBg("white")
#app.setFont(12)

#========= Start Picture Window ============#
app.startSubWindow("Picture Viewer", modal=False)
app.setGeometry(winsize)
app.setBg("white")

app.setSticky("ns")
app.startLabelFrame("Picture One", 0, 0)
app.setInPadding([btnPaddingX, btnPaddingY])
app.setPadding([sidePad, topPad])
app.setBg("white")
app.addIconButton("Picture One", takepic, "md-camera-photo", 0, 0)
app.addImage("img1", "/home/pi/PhotoBooth/SourceImages/default_small.gif", 0, 0)
app.hideImage("img1")
app.stopLabelFrame()

app.setSticky("ns")
app.startLabelFrame("Picture Two", 0, 1)
app.setInPadding([btnPaddingX, btnPaddingY])
app.setPadding([sidePad, topPad])
app.setBg("white")
app.addIconButton("Picture Two", takepic, "md-camera-photo", 0, 1)
app.addImage("img2", "/home/pi/PhotoBooth/SourceImages/default_small.gif", 0, 1)
app.hideImage("img2")
app.stopLabelFrame()

app.setSticky("ns")
app.startLabelFrame("Picture Three", 0, 2)
app.setInPadding([btnPaddingX, btnPaddingY])
app.setPadding([sidePad, topPad])
app.setBg("white")
app.addIconButton("Picture Three", takepic, "md-camera-photo", 0, 2)
app.addImage("img3", "/home/pi/PhotoBooth/SourceImages/default_small.gif", 0, 2)
app.hideImage("img3")
app.stopLabelFrame()
app.stopSubWindow()
#========= Stop Picture Window ============#

#========= Start Email Window ============#
app.startSubWindow("emailwin", "Enter Email Address", modal=True)
app.setGeometry(winsize)
app.setBg("white")
app.setSticky("nsew")

app.startLabelFrame("Enter Your Email Address to Receive Pictures", 0, 0)
app.setBg("white")

app.addValidationEntry("Email Checker", 0, 1)
app.getEntryWidget("Email Checker").config(font="Verdana 12 normal")
app.setEntryDefault("Email Checker", "Enter Email Address")
app.setEntryMaxLength("Email Checker", 100)
app.setEntryWidth("Email Checker", 50)

app.addIconButton("emailbtn", verifyemail, "check", 0, 2)
app.setButtonPadding("emailbtn", [10, 10])

app.addLabel("step1", "Step 1 - Use the attached keyboard to enter your email address.", 1, 0, 2)
app.getLabelWidget("step1").config(font="Verdana 16 normal")
app.addLabel("step2", "Step 2 - Press the email button to confirm email address.", 2, 0, 2)
app.getLabelWidget("step2").config(font="Verdana 16 normal")
app.addLabel("step3", "Step 3 - In the next screen press a camera button (left to right).", 3, 0, 2)
app.getLabelWidget("step3").config(font="Verdana 16 normal")
app.addLabel("step4", "Step 4 - Pose for 3 seconds.", 4, 0, 2)
app.getLabelWidget("step4").config(font="Verdana 16 normal")
app.addLabel("step5", "When all three pictures are shown, press the refresh button to send the picture.", 5, 0, 2)
app.getLabelWidget("step5").config(font="Verdana 12 italic")
app.stopLabelFrame()

app.stopSubWindow()
#========= Stop Email Window ============#

app.startSubWindow("resetwin", "Reset Window", modal=True)
app.setGeometry("250x250")
app.setBg("white")

app.startLabelFrame("Reset Window", 0, 0)

app.setInPadding([btnPaddingX, btnPaddingY])
app.setPadding([sidePad, topPad])
app.setSticky("nsew")
app.addIconButton("Reload Interface", resetwins, "mail", 0, 0)
app.stopLabelFrame()

app.stopSubWindow()

# start the GUI
app.showSplash("MakerLab Photobooth by Darren", fill='white', stripe='black', fg='white', font=33)
app.go(startWindow="emailwin")
