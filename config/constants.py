__author__ = 'Arjun Prasad Namdeo'

import platform
import os
import sys

# for Ubuntu, DJV Static binary not working.. Need to install it from http://djv.sourceforge.net/

packagePath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(packagePath)

os_family = "Mac"

if platform.system() in ["Linux", "Windows"]:
    os_family = str(platform.system())

# List all the Valid Inputs from User

valid_VideoCodec = ['libx264', 'prores', 'dnxhd', 'photojpeg', ]
valid_imgFileTypes = ['.dpx', '.exr', '.png', '.jpg', '.jpeg', '.tga', '.tif', '.tiff']
valid_movFileTypes = ['.mov', '.mp4', '.avi']
valid_fontsExt = [".ttf"]
valid_fontsName = ['lucida', 'agency', 'arial', 'calibri', 'courier', 'verdana']

# Default Arguments for Transcode Process

videoCodec = valid_VideoCodec[0]
fps = 24.0
textSize = 50
textFont = valid_fontsName[0]
textColor = (255, 255, 255)
textPos = (100, 100)
textOpacity = 100
