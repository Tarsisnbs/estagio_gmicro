#!/usr/bin/env python3

## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## DEVELOPER: Cesar Abascal
## PROFESSORS: Cesar Augusto Prior and Cesar Rodrigues (Yeah. Its almost an overflow!)
## PROJECT: µPPG - Photoplethysmography waves acquisition
## ARCHIVE: Plot ppg signal script
## DATE: 18/11/2018 - updated @ 15/03/2019
## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import matplotlib.pyplot as plt
from PPGProcessing.readandfilter import *
from PPGProcessing.mathprocessing import *


# GRAPHICAL FUNCTIONS -----------------------------------------------------

# Plot PPG raw signals
def plotRawSignals():
    plt.figure('Noisy and filtered PPG signals from RED and IR', figsize=(14,6)) # 20,10

    plt.subplot(2,2,1)
    plt.title("Raw RED signal")
    plt.ylabel("amplitude (v)")
    plt.plot(x, RED, "red")
    plt.grid()

    plt.subplot(2,2,2)
    plt.title("Raw IR signal")
    plt.plot(x, IR, "orange")
    plt.grid()

    plt.subplot(2,1,2)
    plt.title("Filtered Signals")
    plt.xlabel("time (s)")
    plt.ylabel("amplitude (v)")
    plt.plot(x, REDf, "red", label="RED Signal")
    plt.plot(x, IRf, "orange", label="IR Signal")
    plt.legend(loc="best")
    plt.grid()

    plt.show()
#end-def

# Plot auxiliary 1 - Plot some states of the method
def plotNoisyFilteredClippedSquared():
    plt.figure('Noisy, Filtered, Clipped and Squared PPG Signal - '+pName, figsize=(14,6))

    plt.subplot(2,2,1)
    plt.title("Noisy Signal")
    plt.ylabel("amplitude (v)")
    plt.plot(x, y)
    plt.grid()

    plt.subplot(2,2,2)
    plt.title("Filtered Signal")
    plt.plot(x, yf)
    plt.grid()

    plt.subplot(2,2,3)
    plt.title("Filtered and Clipped Signal")
    plt.xlabel("time (s)")
    plt.ylabel("amplitude (v)")
    plt.plot(x, yfc)
    plt.grid()

    plt.subplot(2,2,4)
    plt.title("Filtered, Clipped and Squared Signal")
    plt.xlabel("time (s)")
    plt.plot(x, yfcs)
    plt.grid()

    plt.show()
#end-def

# Plot auxiliary 2 - Plot some states of the method
def plotMApeakMAbeatBlocksResult():

    systolicArea, peakx, peaky = getSystolicAreaPeaks()

    plt.figure('MApeak, MAbeat, Blocks of Interest and Result - '+pName, figsize=(14,6))

    plt.subplot(2,2,1)
    plt.title("MApeak from squared signal")
    plt.ylabel("amplitude (v)")
    plt.plot(x, MApeak)
    plt.grid()

    plt.subplot(2,2,2)
    plt.title("MAbeat from squared signal")
    plt.plot(x, MAbeat)
    plt.grid()

    plt.subplot(2,2,3)
    plt.title("systolicArea")
    plt.xlabel("time (s)")
    plt.ylabel("amplitude (v)")
    plt.plot(x, systolicArea)
    plt.grid()

    plt.subplot(2,2,4)
    plt.title("PPG signal filtered, Systolic wave and Systolic peak")
    plt.xlabel("time (s)")
    plt.plot(x, yf, "purple")
    plt.plot(x, systolicArea, "orange")
    plt.scatter(peakx, peaky)
    plt.grid()

    plt.show()
#end-def

# Plot PPG signal filtered and classified
def plotHeartbeatIntervals():
    systolicArea, peakx, peaky = getSystolicAreaPeaks()

    plt.figure('PPG Signal Filtered, Systolic Wave and Peak - '+pName, figsize=(14,6))
    plt.xlabel("time (s)")
    plt.ylabel("amplitude (v)")
    plt.plot(x, yf, "purple", label="PPG signal filtered")
    plt.plot(x, systolicArea, "orange", label="Systolic wave")
    plt.scatter(peakx, peaky, label="Systolic peak")
    plt.legend(loc="best")
    plt.grid()
    plt.show()
#end-def
