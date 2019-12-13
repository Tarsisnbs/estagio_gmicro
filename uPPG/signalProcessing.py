#!/usr/bin/env python3

## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## DEVELOPER: Cesar Abascal
## PROFESSORS: Cesar Augusto Prior and Cesar Rodrigues (Yeah. Its almost an overflow!)
## PROJECT: µPPG - Photoplethysmography waves acquisition
## ARCHIVE: Main script to processing ppg signal
## DATE: 18/11/2018 - updated @ 15/03/2019
## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from PPGProcessing.mathprocessing import *
from PPGProcessing.makegraphics import *


#peakx: Times with heartbeat
#peaky: heartbeat events
#systolicArea: Areas with systolics events
systolicArea, peakx, peaky = getSystolicAreaPeaks()
print(systolicArea)
print(peakx)
print(peaky)

# Plot raw signals
plotRawSignals()

# Plot Noisy, Filtered, Clipped and Squared PPG Signal
plotNoisyFilteredClippedSquared()

# Plot MApeak, MAbeat, Blocks of Interest and Result
plotMApeakMAbeatBlocksResult()

# Plot PPG filtered and heatbeats demarkeds
plotHeartbeatIntervals()

# Save heartbeat intervals
saveHeartbeatIntervals()

# Calculate the SPO2 %
spo2 = getSPO(60)
print(len(spo2))
print(spo2)


