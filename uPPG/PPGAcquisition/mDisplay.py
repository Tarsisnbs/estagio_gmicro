#!/usr/bin/env python3

## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## DEVELOPER: Cesar Abascal
## PROFESSORS: Cesar Augusto Prior and Cesar Rodrigues (Yeah. Its almost an overflow!)
## PROJECT: µPPG - Photoplethysmography waves acquisition
## ARCHIVE: Functions to manager OLED display
## DATE: 18/11/2018 - updated @ 15/03/2019
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


## LIBRARIES -----------------------------------------------------------------------------
import Adafruit_SSD1306
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont


## DEFINE AND CONFIGURE OLED DISPLAY ADDRESS ---------------------------------------------
# Define display reset pin
dispResetPIN = 4 # BCM mode 4 (RPi pin = 7)
# Configure GPIO to use BCM mode
GPIO.setmode(GPIO.BCM)
# Define SSD1306 OLED lib and I2C address
disp = Adafruit_SSD1306.SSD1306_128_64(rst=dispResetPIN, i2c_address=0x3C)

## START OLED DISPLAY --------------------------------------------------------------------
disp.begin()
width = disp.width
height = disp.height


class oledDisplay:

    # MAIN DISPLAY FUNCTIONS -------------------------------------------------------------

    def showDisplay(imgObj):
        disp.image(imgObj)
        disp.display()
    #end-def

    def clearDisplay():
        disp.clear()
        disp.display()
    #end-def


    # SCREENS FUNCTIONS -------------------------------------------------------------------

    def uPPGscreen():
        oledDisplay.clearDisplay()

        imageObj = Image.new('1', (width, height))

        draw = ImageDraw.Draw(imageObj)
        draw.rectangle((0,0,width-1,15), outline=1, fill=0)
        draw.rectangle((0,16,width-1,height-1), outline=1, fill=0)

        font = ImageFont.load_default()
        draw.text((54, 2),'µPPG',  font=font, fill=1)
        draw.text((4, 19),'Blood Pressure\nHeart Variability\nBlood Oxygenation',  font=font, fill=1)

        oledDisplay.showDisplay(imageObj)
    #end-def

    def acquiringScreen():
        oledDisplay.clearDisplay()

        imageObj = Image.open('PPGAcquisition/ppgImg.ppm').convert('1')

        draw = ImageDraw.Draw(imageObj)
        draw.rectangle((0,0,width-1,15), outline=1, fill=0)

        font = ImageFont.load_default()
        draw.text((15, 2),'Acquiring data...',  font=font, fill=1)

        oledDisplay.showDisplay(imageObj)
    #end-def

    def acquiredScreen(name, sps, samples):
        oledDisplay.clearDisplay()

        imageObj = Image.new('1', (width, height))

        draw = ImageDraw.Draw(imageObj)
        draw.rectangle((0,0,width-1,15), outline=1, fill=0)
        draw.rectangle((0,16,width-1,height-1), outline=1, fill=0)

        font = ImageFont.load_default()
        draw.text((25, 2),'Data acquired', font=font, fill=1)
        draw.text((4, 19),'Patient:' + name + '\nSamples:' + str(samples) + ' @ ' + str(sps) +'Hz\nPeriod:' + str('%.1f' % (samples/sps)) + ' seconds',  font=font, fill=1)

        oledDisplay.showDisplay(imageObj)
    #end-def

    def finishScreen():
        oledDisplay.clearDisplay()

        imageObj = Image.new('1', (width, height))

        draw = ImageDraw.Draw(imageObj)
        draw.rectangle((0,0,width-1,15), outline=1, fill=0)
        draw.rectangle((0,16,width-1,height-1), outline=1, fill=0)

        font = ImageFont.load_default()
        draw.text((36, 2),'Santa PPG', font=font, fill=1)
        draw.text((4, 19),'The system has been\nfinalized. Try again\nor turn off.',  font=font, fill=1)

        oledDisplay.showDisplay(imageObj)
    #end-def

#end-class
