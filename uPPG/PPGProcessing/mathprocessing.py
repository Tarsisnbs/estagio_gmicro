#!/usr/bin/env python3

## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## DEVELOPER: Cesar Abascal
## PROFESSORS: Cesar Augusto Prior and Cesar Rodrigues (Yeah. Its almost an overflow!)
## PROJECT: µPPG - Photoplethysmography waves acquisition
## ARCHIVE: Math script for ppg processing
## DATE: 18/11/2018 - updated @ 15/03/2019
## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from PPGProcessing.readandfilter import *


# MATH FUNCTIONS ----------------------------------------------------------

# Cutting negative values
def cuttingNegatives(signal, ssize):
    positives = np.zeros(ssize)
    
    for i in np.arange(ssize):
        if(signal[i] > 0):
            positives[i] = signal[i]
    #end-for

    return positives
#end-def

# Moving average
def movingAverage(signal, ssize, window):
    
    maSum = 0
    mAver = np.zeros(ssize)
    k = int((window-1)/2)

    for i in np.arange(k, ssize-k):
        for j in np.arange(i-k, i+k):
            maSum = maSum + signal[j]
        #end-for
        mAver[i] = maSum/window
        maSum = 0
    #end-for
    
    return mAver
#end-def

# Statistical average
def average(signal, ssize):
    
    aSum = 0
    for i in np.arange(ssize):
        aSum = aSum + signal[i]
    
    return aSum/ssize
#end-def


# SYSTOLIC PEAK METHOD ----------------------------------------------------

# Clipping signal
yfc = cuttingNegatives(yf, nSamples)

# Squaring signal
yfcs = np.power(yfc,2)

# Emphasise the systolic peak area
# W1 = 111ms (28pts @ 250Hz) correspond to the systolic peak duration
MApeak = movingAverage(yfcs, nSamples, 28)

# Emphasise the beat area
# W2 = 667ms (167pts @ 250Hz) correspond to the heartbeat duration
MAbeat = movingAverage(yfcs, nSamples, 167)

# Statiscal mean of the signal
yfcsa = average(yfcs, nSamples)

# Alpha will be the multiplication of yfcsa by beta (0.02)
alpha = 0.02 * yfcsa

# Threshold1 will be the sum of each point in MAbeat by alpha
THR1 = MAbeat + alpha # array

# Threshold2 will be the same as W1
THR2 = 28 # scalar

def getSystolicAreaPeaks():

    # Emphasizing systolic area (block of interest) and finding systolic peaks
    peakx, peaky = [], []
    xpeakmax, ypeakmax, ypeakmaxMAX = 0, 0, 0
    blockWidth = 0
    systolicArea = np.zeros(nSamples)

    for i in np.arange(nSamples):
        if(MApeak[i] > THR1[i]):
            blockWidth += 1
            systolicArea[i] = 1

            if(yf[i] > ypeakmax):
                xpeakmax = x[i]
                ypeakmax = yf[i]
                if(ypeakmax > ypeakmaxMAX):
                    ypeakmaxMAX = ypeakmax
            #end-if
        elif(blockWidth>=THR2):
            blockWidth = 0
            peakx.append(float(xpeakmax))
            peaky.append(float(ypeakmax))
            xpeakmax = ypeakmax = 0
        #end-if
    #end-for

    # Set systolic area wave amplitude with the maximum ypeak founded.
    systolicArea = systolicArea * ypeakmaxMAX

    return systolicArea, peakx, peaky
#end-def

def saveHeartbeatIntervals():

    directory = "ppg-data/heartbeatIntervals/"
    hbiFile = open(directory+pName+"-heartbeat_interval.txt", "w")
    xpeakmax, ypeakmax, ypeakmaxMAX, last_xpeakmax = 0, 0, 0, 0
    blockWidth = 0

    for i in np.arange(nSamples):
        if(MApeak[i] > THR1[i]):
            blockWidth += 1
        
            if(yf[i] > ypeakmax):
                xpeakmax = x[i]
                ypeakmax = yf[i]
            #end-if

        elif(blockWidth>=THR2):
            blockWidth = 0
            
            xpeakmax_dif = int((xpeakmax - last_xpeakmax) * 1000)
            if(last_xpeakmax > 0):
                #print(int(xpeakmax_dif))            
                hbiFile.write(str(xpeakmax_dif) + "\n")
            #end-if
            last_xpeakmax = xpeakmax
            xpeakmax = ypeakmax = 0
        #end-if
    #end-for

    hbiFile.close()
#end-def


# CALCULATE SPO2 METHOD ---------------------------------------------------
'''
def calculateSPO(REDsignal, IRsignal, samples, i0, i1):

    REDsignalSum, IRsignalSum = 0, 0
    REDsignalDC = np.zeros(samples)
    IRsignalDC = np.zeros(samples)

    print("---",i0)
    print("---",i1)
    j = 0
    for i in np.arange(i0, i1):
        REDsignalSum = REDsignalSum + REDsignal[i]
        IRsignalSum = IRsignalSum + IRsignal[i]

        REDsignalDC[i] = REDsignalSum/i
        IRsignalDC[i] = IRsignalSum/i
        
        REDsignalDif = REDsignal[i] - REDsignalDC[i]
        IRsignalDif = IRsignal[i] - IRsignalDC[i]

        REDsignalPow = np.power(REDsignalDif, 2)
        IRsignalPow = np.power(IRsignalDif, 2)

        REDsignalAC = (np.sqrt(REDsignalPow))/i
        IRsignalAC = (np.sqrt(IRsignalPow))/i

        ratio = (REDsignalAC/REDsignalDC[i])/(IRsignalAC/IRsignalDC[i])

        SPO = 100 - ratio
        #print(i)
        j += 1
        print(j)

    return SPO
#end def

def getSPO(GAPsec):

    if((nSamples < 250) or (GAPsec < 0)):
        print("\nLess than 1 second of signal, or gap value isnt positive.\n")
        return [0]
    else:
        nSplits = round( nSamples/(sRate*GAPsec) )
        divPeriod = int(nSamples/nSplits)
        print(divPeriod)
        spo_array = np.zeros(nSplits)
        for n in np.arange(nSplits):
            #print(n*divPeriod, (n+1)*divPeriod)
            spo_array[n] = round( calculateSPO( REDf, IRf, divPeriod+1, n*divPeriod, ((n+1)*divPeriod-1) ) )
        #end-for
    #end-if
    return spo_array
#end-def
'''

def calculateSPO(REDsignal, IRsignal, s0, s1):

    samples = s1-s0
    REDsignalSum, IRsignalSum = 0, 0
    REDsignalDC = np.zeros(samples)
    IRsignalDC = np.zeros(samples)

    print("i0:",s0)
    print("i1:",s1)
    print("size:",samples)

    for i in np.arange(samples):
        j = i+s0
        print("index:",i)
        print("signal:", j)
        
        
        REDsignalSum = REDsignalSum + REDsignal[j]
        IRsignalSum = IRsignalSum + IRsignal[j]

        REDsignalDC[i] = REDsignalSum/i
        IRsignalDC[i] = IRsignalSum/i
        
        REDsignalDif = REDsignal[j] - REDsignalDC[i]
        IRsignalDif = IRsignal[j] - IRsignalDC[i]

        REDsignalPow = np.power(REDsignalDif, 2)
        IRsignalPow = np.power(IRsignalDif, 2)

        REDsignalAC = (np.sqrt(REDsignalPow))/i
        IRsignalAC = (np.sqrt(IRsignalPow))/i

        ratio = (REDsignalAC/REDsignalDC[i])/(IRsignalAC/IRsignalDC[i])

        SPO = 100 - ratio

    return SPO
    
#end def

def getSPO(GAPsec):

    if((nSamples < 200) or (GAPsec < 0)):
        print("\nLess than 1 second of signal, or gap value isnt positive.\n")
        return [0]
    else:
        ndivs = round(nSamples/sRate)
        #if(ndivs%GAPsec or GAPsec>ndivs):
        #    print("\nGap value need to be exact divided and less than the number of signal seconds.\n")
        #    return [0]
        #else:
        ndivs = round(nSamples/(sRate*GAPsec))
        if ndivs != 0:
            sparts = round(nSamples/ndivs)
        #end-if

        print('Samples:', nSamples)
        print('Size Parts:', sparts)
        print('Divisions:', ndivs)

        spo_array = np.zeros(ndivs)
      
        for n in np.arange(ndivs):
            n0 = n*sparts
            n1 = ((n+1)*sparts)
            if(n == ndivs-1):
                n1 = nSamples
            #end-if

            print('n0:', n0, 'n1:', n1)
            spo_array[n] =int( calculateSPO(REDf, IRf, n0, n1) )
        #end-for
    return spo_array
    #end-if
#end-def