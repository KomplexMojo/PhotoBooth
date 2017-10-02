# Copyright (c) 2014 Adafruit Industries
# Initial Author: Tony DiCola
# Edited: Darren Ditto (Aug, 2016) - Extensively rewritten, command keys, etc
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

#
#  Darren's ToDo
#
# Add a default sound for missing file.
# Add a default sound for instrument changing.
# Mess with the lights!
#

import sys
import time
import pygame
import copy
import logging
import os
import Adafruit_MPR121.MPR121 as MPR121

# Set up detailed logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# logging to file in current dir
fh = logging.FileHandler('log_filename.txt')
fh.setLevel(logging.CRITICAL)
fh.setFormatter(formatter)
logger.addHandler(fh)

# logging to interface
ch = logging.StreamHandler()
ch.setLevel(logging.CRITICAL)
ch.setFormatter(formatter)
logger.addHandler(ch)

# Thanks to Scott Garner & BeetBox!
# https://github.com/scottgarner/BeetBox/

logger.info('Adafruit MPR121 Capacitive Touch Audio Player Test - Now with added instrumpent switching...')

# Create MPR121 instance.
cap = MPR121.MPR121()

# Initialize communication with MPR121 using default I2C bus of device, and
# default I2C address (0x5A).  On BeagleBone Black will default to I2C bus 0.
if not cap.begin():
    logger.critical('Error initializing MPR121.  Check your wiring! Exiting Code')
    sys.exit(1)

logger.info('Initializing Mixer')
pygame.mixer.pre_init(44100, -16, 12, 512)
pygame.init()

# path to the example folder
root_path = '/home/pi/'
sound_path = root_path +'sounds/'
file_extenstion = '.wav'

# instruments, please note these have to match the folder names
INSTRUMENTS = {
    0: 'piano', 
    1: 'pluck', 
    2: 'pretty_bell', 
    3: 'zawa'
}

# chords per instrument, please note that these have to match the file names
CHORDS = {
    0: 'c_major',
    1: 'c_minor',
    2: 'd_major',
    3: 'd_minor',
    4: 'e_major',
    5: 'e_minor',
    6: 'f_major',
    7: 'f_minor'
}

# pin number mapped to instrument number
# for convenience I decided that pins 8-11 inclusive would be the instrument control pins
INSTRUMENT_PINS = {
    8:  0,
    9:  1,
    10: 2,
    11: 3
}

logger.info('Creating matrix with {0} columns and {1} rows'.format(len(CHORDS),len(INSTRUMENTS)))

# create a multidimensional array of sounds, per instrument, per chord (currently 4 rows of 8 for 32 in total)
sounds = [ [ 0 for i in range(len(CHORDS))] for j in range(len(INSTRUMENTS)) ]

# set the default instrument sound
instrument_volume = 1

# 0 sets the current instrument to the default instrument (piano) so if buttons are pressed, at least the piano plays
current_instrument = 0

# populate the 2 dimensional list of sounds based on instrument type, then chord
for instrument_num, instrument_name in INSTRUMENTS.items():
    for chord_num, chord_name in CHORDS.items():
        full_path = sound_path + instrument_name + '/' + chord_name + file_extenstion

        if (os.path.isfile(full_path)):		
            logger.info('Creating and adding sound: ' + full_path)
            logger.info('    Row: {0}'.format(instrument_num))
            logger.info('    Col: {0}'.format(chord_num))
            sounds[instrument_num][chord_num] = pygame.mixer.Sound(full_path)
            sounds[instrument_num][chord_num].set_volume(instrument_volume)
        else:
            logger.critical('Path or file error: ' + full_path + ' does not exist.')
            sys.exit(1)
		
logger.debug(sounds)

# Main loop to print a message every time a pin is touched.
logger.info('Entering Main Loop - Press Ctrl-C to quit.')
logger.info('Pins 8 through 12 switch instruments.')

last_touched = cap.touched()
while True:
    current_touched = cap.touched()
    logger.debug('current touched = {0}'.format(current_touched))
    # Check each pin's last and current state to see if it was pressed or released.
    for i in range(12):		
        # Each pin is represented by a bit in the touched value.  A value of 1
        # means the pin is being touched, and 0 means it is not being touched.
        pin_bit = 1 << i
        
	if current_touched & pin_bit and not last_touched & pin_bit:            
            # First check if transitioned from not touched to touched.
            logger.debug('{0} is current touched'.format(current_touched))
            logger.debug('{0} is last touched'.format(last_touched))         			
            # if the pin touched is greater than 7 (8 through 11) use it as a command pin
            if i > 7:
                logger.debug('{0} pin'.format(i))         			            
                current_instrument =  INSTRUMENT_PINS[i]
                logger.debug('{0} current instrument index'.format(current_instrument))         			            
                logger.info('Switching instrument to: ' + INSTRUMENTS[current_instrument].capitalize())
                # play the sound based on the command pin
            else:
                logger.info('Playing instrument:' + INSTRUMENTS[current_instrument].capitalize())				
                logger.info('**Playing chord:' + CHORDS[i].upper())
                sounds[current_instrument][i].play()

        if not current_touched & pin_bit and last_touched & pin_bit:
            logger.debug('{0} is pin released!'.format(i))

    # Update last state and wait a short period before repeating.
    last_touched = current_touched
    time.sleep(0.1)
