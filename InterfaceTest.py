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
from PhotoBooth import PhotoBooth

booth = PhotoBooth(eml,true, false, false)

# handle button events
def press(button):
    if button == "Reset":
        app.setFocus("Email:")
        app.setEntry("Email:", "", callFunction=False)
        #app.stop()
    else:
        eml = app.getEntry("Email:")
        if booth.validateEmail(eml) is False:
            print("email is invalid")

  
# create a GUI variable called app
app = gui("Login Window", "640x480")
app.setBg("grey")
app.setFont(18)

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "MakerLab - Photo Booth")
app.setLabelBg("title", "black")
app.setLabelFg("title", "white")

app.addLabelEntry("Email:")

# link the buttons to the function called press
app.addButtons(["Confirm Email","Take Picture", "Reset"], press)

app.setFocus("Email:")

# start the GUI
app.go()
