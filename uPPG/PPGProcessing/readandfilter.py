#!/usr/bin/env python3

## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## DEVELOPER: Cesar Abascal
## PROFESSORS: Cesar Augusto Prior and Cesar Rodrigues (Yeah. Its almost an overflow!)
## PROJECT: µPPG - Photoplethysmography waves acquisition
## ARCHIVE: Read file and filter signals script to use on ppg processing
## DATE: 18/11/2018 - updated @ 15/03/2019
## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from scipy.signal import butter, lfilter, lfilter_zi
import numpy as np


# FUNCTIONS ---------------------------------------------------------------

# Get signals from file ---------------------------------------------------
def getAFESignal():

    sps = 200 # Samples per second
    REDsignal, IRsignal, synced = [], [], []
    signalBase = 1.045

    patient = str(input("Patient name: "))
    fileDir = "ppg-data/raw-ppg/" + patient + "/uppg_signals.csv"

    samples = 0
    with open(fileDir) as dataFile:
        next(dataFile)
        for line in dataFile:
            aux = line.split(',')
            REDsignal.append(signalBase - float(aux[0]))
            IRsignal.append(signalBase - float(aux[1]))
            synced.append(float(aux[2]))
            samples +=1
        #end-for
    #end-with

    dataFile.close()

    return REDsignal, IRsignal, synced, samples, sps, patient
#end def

# Butterworth filter ------------------------------------------------------
def butter_bandpass(lowcut, highcut, sRate, order=5):
    nyq = 0.5 * sRate
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a
#end def

#def butter_bandpass_filter(data, lowcut, highcut, sRate, order=5):
#    b, a = butter_bandpass(lowcut, highcut, sRate, order=order)
#    y = lfilter(b, a, data)
#    return y
##end def

# This function will apply the filter considering the initial transient.
def butter_bandpass_filter_zi(data, lowcut, highcut, sRate, order=5):
    b, a = butter_bandpass(lowcut, highcut, sRate, order=order)
    zi = lfilter_zi(b, a)
    y,zo = lfilter(b, a, data, zi=zi*data[0])
    return y
#end def


# GET AND FILTER ----------------------------------------------------------

# Get data
RED, IR, syncArray, nSamples, sRate, pName = getAFESignal()

# Apply bandpass filter into raw signals
lowcut = 0.4
highcut = 8
order = 3
REDf = butter_bandpass_filter_zi(RED, lowcut, highcut, sRate, order)
IRf = butter_bandpass_filter_zi(IR, lowcut, highcut, sRate, order)
print('sinal orig: ' + str(RED) + 'sinal filt' + str(REDf))
# Calculate x axis and define y axis
x = np.linspace(0, nSamples/sRate, nSamples, endpoint=True)
y = IR
yf = IRf