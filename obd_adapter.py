import sys
import os
import platform
import math
import time

#lib_path = r"C:\Users\paolo\AppData\Local\Programs\Python\Python311\Lib"
#sys.path.insert(0, lib_path)

#import asyncio
import threading
from queue import Queue

if platform.architecture()[0] == "64bit":
    dllfolder = "stdlib64"
else:
    dllfolder = "stdlib"
cwd = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(cwd, dllfolder))
os.environ['PATH'] = os.environ['PATH'] + ";."

#from obd_emulator import FreematicsEmulator
import obd_emulator

import ac
import acsys

PID_RPM = "010C"
PID_SPEED = "010D"
PID_THROTTLE = "0111"
PID_TORQUE = "0163"

rpm_label=0
speed_label=0
throttle_label=0
brake_label=0
torque_label=0

rpm_value=0
speed_value=0
throttle_value=0
brake_value=0
torque_value=0

obd_emulator_status_label=0
is_OBD_emu_connected=False
is_procol_set=False
obd_emu = obd_emulator.FreematicsEmulator()

ioActivity=0
close_io=False
error_label=0
buffer = Queue()

runtime_chrono=0
package_counter=0
#libdir = "serial"          
#lib_path = os.path.join(os.path.dirname(__file__), libdir)
#sys.path.insert(0, lib_path)
#os.environ['PATH'] = os.environ['PATH'] + ";."

#app_name = os.path.basename(__file__).replace(".py", "")
#libdir = "libs\serial"          
#lib_path = os.path.join(os.path.dirname(__file__), libdir)
#sys.path.insert(0, lib_path)
#os.environ['PATH'] = os.environ['PATH'] + ";."

#def obd_emu_connect():
#    ac.setText(obd_emulator_status_label, "OBD Emulator: CONNECTING")
#    obd_emu.connect()
#    #obd_emu.reinitialize()
#    obd_emu.set_protocol("ISO9141_2") 
#    obd_emu.clear_dtc()
#    obd_emu.enable_vin()
#    if obd_emu.set_vin("4" * 17) == "OK":
#        ac.setText(obd_emulator_status_label, "OBD Emulator: OK")
#        return True
#    else: return False

#def process_OBD(emulator_istance, text):

def sendData(buffer:Queue):
    global rpm_value, speed_value, throttle_value, torque_value, close_io, obd_emu, error_label, obd_emulator_status_label, close_io, obd_emu
    #global close_io, obd_emu, error_label, rpm_value, obd_emulator_status_label

    ac.setText(error_label, "STATUS: INIT")

    try:
        while True:
            #msg=buffer.get()
            ac.setText(error_label, "STATUS: {}".format(rpm_value))
            #ac.setText(obd_emulator_status_label, "OBD Emulator: OK")
            #if obd_emu.set_pid(PID_RPM, rpm_value) != "OK":
            #    ac.setText(obd_emulator_status_label, "OBD Emulator: FAULT")
            obd_emu.set_pid(PID_RPM, rpm_value)
            obd_emu.set_pid(PID_SPEED, speed_value)
            obd_emu.set_pid(PID_THROTTLE, throttle_value)
            obd_emu.set_pid(PID_TORQUE, torque_value)
            #time.sleep(0.1)
            if close_io:
                return
    except:
        ac.setText(error_label, "STATUS: ERROR")
        return


def acMain(ac_version):
    global ioActivity, rpm_label, speed_label, throttle_label, brake_label, torque_label, obd_emulator_status_label, close_io, error_label

    #Initializing in-game Window
    appWindow = ac.newApp("obd_adapter")
    ac.setSize(appWindow, 400, 400)

    #Initializing Labels
    rpm_label = ac.addLabel(appWindow, "RPM: 0")
    speed_label = ac.addLabel(appWindow, "Speed: 0 kmh")
    throttle_label = ac.addLabel(appWindow, "Throttle: 0%")
    brake_label = ac.addLabel(appWindow, "Brake: 0%")
    torque_label = ac.addLabel(appWindow, "Torque: 0.00Nm")
    obd_emulator_status_label = ac.addLabel(appWindow, "OBD Emulator: NO")
    error_label = ac.addLabel(appWindow, "STATUS: Undefined")
    

    #Setting Labels position
    ac.setPosition(rpm_label, 3, 30)
    ac.setPosition(speed_label, 3, 50)
    ac.setPosition(throttle_label, 3, 70)
    ac.setPosition(brake_label, 3, 90)
    ac.setPosition(torque_label, 3, 110)
    ac.setPosition(obd_emulator_status_label, 3, 140)
    ac.setPosition(error_label, 3, 170)

    ac.setText(obd_emulator_status_label, "OBD Emulator: CONNECTING")
    obd_emu.connect()
    #obd_emu.reinitialize()
    obd_emu.clear_dtc()
    obd_emu.enable_vin()
    if obd_emu.set_vin("4" * 17) == "OK":
        is_OBD_emu_connected=True
        ac.setText(obd_emulator_status_label, "OBD Emulator: OK")
    obd_emu.set_protocol("ISO9141_2")
    
    ioActivity = threading.Thread(target=sendData, args=(buffer,))
    ioActivity.daemon = True
    ioActivity.start()
    ac.setText(error_label, "STATUS: RUNNING")

    return "obd_adapter"

def acUpdate(deltaT):
    global package_counter, runtime_chrono, rpm_label, speed_label, throttle_label, brake_label, rpm_value, speed_value, throttle_value, brake_value, torque_label, torque_value, obd_emulator_status_label, is_OBD_emu_connected, is_procol_set, obd_emu
    
    #msg={}
    #runtime_chrono_live=time.time()*1000
    #msg = math.trunc(ac.getCarState(0, acsys.CS.RPM))
    #if (runtime_chrono_live - runtime_chrono) > 250:

    rpm = math.trunc(ac.getCarState(0, acsys.CS.RPM))
    speed = math.trunc(ac.getCarState(0, acsys.CS.SpeedKMH))
    throttle = math.trunc(ac.getCarState(0, acsys.CS.Gas)*100)
    #msg["brake"] = ac.getCarState(0, acsys.CS.Brake)
    torque = math.trunc(ac.ext_getCurrentTorque()) # Only works with CSP 0.1.79 (or higher) installed, third party pack for Assetto Corsa
    if torque<0:
        torque=0
    
    #Values update in the in-game app and in the OBD-II Emulator
    #if msg['rpm'] != rpm_value:
    if rpm != rpm_value:
        #send_flag=True
        rpm_value = rpm
        #toSend = math.trunc(rpm_value)
        ac.setText(rpm_label, "RPM: {}".format(rpm))
        #buffer.put(msg)
        #if (runtime_chrono_live - runtime_chrono) > 250:
        #    if (is_OBD_emu_connected and is_procol_set):    
        #        if obd_emu.set_pid(PID_RPM, toSend) == "ERROR":
        #            link_error=True

    if speed != speed_value:
        #send_flag=True
        speed_value = speed
        #toSend = math.trunc(speed_value)
        ac.setText(speed_label, "Speed: {} kmh".format(speed))
        #if (is_OBD_emu_connected and is_procol_set): 
            #if obd_emu.set_pid(PID_SPEED, toSend) == "ERROR":
            #    link_error=True

    if throttle != throttle_value:
        #send_flag=True
        throttle_value = throttle
        #toSend = math.trunc(throttle_value)
        ac.setText(throttle_label, "Throttle: {}%".format(throttle))
        #if (is_OBD_emu_connected and is_procol_set): 
        #    if obd_emu.set_pid(PID_THROTTLE, toSend) == "ERROR":
        #        link_error=True

    #if msg["brake"] != brake_value:
    #    brake_value = msg["brake"]
    #    toSend = math.trunc(brake_value*100)
    #    ac.setText(brake_label, "Brake: {}%".format(toSend))
    #BRAKE Percent is NOT being sent

    if torque != torque_value:
        #send_flag=True
        torque_value = torque
        #toSend = math.trunc(torque_value)
        ac.setText(torque_label, "Torque: {}Nm".format(torque))
        #if (is_OBD_emu_connected and is_procol_set): 
        #    if obd_emu.set_pid(PID_TORQUE, toSend) == "ERROR":
        #        link_error=True

    #if send_flag:
    #    buffer.put(msg)

    #Setup OBD-II Emulator Connection
    #if not is_OBD_emu_connected: 
    #    obd_emu_connect()
    #if not is_OBD_emu_connected:
    #    ac.setText(obd_emulator_status_label, "OBD Emulator: CONNECTING")
    #    obd_emu.connect()
    #    #obd_emu.reinitialize()
    #    obd_emu.clear_dtc()
    #    obd_emu.enable_vin()
    #    if obd_emu.set_vin("4" * 17) == "OK":
    #        is_OBD_emu_connected=True
    #        ac.setText(obd_emulator_status_label, "OBD Emulator: OK")

    #OBD-II Emulator Protocol Setup
    #if not is_procol_set:
    #    if (obd_emu.set_protocol("ISO9141_2") == "OK"):
    #        is_procol_set=True
    
    #OBD-II PID Values Update
    #link_error=False
    #runtime_chrono_live=time.time()*1000
    #if (is_OBD_emu_connected and is_procol_set):
    #if (is_OBD_emu_connected):
        #if (runtime_chrono_live - runtime_chrono) > 250:
        #runtime_chrono=runtime_chrono_live    
    #if obd_emu.set_pid(PID_RPM, rpm) == "ERROR":
    #    link_error=True
    #if obd_emu.set_pid(PID_SPEED, speed) == "ERROR":
    #    link_error=True
    #if obd_emu.set_pid(PID_THROTTLE, throttle) == "ERROR":
    #    link_error=True
    #if obd_emu.set_pid(PID_TORQUE, torque) == "ERROR":
    #    link_error=True
    
    #if link_error:
    #    ac.setText(obd_emulator_status_label, "OBD Emulator: RESTARTING")
    #    obd_emu.reinitialize()
        
    #package_counter = package_counter + 1
    #if package_counter == 25:
    #    sendData()
    #    package_counter=0

    

def acShutdown():
    global obd_emu, ioActivity, close_io
    close_io=True
    ioActivity.join()
    obd_emu.close()
    
    return



    

    

