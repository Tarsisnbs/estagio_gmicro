#!/usr/bin/env python3

## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## DEVELOPER: Cesar Abascal
## PROFESSORS: Cesar Augusto Prior and Cesar Rodrigues (Yeah. Its almost an overflow!)
## PROJECT: µPPG - Photoplethysmography waves acquisition
## ARCHIVE: Aplication core containing the most importants methods and variables
## DATE: 18/11/2018 - updated @ 15/03/2019
## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


## LIBRARIES ----------------------------------------------------------------------------
import spidev
from time import sleep
import RPi.GPIO as GPIO
from PPGAcquisition.AFEdefs import *
from PPGAcquisition.mDisplay import oledDisplay as od
import time
import socket
from threading import Thread
import sys
import json
import pickle

from scipy.signal import butter, lfilter, lfilter_zi
import numpy as np

## CLASSES and FUNCTIONS ----------------------------------------------------------------
class functions:

    ## VARIABLES ------------------------------------------------------------------------
    # SPI declaration
    spi = spidev.SpiDev()

    # Patient, sample and file variables to loop aquisition
    patientN = ""
    nSamples = 0
    dataFile = None
    testFile = None
    # Control variable to run acquisition and sychronize
    running = True
    syncValue = 0

################# Input 
    sample_data = ''
################ Output
    signals_f = []
    processing_ok = False
################# Tests variables   
    t = 0
    t_ant = 0
    tempo_atual = 0

################## Trash
    recv = False
    ping_full = False 
    pong_full = False
    sizeb = 10
    pkt_cnt = 1    
    t_run = Thread()
    init_strm = False
    
#######  MEM_SYNC ################ 
    SIZE_PKT = 20
    n = 2
    mem1 = [0] * n
    for i in range(n):
        mem1[i] = [0] * SIZE_PKT
    swap1 = False
    swp_mem1 = False
    out_mem1 = [] 
    global_index = 0
########## Flags socket controll
    ctl_byte = b'stop'
    flag_b = b'waiting'

########## Server Socket TCP
    port = 3000
    client = socket.SocketType
    server = None
    
    
    t_wait = Thread()
    
    ## FUNCTIONS -----------------------------------------------------------------------
    def showInitInfos():
        od.uPPGscreen()
        print("\n| uPPG ACQUIRING |\n")
    #end-def

    def showAcqInfos():
        od.acquiringScreen() # Show acquiring screen
        print("\nSample acquiring started...\nTo stop, press CTRL-C\n")
    #end-def

    def mainLoop():    
        print("main loop...")     
        GPIO.output(stePIN, GPIO.LOW) # Enable SPI conversation
        print("Running")
        functions.t_wait = Thread(target = functions.app_waiting())
        functions.t_wait.daemon = True
        functions.t_wait.start()
        
        while(functions.running):
            if(GPIO.input(syncbtnPIN)):
                sleep(0.1) # Like debounce!
                if(GPIO.input(syncbtnPIN)):
                    functions.syncValue = 1
                    GPIO.setup(outputonePIN, GPIO.HIGH)
                    print("synced")
                #end-if
            else:
                functions.syncValue = 0
                GPIO.setup(outputonePIN, GPIO.LOW)
                



    def app_waiting():
        while(True):
            functions.ctl_byte = functions.client.recv(1024)
            if functions.ctl_byte == b'start':  
                functions.flag_b = b"pronto" 
                functions.client.send(functions.flag_b)
                functions.stream_data()    
                break
            else: 
                print('aguardando comando')
                functions.flag_b = b"waiting"
                functions.client.send(functions.flag_b)

    
#######################################################################################################################                 
#######################################################################################################################
    def mem_sync(swp_ch,adr,pkt):
        if functions.swp_mem1 == True:
            ping = 0
            pong = 1
        else: 
            ping = 1
            pong = 0
        if swp_ch == True:
            functions.out_mem1 = functions.mem1[pong]
            functions.mem1[pong] = [0]*functions.SIZE_PKT   
        functions.mem1[ping][adr] = pkt    

    def mem_ctr(len_a, len_b): 
        if(len_a != 0 and  len_b == 0) or (len_b != 0 and  len_a == 0): 
            #print ('swap1 time and mem1:' + str(functions.mem1))
            functions.swp_mem1 =  not(functions.swp_mem1) # CH0 is Input, in the next time is output
            return True # condição de swap1
        else: 
            return False

    def stream_data():
        print('servidor iniciando streaming...')
        while True: 
            #functions.get_signals_f()
            if functions.ctl_byte == b'stop':    
                print('breaking Loop t_run')
                functions.flag_b = b"waiting"
                functions.t_wait.run(target = functions.app_waiting())  
                break 
            else:
                if len(functions.out_mem1) == functions.SIZE_PKT:
                    #print('buffer de saída: ' + str(functions.signals_f))
                    p = pickle.dumps(functions.out_mem1)
                    functions.out_mem1 = []
                    functions.processing_ok = False
                    ################################
                    functions.client.send(p)
                    functions.ctl_byte  = (functions.client.recv(1024))  
                    ################################..............
                    if functions.ctl_byte == b'stop': 
                        functions.flag_b = b"waiting"
                    ################################ blocking calls    
                    functions.client.send(functions.flag_b)
                    ################################..............
                    functions.t_ant = functions.t
                    functions.t = time.time()
                    delta = functions.t - functions.t_ant
                    #print('tempo para enviar quadro: ' + str(delta))
                else: pass 
#######################################################
# ---------------------------------------------------------CHANGES AFTER V:0.5                
#######################################################
   
    def get_signals_f():
        if len(functions.out_mem1) == functions.SIZE_PKT:
            lowcut = 0.4
            highcut = 8
            order = 3
            sps = 200 # Samples per second
            REDsignal, IRsignal, synced = [], [], []
            signalBase = 1.045
            print('processando novo quadro')
            #p = pickle.dumps(functions.out_mem1)
            for i in range(0,20):
                aux = str(functions.out_mem1[i]).split(',')
                #print(aux)
                REDsignal.append(signalBase - float(aux[0]))
                IRsignal.append(signalBase - float(aux[1]))
                functions.signals_f.append(str(signalBase - float(aux[0])) + "," + str(signalBase - float(aux[1])) + "," + str(1))
                #samples +=1
            REDf = functions.butter_bandpass_filter_zi(REDsignal, lowcut, highcut, sps, order)
            IRf = functions.butter_bandpass_filter_zi(IRsignal, lowcut, highcut, sps, order)
            functions.processing_ok = True
        else:
            pass
        pass
        

#######################################################################################################################                 
#######################################################################################################################
    def finish():
        functions.running = False
        functions.AFEfinish()
        functions.closeSPIConnection()
        functions.dataFile.close() # Close data file
        od.acquiredScreen(functions.patientN, sps, functions.nSamples) # Show acquired data screen on display
    #end-def

    def openSPIConnection():
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)

        # IO Interface
        GPIO.setup(syncbtnPIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # Set sync button pin as input.
        GPIO.setup(thirdbtnPIN, GPIO.IN) # Set third button pin as input.
        GPIO.setup(outputonePIN, GPIO.OUT, initial=GPIO.LOW) # Set output one pin as output and init with low.

        # Connection Interface
        #GPIO.setup(diagendPIN, GPIO.IN) # Set diagnostic pin as input.
        #GPIO.setup(pdalmPIN, GPIO.IN) # Set pd alarm pin as input.
        #GPIO.setup(ledalmPIN, GPIO.IN) # Set data led alarm pin as input.
        GPIO.setup(resetPIN, GPIO.OUT, initial=GPIO.HIGH) # Set resetPIN as output and init with high.
        GPIO.setup(pdnPIN, GPIO.OUT, initial=GPIO.HIGH) # Set pdnPin as output and init with high.
        GPIO.setup(stePIN, GPIO.OUT, initial=GPIO.HIGH) # Set stePin as output and init with high.
        GPIO.setup(adcrdyPIN, GPIO.IN) # Set data ISR pin as input.

        # SPI Definition
        functions.spi.open(0,0)
        functions.spi.max_speed_hz = 8000000 # 8MHz
        functions.spi.mode = 0b00 # CPOL = 0, CPHA = 0
    #end def

    def closeSPIConnection():
        functions.spi.close()
        GPIO.cleanup()
    #end def

    def setISR():
        GPIO.add_event_detect(adcrdyPIN, GPIO.RISING, callback=functions.adcrdyInterruption) # Enable data ISR.
    #end-def

    def adcrdyInterruption(state):
        

        RED, IR = functions.SPIReadLED2LED1Values() # RED=LED2 and IR=LED1
        functions.sample_data = str('%.16f' % (RED*digitalToVolt)) + "," + str('%.16f' % (IR*digitalToVolt)) + "," + str(functions.global_index) 
        #print('ctl_b: ' + str(functions.ctl_byte) + '|flag_b: ' + str(functions.flag_b))
        if functions.ctl_byte == b'start':
            if functions.global_index < int(functions.SIZE_PKT):
                functions.mem_sync(functions.mem_ctr((functions.mem1[0][-1]), (functions.mem1[1][-1])), functions.global_index,functions.sample_data)
                functions.global_index = functions.global_index + 1
            else: functions.global_index = 0    
        else: 'aguardando cliente para preparar pacotes'    
        ##############
         
        ##############

        '''
       # if functions.ctl_byte == b'start': 
          #  temp_string = str('%.16f' % (delta)) + "," + "streaming"
          #  functions.dataFile.write("%s\n" % temp_string)
        print('hi! ' + str(functions.t))
        #else: 
          #  temp_string = str('%.16f' % (delta)) + "," + "waiting"
           # functions.dataFile.write("%s\n" % temp_string )

        if functions.swap1 == True and functions.ping_full == False:
            if len(functions.ping) >= 10:                       
                functions.ping_full = True 
                functions.pong.append(functions.sample_data)
            else:            
                functions.ping.append(functions.sample_data)     
        elif functions.swap1 == False and functions.pong_full == False:    
            if len(functions.pong) >= 10:         
                functions.pong_full = True             
                functions.ping.append(functions.sample_data)     
            else: 
                functions.pong.append(functions.sample_data)     
                
        '''

    def SPIWriteReg(regAddress, regValue):
        functions.spi.xfer2([regAddress])

        maskLSB = 0xFF
        maskMidByte = 0xFF00
        maskMSB = 0xFF0000

        LSB = regValue & maskLSB
        midByte = (regValue & maskMidByte) >> 8
        MSB = (regValue & maskMSB) >> 16

        functions.spi.xfer2([MSB])
        functions.spi.xfer2([midByte])
        functions.spi.xfer2([LSB])
    #end def

    def SPIReadLED2LED1Values():
        #functions.spi.xfer2([LED2VAL]) # Just LED2
        functions.spi.xfer2([LED2ALED2VAL]) # LED2 - ALED2
        ret2 = functions.spi.xfer2([0x00] * 3)
        l2Value = (ret2[0] << 8) | ret2[1]
        l2Value = (l2Value << 8) | ret2[2]

        #functions.spi.xfer2([LED1VAL]) # Just LED1
        functions.spi.xfer2([LED1ALED1VAL]) # LED1 - ALED1
        ret1 = functions.spi.xfer2([0x00] * 3)
        l1Value = (ret1[0] << 8) | ret1[1]
        l1Value = (l1Value << 8) | ret1[2]

        return l2Value, l1Value
    #end def

    # This function will write some configurations in AFE4490 registers to initialize and enable ISR.
    def AFEinit():
        print("\nInitializing AFE4490 CI")

        GPIO.output(stePIN, GPIO.LOW) # ENABLE SPI CONVERSATION

        # To use on SPI Read functions.
        functions.SPIWriteReg(CONTROL0, 8) # Software reset applied. Resets all internal registers
                                           #to the default values and self-clears to '0'.
                                           # This will also DISABLE SPI READ (enable SPI write).

        # To configure timer control registers, see the AFE4490 datasheet page 36.

        # Set the Pulse Repetition Counter
        functions.SPIWriteReg(PRPCOUNT, 19999) # num = 4MHz/SPS -1 -> num = 4MHz/200SPS -1 -> num = 19999

        # LED 2 (RED LED) Registers ...
        functions.SPIWriteReg(LED2STC, 15080) # Start LED2 sample at PRPCOUNT = 15080
        functions.SPIWriteReg(LED2ENDC, 18998) # End LED2 sample at PRPCOUNT = 18998
        functions.SPIWriteReg(LED2LEDSTC, 15000) # Start LED2 at PRPCOUNT = 15000
        functions.SPIWriteReg(LED2LEDENDC, 18999) # End LED2 at PRPCOUNT = 18999
        functions.SPIWriteReg(ALED2STC, 80) # Start Amb LED2 sample at PRPCOUNT = 80
        functions.SPIWriteReg(ALED2ENDC, 3998) # End Amb LED2 sample at PRPCOUNT = 3998

        # LED 1 (IR LED) Registers ...
        functions.SPIWriteReg(LED1STC, 5080) # Start LED1 sample at PRPCOUNT = 5080
        functions.SPIWriteReg(LED1ENDC, 8998) # End LED1 sample at PRPCOUNT = 8998
        functions.SPIWriteReg(LED1LEDSTC, 5000) # Start LED1 at PRPCOUNT = 5000
        functions.SPIWriteReg(LED1LEDENDC, 8999) # End LED1 at PRPCOUNT = 8999
        functions.SPIWriteReg(ALED1STC, 10080) # Start Amb LED1 sample at PRPCOUNT = 10080
        functions.SPIWriteReg(ALED1ENDC, 13998) # End Amb LED1 sample at PRPCOUNT = 13998

        # ... LED 2 (RED LED) Registers
        functions.SPIWriteReg(LED2CONVST, 6) # Start LED2 conversion at PRPCOUNT = 6
        functions.SPIWriteReg(LED2CONVEND, 4999) # End LED2 conversion at PRPCOUNT = 4999
        functions.SPIWriteReg(ALED2CONVST, 5006) # Start Amb LED2 conversion at PRPCOUNT = 5006
        functions.SPIWriteReg(ALED2CONVEND, 9999) # End Amb LED2 conversion at PRPCOUNT = 9999

        # ... LED 1 (IR LED) Registers
        functions.SPIWriteReg(LED1CONVST, 10006) # Start LED1 conversion at PRPCOUNT = 10006
        functions.SPIWriteReg(LED1CONVEND, 14999) # End LED1 conversion at PRPCOUNT = 14999
        functions.SPIWriteReg(ALED1CONVST, 15006) # Start Amb LED1 conversion at PRPCOUNT = 15006
        functions.SPIWriteReg(ALED1CONVEND, 19999) # End Amb LED1 conversion at PRPCOUNT = 19999

        # To manipulate the ADCx Reset positions
        ## It will manipulate the pulses, in this case, we've 4 pulses, so we've 25% on duty cycle.
        ## We're using 5000 per pulse and 19999 at PRPCOUNT (200SPS at 4MHz), so we've 25% on duty cycle and 200SPS.
        functions.SPIWriteReg(ADCRSTSTCT0, 0) # Start pulse 1 at PRPCOUNT = 0
        functions.SPIWriteReg(ADCRSTENDCT0, 5) # End pulse 1 at PRPCOUNT = 5
        functions.SPIWriteReg(ADCRSTSTCT1, 5000) # Start pulse 2 at PRPCOUNT = 5000
        functions.SPIWriteReg(ADCRSTENDCT1, 5005) # End pulse 2 at PRPCOUNT = 5005
        functions.SPIWriteReg(ADCRSTSTCT2, 10000) # Start pulse 3 at PRPCOUNT = 10000
        functions.SPIWriteReg(ADCRSTENDCT2, 10005) # End pulse 3 at PRPCOUNT = 10005
        functions.SPIWriteReg(ADCRSTSTCT3, 15000) # Start pulse 4 at PRPCOUNT = 15000
        functions.SPIWriteReg(ADCRSTENDCT3, 15005) # End pulse 4 at PRPCOUNT = 15005

        # Other settings
        functions.SPIWriteReg(CONTROL2, 262144) # TX_REF=01b -> 1.0-V Tx reference voltage available on TX_REF pin.
                                                # RST_CLK_ON_PD_ALM=0b -> Normal mode. No reset clock signal is connected to the PD_ALM pin.
                                                # EN_ADC_BYP=0b -> Normal mode. The internal ADC is active.
                                                # TXBRGMOD=0b -> LED driver is configured as an H-bridge.
                                                # DIGOUT_TRISTATE=0b -> SPI active and in use.
                                                # XTALDIS=0b -> The crystal module is enable. The 8MHz crystal mus be connected to the XIN and XOUT pins.
                                                # EN_SLOW_DIAG=0b -> Fast diagnostics mode, 8ms.
        
        functions.SPIWriteReg(TIAGAIN, 16638) # ENSEPGAIN=0b -> The RF, CF values and stage 2 gain settings are the same for both the LED2 and LED1 signals.
                                              # ENSEPGAIN=1b -> The RF, CF values and stage 2 gain settings can be independently set for the LED2 and
                                              #LED1 signals. The values for LED1 are specified using the RF_LED1, CF_LED1,
                                              #STAGE2EN1, and STG2GAIN1 bits in the TIAGAIN register, whereas the values for LED2
                                              #are specified using the corresponding bits in the TIA_AMB_GAIN register.
                                                # STAGE2EN1=1b -> Stage 2 is enabled with the gain value specified by the STG2GAIN1[2:0] bits
                                                # STG2GAIN1=000b -> Gain = 1x
                                                # CF_LED1=11111b -> LED1 Cf=270pF
                                                # RF_LED1=110b -> LED1 Rf=1MR
                                                # Fc = 580Hz

        functions.SPIWriteReg(TIA_AMB_GAIN, 16638) # AMBDAC=0000b -> Cancellation current = 0uA
                                                   # FLTRCNRSEL=0b -> 500Hz filter corner
                                                   # STAGE2EN2=1b -> Stage 2 is enabled with the gain value specified by the STG2GAIN2[2:0] bits
                                                   # STG2GAIN2=000b -> Gain = 1x
                                                   # CF_LED2=11111b -> LED2 Cf=270pF
                                                   # RF_LED2=110b -> LED2 Rf=1MR
                                                   # Fc = 580Hz

        functions.SPIWriteReg(LEDCNTRL, 70681) # LED_RANGE=01b -> Imax=100mA and Vhr=1.6V OBS.: IMPIRICAL GOOD VALUES FOR SPO2EVM PROBE.
                                               # LED1(IR)=00010100b=20d -> LED1 current = (20*100)/256 ~= 7.81mA
                                               # LED2(RED)=00011001b=25d -> LED2 current = (25*100)/256 ~= 9.76mA
        
        
        functions.SPIWriteReg(ALARM, 0) # ALARM reg need to be set before CONTROL1 reg.
                                        # ALMPINCLKEN=0b -> Disables the monitoring of internal clocks.
                                        #The PD_ALM and LED_ALM pins function as diagnostic fault alarm output pins (default after reset).

        functions.SPIWriteReg(CONTROL1, 263) # CLKALMPIN=011b -> PD_ALM=Sample LED2 pulse and LED_ALM=Sample LED1 pulse.
                                             # TIMEREN=1b -> Internal clock enable (timer module is enable)
                                             # NUMAV=00000111d -> To avarage 8 ADC samples.
        
        functions.SPIWriteReg(CONTROL0,1) # ENABLE SPI READ (disable SPI write)

        GPIO.output(stePIN, GPIO.HIGH) # DISABLE SPI CONVERSATION.

        print("... done")

        #init server socket tcp and wait a client
        functions.server = socket.socket()
        port = 3001
        functions.server.bind(('', port))
        functions.server.listen(1)
        functions.client,addr = functions.server.accept()
        print("got a connection from %s" % str(addr))


    #end-def

    # This function will write default values into AFE4490 registers to finish.
    def AFEfinish():
        print("\nFinishing AFE4490 CI")
        GPIO.output(stePIN, GPIO.LOW) # Enable SPI conversation

        functions.SPIWriteReg(CONTROL0,0) # Disable SPI read (Enable SPI Write)
        functions.SPIWriteReg(CONTROL0, 8) # Software reset applied. Resets all internal registers to the default values.

        GPIO.output(stePIN, GPIO.HIGH) # Disable SPI conversation
        functions.client.close()
        print("... done\n")

    #end-def

#end-class
