
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## DEVELOPER: Cesar Abascal
## PROFESSORS: Cesar Augusto Prior and Cesar Rodrigues (Yeah. Its almost an overflow!)
## PROJECT: µPPG - Photoplethysmography waves acquisition
## ARCHIVE: Simple loop infinite acquisition main page
## DATE: 18/11/2018 - updated @ 15/03/2019
## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


## LIBRARIES ----------------------------------------------------------------------------
import os
from PPGAcquisition.AFEcore import functions as f
import socket
from threading import Thread

buffer1 = []
buffer2 = []


if __name__ == '__main__':
    try:
        # Show uPPG screen on display and info on terminal
        f.showInitInfos()

        # Get pacient name and create txt file to save data
        f.patientN = "testejj" #str(input("Patient name: "))
        path = "ppg-data/raw-ppg/" + f.patientN
        if(not os.path.exists(path)):
            os.makedirs(path)
        f.dataFile = open(path+"/uppg_signals.csv", "w+")
        f.dataFile.write("REDsignal,IRsignal,synced\n")

        # Open SPI connection
        f.openSPIConnection()

        # Initialize AFE4490 CI
        f.AFEinit()

        # Show acquiring screen on display and info on terminal
        f.showAcqInfos()

        # Set Interruption Service Routine
        f.setISR()
        #chamada da thread TCP
        print("...")

        # Start acquisition infinite loop until ctrl-c be pressed
        print("fim main...")
        f.mainLoop()

    #end-try

    except KeyboardInterrupt:
        # Stop and finish acquisition when crtl-c where pressed
        f.finish()
    #end-except
