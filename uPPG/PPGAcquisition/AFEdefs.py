#!/usr/bin/env python3

## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## DEVELOPER: Cesar Abascal
## PROFESSORS: Cesar Augusto Prior and Cesar Rodrigues (Yeah. Its almost an overflow!)
## PROJECT: µPPG - Photoplethysmography waves acquisition
## ARCHIVE: Registers and definitions map.
## DATE: 18/11/2018 - updated @ 15/03/2019
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


## DEFINITIONS ---------------------------------------------------------------------------------------------------------------
# Interface Communication (Use all in BCM)
stePIN = 25 # RPi pin 22 (BCM = 25)
adcrdyPIN = 8 # RPi pin 24 (BCM = 8)
diagendPIN = 22 #RPi pin 15 (BCM = 22)
pdalmPIN = 23 # RPi pin 16 (BCM = 23)
ledalmPIN = 24 # RPI pin 18 (BCM = 24)
resetPIN = 17 # RPI pin 11 (BCM = 17)
pdnPIN = 27 # RPI pin 13 (BCM = 27)
# MISO = RPi pin 21 ; MOSI = RPi pin 19 ; SCLK = RPi pin 23

# IO Interface (Use all in BCM)
syncbtnPIN = 19 # Prototype0: syncbtnPIN=19 and Prototype1: syncbtnPIN=14
#shutdownbtnPIN = 13 # Prototype0: shutdownbtnPIN=13 and Prototype1: shutdownbtnPIN=18 / Used in launcher script
thirdbtnPIN = 15 # Prototype0: doesn't exist and Prototype1: thirdbtnPIN=15
outputonePIN = 26 # Prototype0: outputonePIN=26 and Prototype1: outputonePIN=12
#outputtwoPIN = ? # Prototype0: outputtwoPIN=? and Prototype1: outputtwoPIN=16
#outputthreePIN = ? # Prototype0: outputthreePIN=? and Prototype1: outputthreePIN=20
#outputfourPIN = ? # Prototype0: outputfourPIN=? and Prototype1: outputfourPIN=21

## VARIABLES ----------------------------------------------------------------------------------------------------------------
digitalToVolt = 1.2/2097152 # VRef = 1.2V
sps = 200 # Samples per Second

## AFE449 REGISTERS MAP -----------------------------------------------------------------------------------------------------
# Write Registers:
CONTROL0 = 0x00 # This register is used for AFE software and count timer reset, diagnostics enable, and SPI read functions.
# Read and Write Registers:
LED2STC = 0x01 # This register sets the start timing value for the LED2 signal sample.
LED2ENDC = 0x02 # This register sets the end timing value for the LED2 signal sample.
LED2LEDSTC = 0x03 # This register sets the start timing value for when the LED2 signal turns on.
LED2LEDENDC = 0x04 # This register sets the end timing value for when the LED2 signal turns off.
ALED2STC = 0x05 # This register sets the start timing value for the ambient LED2 signal sample.
ALED2ENDC = 0x06 # This register sets the end timing value for the ambient LED2 signal sample.
LED1STC = 0x07 # This register sets the start timing value for the LED1 signal sample.
LED1ENDC = 0x08 # This register sets the end timing value for the LED1 signal sample.
LED1LEDSTC = 0x09 # This register sets the start timing value for when the LED1 signal turns on.
LED1LEDENDC = 0x0A # This register sets the end timing value for when the LED1 signal turns off.
ALED1STC = 0x0B # This register sets the start timing value for the ambient LED1 signal sample.
ALED1ENDC = 0x0C # This register sets the end timing value for the ambient LED1 signal sample.
LED2CONVST = 0x0D # This register sets the start timing value for the LED2 conversion.
LED2CONVEND = 0x0E # This register sets the end timing value for the LED2 conversion.
ALED2CONVST = 0x0F # This register sets the start timing value for the ambient LED2 conversion.
ALED2CONVEND = 0x10 # This register sets the end timing value for the ambient LED2 conversion.
LED1CONVST = 0x11 # This register sets the start timing value for the LED1 conversion.
LED1CONVEND = 0x12 # This register sets the end timing value for the LED1 conversion.
ALED1CONVST = 0x13 # This register sets the start timing value for the ambient LED1 conversion.
ALED1CONVEND = 0x14 # This register sets the end timing value for the ambient LED1 conversion.
ADCRSTSTCT0 = 0x15 # This register sets the start position of the ADC0 reset conversion signal.
ADCRSTENDCT0 = 0x16 # This register sets the end position of the ADC0 reset conversion signal.
ADCRSTSTCT1 = 0x17 # This register sets the start position of the ADC1 reset conversion signal.
ADCRSTENDCT1 = 0x18 # This register sets the end position of the ADC1 reset conversion signal.
ADCRSTSTCT2 = 0x19 # This register sets the start position of the ADC2 reset conversion signal.
ADCRSTENDCT2 = 0x1A # This register sets the end position of the ADC2 reset conversion signal.
ADCRSTSTCT3 = 0x1B # This register sets the start position of the ADC3 reset conversion signal.
ADCRSTENDCT3 = 0x1C # This register sets the end position of the ADC3 reset conversion signal.
PRPCOUNT = 0x1D # This register sets the device pulse repetition period count.
CONTROL1 = 0x1E # This register configures the clock alarm pin, timer, and number of averages.
SPARE1 = 0x1F # This register is a spare register and is reserved for future use. [IT MUST BE 0]
TIAGAIN = 0x20 # This register sets the device transimpedance amplifier gain mode and feedback resistor and capacitor values.
TIA_AMB_GAIN = 0x21 # This register configures the ambient light cancellation amplifier gain, cancellation current, and filter corner frequency.
LEDCNTRL = 0x22 # This register sets the LED current range and the LED1 and LED2 drive current.
CONTROL2 = 0x23 # This register controls the LED transmitter, crystal, and the AFE, transmitter, and receiver power modes.
SPARE2 = 0x24 # This register is a spare register and is reserved for future use. [IT MUST BE 0]
SPARE3 = 0x25 # This register is a spare register and is reserved for future use. [IT MUST BE 0]
SPARE4 = 0x26 # This register is a spare register and is reserved for future use. [IT MUST BE 0]
# Read Registers:
RESERVED1 = 0x27 # This register is reserved for factory use. Readback values vary between devices.
RESERVED2 = 0x28 # This register is reserved for factory use. Readback values vary between devices.
ALARM = 0x29 # This register controls the Alarm pin functionality.
LED2VAL = 0x2A # This register contains the digital value of the latest LED2 sample converted by the ADC.
                # The ADC_RDY signal goes high each time that the contents of this register are updated.
                # The host processor must readout this register before the next sample is converted by the AFE.
ALED2VAL = 0x2B # This register contains the digital value of the latest LED2 ambient sample converted by the ADC.
                 # The ADC_RDY signal goes high each time that the contents of this register are updated.
                 # The host processor must readout this register before the next sample is converted by the AFE.
LED1VAL = 0x2C # This register contains the digital value of the latest LED1 sample converted by the ADC.
                # The ADC_RDY signal goes high each time that the contents of this register are updated.
                # The host processor must readout this register before the next sample is converted by the AFE.
ALED1VAL = 0x2D # This register contains the digital value of the latest LED1 ambient sample converted by the ADC.
                 # The ADC_RDY signal goes high each time that the contents of this register are updated.
                 # The host processor must readout this register before the next sample is converted by the AFE.
LED2ALED2VAL = 0x2E # This register contains the digital value of the LED2 sample after the LED2 ambient is subtracted.
                     # The host processor must readout this register before the next sample is converted by the AFE.
LED1ALED1VAL = 0x2F # This register contains the digital value of the LED1 sample after the LED1 ambient is subtracted.
                     # The host processor must readout this register before the next sample is converted by the AFE.
DIAG = 0x30 # This register is read only. This register contains the status of all diagnostic flags at the end of the diagnostics sequence.
             # The end of the diagnostics sequence is indicated by the signal going high on DIAG_END pin.
             