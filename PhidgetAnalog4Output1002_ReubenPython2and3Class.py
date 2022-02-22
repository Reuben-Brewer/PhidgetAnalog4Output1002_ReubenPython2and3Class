# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision D, 02/22/2022

Verified working on: Python 2.7 and 3 for Windows 8.1 64-bit and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

import os, sys, platform
import time, datetime
import math
import collections
import inspect #To enable 'TellWhichFileWereIn'
import threading
import traceback

###############
if sys.version_info[0] < 3:
    from Tkinter import * #Python 2
    import tkFont
    import ttk
else:
    from tkinter import * #Python 3
    import tkinter.font as tkFont #Python 3
    from tkinter import ttk
###############

###############
if sys.version_info[0] < 3:
    import Queue  # Python 2
else:
    import queue as Queue  # Python 3
###############

###############
if sys.version_info[0] < 3:
    from builtins import raw_input as input
else:
    from future.builtins import input as input
############### #"sudo pip3 install future" (Python 3) AND "sudo pip install future" (Python 2)

###############
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
###############

###########################################################
###########################################################
#To install Phidget22, enter folder "Phidget22Python_1.0.0.20190107\Phidget22Python" and type "python setup.py install"
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.VoltageOutput import *
###########################################################
###########################################################

class PhidgetAnalog4Output1002_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    #######################################################################################################################
    #######################################################################################################################
    def __init__(self, setup_dict): #Subclass the Tkinter Frame

        print("#################### PhidgetAnalog4Output1002_ReubenPython2and3Class __init__ starting. ####################")

        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = -1
        self.EnableInternal_MyPrint_Flag = 0
        self.MainThread_still_running_flag = 0

        self.ToggleVoltageToMeasureMaxFrequency_ToggleState = -1 #-1 or 1, never 0

        self.VoltageOutputsList_PhidgetsVoltageOutputObjects = list()

        self.VoltageOutputsList_AttachedAndOpenFlag = [-1.0] * 4
        self.VoltageOutputsList_ErrorCallbackFiredFlag = [-1.0] * 4

        self.VoltageOutputsList_EnabledState = [-1] * 4
        self.VoltageOutputsList_EnabledState_NeedsToBeChangedFlag = [1]*4
        self.VoltageOutputsList_EnabledState_ToBeSet = [0] * 4

        self.VoltageOutputsList_Voltage = [-1] * 4
        self.VoltageOutputsList_Voltage_NeedsToBeChangedFlag = [1]*4
        self.VoltageOutputsList_Voltage_ToBeSet = [0] * 4

        self.MostRecentDutyCycleDict = dict()

        ##########################################
        ##########################################
        if platform.system() == "Linux":

            if "raspberrypi" in platform.uname(): #os.uname() doesn't work in windows
                self.my_platform = "pi"
            else:
                self.my_platform = "linux"

        elif platform.system() == "Windows":
            self.my_platform = "windows"

        elif platform.system() == "Darwin":
            self.my_platform = "mac"

        else:
            self.my_platform = "other"

        print("The OS platform is: " + self.my_platform)
        ##########################################
        ##########################################

        ##########################################
        ##########################################
        if "GUIparametersDict" in setup_dict:
            self.GUIparametersDict = setup_dict["GUIparametersDict"]

            ##########################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("USE_GUI_FLAG = " + str(self.USE_GUI_FLAG))
            ##########################################

            ##########################################
            if "root" in self.GUIparametersDict:
                self.root = self.GUIparametersDict["root"]
                self.RootIsOwnedExternallyFlag = 1
            else:
                self.root = None
                self.RootIsOwnedExternallyFlag = 0

            print("RootIsOwnedExternallyFlag = " + str(self.RootIsOwnedExternallyFlag))
            ##########################################

            ##########################################
            if "GUI_RootAfterCallbackInterval_Milliseconds" in self.GUIparametersDict:
                self.GUI_RootAfterCallbackInterval_Milliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_RootAfterCallbackInterval_Milliseconds", self.GUIparametersDict["GUI_RootAfterCallbackInterval_Milliseconds"], 0.0, 1000.0))
            else:
                self.GUI_RootAfterCallbackInterval_Milliseconds = 30

            print("GUI_RootAfterCallbackInterval_Milliseconds = " + str(self.GUI_RootAfterCallbackInterval_Milliseconds))
            ##########################################

            ##########################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            ##########################################

            ##########################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            ##########################################

            ##########################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("NumberOfPrintLines = " + str(self.NumberOfPrintLines))
            ##########################################

            ##########################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            ##########################################

            ##########################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("GUI_ROW = " + str(self.GUI_ROW))
            ##########################################

            ##########################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("GUI_COLUMN = " + str(self.GUI_COLUMN))
            ##########################################

            ##########################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("GUI_PADX = " + str(self.GUI_PADX))
            ##########################################

            ##########################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("GUI_PADY = " + str(self.GUI_PADY))
            ##########################################

            ##########################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 0.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 0

            print("GUI_ROWSPAN = " + str(self.GUI_ROWSPAN))
            ##########################################

            ##########################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 0

            print("GUI_COLUMNSPAN = " + str(self.GUI_COLUMNSPAN))
            ##########################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG = " + str(self.USE_GUI_FLAG))

        print("GUIparametersDict = " + str(self.GUIparametersDict))
        ##########################################
        ##########################################

        ##########################################
        if "DesiredSerialNumber" in setup_dict:
            try:
                self.DesiredSerialNumber = int(setup_dict["DesiredSerialNumber"])
            except:
                print("ERROR: DesiredSerialNumber invalid.")
        else:
            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
            print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__ ERROR: Must initialize object with 'DesiredSerialNumber' argument.")
            return
        
        print("DesiredSerialNumber: " + str(self.DesiredSerialNumber))
        ##########################################

        ##########################################
        if "NameToDisplay_UserSet" in setup_dict:
            self.NameToDisplay_UserSet = str(setup_dict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""
            ##########################################

        ##########################################
        if "WaitForAttached_TimeoutDuration_Milliseconds" in setup_dict:
            self.WaitForAttached_TimeoutDuration_Milliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("WaitForAttached_TimeoutDuration_Milliseconds", setup_dict["WaitForAttached_TimeoutDuration_Milliseconds"], 0.0, 60000.0))

        else:
            self.WaitForAttached_TimeoutDuration_Milliseconds = 5000

        print("WaitForAttached_TimeoutDuration_Milliseconds: " + str(self.WaitForAttached_TimeoutDuration_Milliseconds))
        ##########################################

        ##########################################
        if "UsePhidgetsLoggingInternalToThisClassObjectFlag" in setup_dict:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UsePhidgetsLoggingInternalToThisClassObjectFlag", setup_dict["UsePhidgetsLoggingInternalToThisClassObjectFlag"])
        else:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = 1

        print("UsePhidgetsLoggingInternalToThisClassObjectFlag: " + str(self.UsePhidgetsLoggingInternalToThisClassObjectFlag))
        ##########################################

        ##########################################
        if "VoltageOutputsList_MinVoltage" in setup_dict:
            VoltageOutputsList_MinVoltage_TEMP = setup_dict["VoltageOutputsList_MinVoltage"]
            
            if self.IsInputList(VoltageOutputsList_MinVoltage_TEMP) == 1 and len(VoltageOutputsList_MinVoltage_TEMP) == 4:
                self.VoltageOutputsList_MinVoltage = list()
                
                for VoltageOutputChannel, VoltageValue in enumerate(VoltageOutputsList_MinVoltage_TEMP):
                    MinVoltage = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VoltageOutputsList_MinVoltage, VoltageOutputChannel " + str(VoltageOutputChannel), VoltageValue, -10.0, 10.0)
                    self.VoltageOutputsList_MinVoltage.append(MinVoltage)
            else:
                print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: ERROR, 'VoltageOutputsList_MinVoltage' must be length 4.")
                
        else:
            self.VoltageOutputsList_MinVoltage = [-10.0]*4

        print("VoltageOutputsList_MinVoltage: " + str(self.VoltageOutputsList_MinVoltage))
        ##########################################

        ##########################################
        if "VoltageOutputsList_MaxVoltage" in setup_dict:
            VoltageOutputsList_MaxVoltage_TEMP = setup_dict["VoltageOutputsList_MaxVoltage"]
            
            if self.IsInputList(VoltageOutputsList_MaxVoltage_TEMP) == 1 and len(VoltageOutputsList_MaxVoltage_TEMP) == 4:
                self.VoltageOutputsList_MaxVoltage = list()
                
                for VoltageOutputChannel, VoltageValue in enumerate(VoltageOutputsList_MaxVoltage_TEMP):
                    MaxVoltage = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VoltageOutputsList_MaxVoltage, VoltageOutputChannel " + str(VoltageOutputChannel), VoltageValue, -10.0, 10.0)
                    self.VoltageOutputsList_MaxVoltage.append(MaxVoltage)
            else:
                print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: ERROR, 'VoltageOutputsList_MaxVoltage' must be length 4.")
                
        else:
            self.VoltageOutputsList_MaxVoltage = [-10.0]*4

        print("VoltageOutputsList_MaxVoltage: " + str(self.VoltageOutputsList_MaxVoltage))
        ##########################################

        ##########################################
        if "MainThread_TimeToSleepEachLoop" in setup_dict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", setup_dict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.005

        print("MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        ##########################################

        ##########################################
        if "ReadActualVoltageAfterSettingNewValueFlag" in setup_dict:
            self.ReadActualVoltageAfterSettingNewValueFlag = self.PassThrough0and1values_ExitProgramOtherwise("ReadActualVoltageAfterSettingNewValueFlag", setup_dict["ReadActualVoltageAfterSettingNewValueFlag"])
        else:
            self.ReadActualVoltageAfterSettingNewValueFlag = 1

        print("ReadActualVoltageAfterSettingNewValueFlag: " + str(self.ReadActualVoltageAfterSettingNewValueFlag))
        ##########################################

        ##########################################
        if "ToggleVoltageToMeasureMaxFrequencyFlag" in setup_dict:
            self.ToggleVoltageToMeasureMaxFrequencyFlag = self.PassThrough0and1values_ExitProgramOtherwise("ToggleVoltageToMeasureMaxFrequencyFlag", setup_dict["ToggleVoltageToMeasureMaxFrequencyFlag"])
        else:
            self.ToggleVoltageToMeasureMaxFrequencyFlag = 1

        print("ToggleVoltageToMeasureMaxFrequencyFlag: " + str(self.ToggleVoltageToMeasureMaxFrequencyFlag))
        ##########################################

        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################

        #########################################################
        self.CurrentTime_CalculatedFromMainThread = -11111
        self.LastTime_CalculatedFromMainThread = -11111
        self.DataStreamingFrequency_CalculatedFromMainThread = -11111
        self.DataStreamingDeltaT_CalculatedFromMainThread = -11111

        self.DetectedDeviceName = "default"
        self.DetectedDeviceID = "default"
        self.DetectedDeviceVersion = "default"
        self.DetectedDeviceSerialNumber = "default"
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:

            #########################################################
            self.VoltageOutput0object = VoltageOutput()
            self.VoltageOutputsList_PhidgetsVoltageOutputObjects.append(self.VoltageOutput0object)
            self.VoltageOutput0object.setDeviceSerialNumber(self.DesiredSerialNumber)
            self.VoltageOutput0object.setChannel(0)
            self.VoltageOutput0object.setOnAttachHandler(self.VoltageOutput0onAttachCallback)
            self.VoltageOutput0object.setOnDetachHandler(self.VoltageOutput0onDetachCallback)
            self.VoltageOutput0object.setOnErrorHandler(self.VoltageOutput0onErrorCallback)
            self.VoltageOutput0object.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)

            self.VoltageOutput1object = VoltageOutput()
            self.VoltageOutputsList_PhidgetsVoltageOutputObjects.append(self.VoltageOutput1object)
            self.VoltageOutput1object.setDeviceSerialNumber(self.DesiredSerialNumber)
            self.VoltageOutput1object.setChannel(1)
            self.VoltageOutput1object.setOnAttachHandler(self.VoltageOutput1onAttachCallback)
            self.VoltageOutput1object.setOnDetachHandler(self.VoltageOutput1onDetachCallback)
            self.VoltageOutput1object.setOnErrorHandler(self.VoltageOutput1onErrorCallback)
            self.VoltageOutput1object.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            
            self.VoltageOutput2object = VoltageOutput()
            self.VoltageOutputsList_PhidgetsVoltageOutputObjects.append(self.VoltageOutput2object)
            self.VoltageOutput2object.setDeviceSerialNumber(self.DesiredSerialNumber)
            self.VoltageOutput2object.setChannel(2)
            self.VoltageOutput2object.setOnAttachHandler(self.VoltageOutput2onAttachCallback)
            self.VoltageOutput2object.setOnDetachHandler(self.VoltageOutput2onDetachCallback)
            self.VoltageOutput2object.setOnErrorHandler(self.VoltageOutput2onErrorCallback)
            self.VoltageOutput2object.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            
            self.VoltageOutput3object = VoltageOutput()
            self.VoltageOutputsList_PhidgetsVoltageOutputObjects.append(self.VoltageOutput3object)
            self.VoltageOutput3object.setDeviceSerialNumber(self.DesiredSerialNumber)
            self.VoltageOutput3object.setChannel(3)
            self.VoltageOutput3object.setOnAttachHandler(self.VoltageOutput3onAttachCallback)
            self.VoltageOutput3object.setOnDetachHandler(self.VoltageOutput3onDetachCallback)
            self.VoltageOutput3object.setOnErrorHandler(self.VoltageOutput3onErrorCallback)
            self.VoltageOutput3object.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            #########################################################

            self.PhidgetsDeviceConnectedFlag = 1

        except PhidgetException as e:
            self.PhidgetsDeviceConnectedFlag = 0
            print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__Failed to attach, Phidget Exception %i: %s" % (e.code, e.details))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.PhidgetsDeviceConnectedFlag == 1:
            dummy_var = 0

            #########################################################
            if self.UsePhidgetsLoggingInternalToThisClassObjectFlag == 1:
                try:
                    Log.enable(LogLevel.PHIDGET_LOG_INFO, os.getcwd() + "\PhidgetAnalog4Output1002_ReubenPython2and3Class_PhidgetLog_INFO.txt")
                    print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__Enabled Phidget Logging.")
                except PhidgetException as e:
                    print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__Failed to enable Phidget Logging, Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceName = self.VoltageOutput0object.getDeviceName()
                print("DetectedDeviceName: " + self.DetectedDeviceName)

            except PhidgetException as e:
                print("Failed to call 'getDeviceName', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceSerialNumber = self.VoltageOutput0object.getDeviceSerialNumber()
                print("DetectedDeviceSerialNumber: " + str(self.DetectedDeviceSerialNumber))

            except PhidgetException as e:
                print("Failed to call 'getDeviceSerialNumber', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceID = self.VoltageOutput0object.getDeviceID()
                print("DetectedDeviceID: " + str(self.DetectedDeviceID))

            except PhidgetException as e:
                print("Failed to call 'getDeviceID', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceVersion = self.VoltageOutput0object.getDeviceVersion()
                print("DetectedDeviceVersion: " + str(self.DetectedDeviceVersion))

            except PhidgetException as e:
                print("Failed to call 'getDeviceVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceLibraryVersion = self.VoltageOutput0object.getLibraryVersion()
                print("DetectedDeviceLibraryVersion: " + str(self.DetectedDeviceLibraryVersion))

            except PhidgetException as e:
                print("Failed to call 'getLibraryVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            if self.DetectedDeviceSerialNumber != self.DesiredSerialNumber:
                print("The desired Serial Number (" + str(self.DesiredSerialNumber) + ") does not match the detected serial number (" + str(self.DetectedDeviceSerialNumber) + ").")
                input("Press any key (and enter) to exit.")
                sys.exit()
            #########################################################

            ##########################################
            self.MainThread_ThreadingObject = threading.Thread(target=self.MainThread, args=())
            self.MainThread_ThreadingObject.start()
            ##########################################

            ##########################################
            if self.USE_GUI_FLAG == 1:
                self.StartGUI(self.root)
            ##########################################

            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1

        #########################################################
        #########################################################

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def __del__(self):
        dummy_var = 0
    #######################################################################################################################
    #######################################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber):

        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThrough0and1values_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be 0 or 1 (value was " +
                          str(InputNumber_ConvertedToFloat) +
                          "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue):
        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat >= RangeMinValue and InputNumber_ConvertedToFloat <= RangeMaxValue:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be in the range [" +
                          str(RangeMinValue) +
                          ", " +
                          str(RangeMaxValue) +
                          "] (value was " +
                          str(InputNumber_ConvertedToFloat) + "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TellWhichFileWereIn(self):

        #We used to use this method, but it gave us the root calling file, not the class calling file
        #absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        #filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

        frame = inspect.stack()[1]
        filename = frame[1][frame[1].rfind("\\") + 1:]
        filename = filename.replace(".py","")

        return filename
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageOutputGENERALonAttachCallback(self, VoltageOutputChannel):

        try:
            self.VoltageOutputsList_AttachedAndOpenFlag[VoltageOutputChannel] = 1
            self.MyPrint_WithoutLogFile("$$$$$$$$$$ VoltageOutputGENERALonAttachCallback event for VoltageOutputChannel " + str(VoltageOutputChannel) + ", Attached! $$$$$$$$$$")

        except PhidgetException as e:
            self.VoltageOutputsList_AttachedAndOpenFlag[VoltageOutputChannel] = 0
            self.MyPrint_WithoutLogFile("VoltageOutputGENERALonAttachCallback event for VoltageOutputChannel " + str(VoltageOutputChannel) + ", ERROR: Failed to attach VoltageOutput0, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageOutputGENERALonDetachCallback(self, VoltageOutputChannel):

        self.VoltageOutputsList_AttachedAndOpenFlag[VoltageOutputChannel] = 0
        self.MyPrint_WithoutLogFile("$$$$$$$$$$ VoltageOutputGENERALonDetachCallback event for VoltageOutputChannel " + str(VoltageOutputChannel) + ", Detatched! $$$$$$$$$$")

        try:
            self.VoltageOutputsList_PhidgetsVoltageOutputObjects[VoltageOutputChannel].openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            time.sleep(0.250)

        except PhidgetException as e:
            self.MyPrint_WithoutLogFile("VoltageOutputGENERALonDetachCallback event for VoltageOutput Channel " + str(VoltageOutputChannel) + ", failed to openWaitForAttachment, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageOutputGENERALonErrorCallback(self, VoltageOutputChannel, code, description):

        self.VoltageOutputsList_ErrorCallbackFiredFlag[VoltageOutputChannel] = 1

        self.MyPrint_WithoutLogFile("VoltageOutputGENERALonErrorCallback event for VoltageOutput Channel " + str(VoltageOutputChannel) + ", Error Code " + ErrorEventCode.getName(code) + ", description: " + str(description))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageOutput0onAttachCallback(self, HandlerSelf):

        VoltageOutputChannel = 0
        self.VoltageOutputGENERALonAttachCallback(VoltageOutputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageOutput0onDetachCallback(self, HandlerSelf):

        VoltageOutputChannel = 0
        self.VoltageOutputGENERALonDetachCallback(VoltageOutputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageOutput0onErrorCallback(self, HandlerSelf, code, description):

        VoltageOutputChannel = 0
        self.VoltageOutputGENERALonErrorCallback(VoltageOutputChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageOutput1onAttachCallback(self, HandlerSelf):

        VoltageOutputChannel = 1
        self.VoltageOutputGENERALonAttachCallback(VoltageOutputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageOutput1onDetachCallback(self, HandlerSelf):

        VoltageOutputChannel = 1
        self.VoltageOutputGENERALonDetachCallback(VoltageOutputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageOutput1onErrorCallback(self, HandlerSelf, code, description):

        VoltageOutputChannel = 1
        self.VoltageOutputGENERALonErrorCallback(VoltageOutputChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def VoltageOutput2onAttachCallback(self, HandlerSelf):

        VoltageOutputChannel = 2
        self.VoltageOutputGENERALonAttachCallback(VoltageOutputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageOutput2onDetachCallback(self, HandlerSelf):

        VoltageOutputChannel = 2
        self.VoltageOutputGENERALonDetachCallback(VoltageOutputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageOutput2onErrorCallback(self, HandlerSelf, code, description):

        VoltageOutputChannel = 2
        self.VoltageOutputGENERALonErrorCallback(VoltageOutputChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageOutput3onAttachCallback(self, HandlerSelf):

        VoltageOutputChannel = 3
        self.VoltageOutputGENERALonAttachCallback(VoltageOutputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageOutput3onDetachCallback(self, HandlerSelf):

        VoltageOutputChannel = 3
        self.VoltageOutputGENERALonDetachCallback(VoltageOutputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageOutput3onErrorCallback(self, HandlerSelf, code, description):

        VoltageOutputChannel = 3
        self.VoltageOutputGENERALonErrorCallback(VoltageOutputChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        self.MostRecentDutyCycleDict = dict([("VoltageOutputsList_EnabledState", self.VoltageOutputsList_EnabledState),
                                             ("VoltageOutputsList_Voltage", self.VoltageOutputsList_Voltage),
                                             ("VoltageOutputsList_ErrorCallbackFiredFlag", self.VoltageOutputsList_ErrorCallbackFiredFlag),
                                             ("Time", self.CurrentTime_CalculatedFromMainThread)])

        return self.MostRecentDutyCycleDict
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_MainThread(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread - self.LastTime_CalculatedFromMainThread

            if self.DataStreamingDeltaT_CalculatedFromMainThread != 0.0:
                self.DataStreamingFrequency_CalculatedFromMainThread = 1.0/self.DataStreamingDeltaT_CalculatedFromMainThread

            self.LastTime_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_MainThread ERROR with Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber(self, min_val, max_val, test_val):

        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitTextEntryInput(self, min_val, max_val, test_val, TextEntryObject):

        test_val = float(test_val)  # MUST HAVE THIS LINE TO CATCH STRINGS PASSED INTO THE FUNCTION

        if test_val > max_val:
            test_val = max_val
        elif test_val < min_val:
            test_val = min_val
        else:
            test_val = test_val

        if TextEntryObject != "":
            if isinstance(TextEntryObject, list) == 1:  # Check if the input 'TextEntryObject' is a list or not
                TextEntryObject[0].set(str(test_val))  # Reset the text, overwriting the bad value that was entered.
            else:
                TextEntryObject.set(str(test_val))  # Reset the text, overwriting the bad value that was entered.

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetEnabledState(self, VoltageOutputChannel, EnabledStateToBeSet):

        if VoltageOutputChannel in [0, 1, 2, 3]:
            if EnabledStateToBeSet in [0, 1]:
                self.VoltageOutputsList_EnabledState_ToBeSet[VoltageOutputChannel] = EnabledStateToBeSet
                self.VoltageOutputsList_EnabledState_NeedsToBeChangedFlag[VoltageOutputChannel] = 1

            else:
                print("SetEnabledState ERROR: VoltageOutputChannel must be 0 or 1!")

        else:
            print("SetEnabledState ERROR: VoltageOutputChannel must be 0, 1, 2, or 3!")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetVoltage(self, VoltageOutputChannel, VoltageToBeSet):

        if VoltageOutputChannel in [0, 1, 2, 3]:
            VoltageToBeSet_Limited = self.LimitNumber(self.VoltageOutputsList_MinVoltage[VoltageOutputChannel], self.VoltageOutputsList_MaxVoltage[VoltageOutputChannel], VoltageToBeSet)
            self.VoltageOutputsList_Voltage_ToBeSet[VoltageOutputChannel] = VoltageToBeSet_Limited
            self.VoltageOutputsList_Voltage_NeedsToBeChangedFlag[VoltageOutputChannel] = 1
            self.VoltageOutputsList_Voltage_Entry_TextContentList_NeedsToBeUpdatedFlag[VoltageOutputChannel] = 1
        else:
            print("SetVoltage ERROR: VoltageOutputChannel must be 0, 1, 2, or 3!")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ########################################################################################################## unicorn
    def MainThread(self):

        self.MyPrint_WithoutLogFile("Started MainThread for PhidgetAnalog4Output1002_ReubenPython2and3Class object.")
        
        self.MainThread_still_running_flag = 1



        ###############################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ###############################################
            self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()
            ###############################################

            ###############################################
            if self.ToggleVoltageToMeasureMaxFrequencyFlag == 1:

                if self.ToggleVoltageToMeasureMaxFrequency_ToggleState == 1:
                    self.ToggleVoltageToMeasureMaxFrequency_ToggleState = -1
                else:
                    self.ToggleVoltageToMeasureMaxFrequency_ToggleState = 1

                for VoltageOutputChannel in range(0, 4):
                    self.SetVoltage(VoltageOutputChannel, 5.0*self.ToggleVoltageToMeasureMaxFrequency_ToggleState)

            ###############################################

            ###############################################
            for VoltageOutputChannel in range(0, 4):

                if self.VoltageOutputsList_EnabledState_NeedsToBeChangedFlag[VoltageOutputChannel] == 1:

                    self.VoltageOutputsList_PhidgetsVoltageOutputObjects[VoltageOutputChannel].setEnabled(self.VoltageOutputsList_EnabledState_ToBeSet[VoltageOutputChannel])

                    #################
                    self.VoltageOutputsList_EnabledState[VoltageOutputChannel] = self.VoltageOutputsList_PhidgetsVoltageOutputObjects[VoltageOutputChannel].getEnabled()
                    if self.VoltageOutputsList_EnabledState[VoltageOutputChannel] == self.VoltageOutputsList_EnabledState_ToBeSet[VoltageOutputChannel]:
                        self.VoltageOutputsList_EnabledState_NeedsToBeChangedFlag[VoltageOutputChannel] = 0
                    #################
                        
            ###############################################

            ###############################################
            for VoltageOutputChannel in range(0, 4):

                if self.VoltageOutputsList_Voltage_NeedsToBeChangedFlag[VoltageOutputChannel] == 1:

                    self.VoltageOutputsList_PhidgetsVoltageOutputObjects[VoltageOutputChannel].setVoltage(self.VoltageOutputsList_Voltage_ToBeSet[VoltageOutputChannel])

                    #################
                    if self.ReadActualVoltageAfterSettingNewValueFlag == 1:
                        #print("ReadActualVoltageAfterSettingNewValueFlag")
                        self.VoltageOutputsList_Voltage[VoltageOutputChannel] = self.VoltageOutputsList_PhidgetsVoltageOutputObjects[VoltageOutputChannel].getVoltage()
                        if self.VoltageOutputsList_Voltage[VoltageOutputChannel] == self.VoltageOutputsList_Voltage_ToBeSet[VoltageOutputChannel]:
                            self.VoltageOutputsList_Voltage_NeedsToBeChangedFlag[VoltageOutputChannel] = 0
                    else:
                        self.VoltageOutputsList_Voltage_NeedsToBeChangedFlag[VoltageOutputChannel] = 0
                    #################
                        
            ###############################################

            ############################################### USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
            ###############################################
            ###############################################
            self.UpdateFrequencyCalculation_MainThread()

            if self.MainThread_TimeToSleepEachLoop > 0.0:
                time.sleep(self.MainThread_TimeToSleepEachLoop)

            ###############################################
            ###############################################
            ###############################################

        ###############################################

        ###############################################
        for VoltageOutputChannel in range(0, 4):
            self.VoltageOutputsList_PhidgetsVoltageOutputObjects[VoltageOutputChannel].close()
        ###############################################

        self.MyPrint_WithoutLogFile("Finished MainThread for PhidgetAnalog4Output1002_ReubenPython2and3Class object.")
        
        self.MainThread_still_running_flag = 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for PhidgetAnalog4Output1002_ReubenPython2and3Class object")

        self.EXIT_PROGRAM_FLAG = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartGUI(self, GuiParent=None):

        GUI_Thread_ThreadingObject = threading.Thread(target=self.GUI_Thread, args=(GuiParent,))
        GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self, parent=None):

        print("Starting the GUI_Thread for PhidgetAnalog4Output1002_ReubenPython2and3Class object.")

        ###################################################
        if parent == None:  #This class object owns root and must handle it properly
            self.root = Tk()
            self.parent = self.root

            ################################################### SET THE DEFAULT FONT FOR ALL WIDGETS CREATED AFTTER/BELOW THIS CALL
            default_font = tkFont.nametofont("TkDefaultFont")
            default_font.configure(size=8)
            self.root.option_add("*Font", default_font)
            ###################################################

        else:
            self.root = parent
            self.parent = parent
        ###################################################

        ###################################################
        self.myFrame = Frame(self.root)

        if self.UseBorderAroundThisGuiObjectFlag == 1:
            self.myFrame["borderwidth"] = 2
            self.myFrame["relief"] = "ridge"

        self.myFrame.grid(row = self.GUI_ROW,
                          column = self.GUI_COLUMN,
                          padx = self.GUI_PADX,
                          pady = self.GUI_PADY,
                          rowspan = self.GUI_ROWSPAN,
                          columnspan= self.GUI_COLUMNSPAN)
        ###################################################

        ###################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        self.TkinterScaleWidth = 10
        self.TkinterScaleLength = 250
        ###################################################

        #################################################
        self.device_info_label = Label(self.myFrame, text="Device Info", width=30) #, font=("Helvetica", 16)

        self.device_info_label["text"] = self.NameToDisplay_UserSet + \
                                         "\nDevice Name: " + self.DetectedDeviceName + \
                                         "\nDevice Serial Number: " + str(self.DetectedDeviceSerialNumber) + \
                                         "\nDevice Version: " + str(self.DetectedDeviceVersion)

        self.device_info_label.grid(row=0, column=0, padx=5, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        self.VoltageOutputs_Label = Label(self.myFrame, text="VoltageOutputs_Label", width=70)
        self.VoltageOutputs_Label.grid(row=0, column=1, padx=5, pady=1, columnspan=1, rowspan=10)
        #################################################
        
        #################################################

        self.VoltageOutputButtonsFrame = Frame(self.myFrame)

        #if self.UseBorderAroundThisGuiObjectFlag == 1:
        #    self.myFrame["borderwidth"] = 2
        #    self.myFrame["relief"] = "ridge"

        self.VoltageOutputButtonsFrame.grid(row = 1, column = 0, padx = 1, pady = 1, rowspan = 1, columnspan = 1)
        #################################################

        #################################################
        self.VoltageOutputsList_EnabledState_ButtonObjects = []
        for VoltageOutputChannel in range(0, 4):
            self.VoltageOutputsList_EnabledState_ButtonObjects.append(Button(self.VoltageOutputButtonsFrame, text="Voltage Enabled " + str(VoltageOutputChannel), state="normal", width=20, command=lambda i=VoltageOutputChannel: self.VoltageOutputsList_EnabledState_ButtonObjectsResponse(i)))
            self.VoltageOutputsList_EnabledState_ButtonObjects[VoltageOutputChannel].grid(row=VoltageOutputChannel, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        #################################################

        ###################################################
        self.VoltageOutputsList_Voltage_Entry_TextContentList_NeedsToBeUpdatedFlag = [0]*4
        #self.VoltageOutputsList_Voltage_Entry_TextContentList = []*4
        self.VoltageOutputsList_Voltage_Entry_TextContentList = list()

        self.VoltageOutputsList_Voltage_Entry_TextInputBoxList = list()
        for VoltageOutputChannel in range(0, 4):
            self.VoltageOutputsList_Voltage_Entry_TextContentList.append(StringVar())
            #self.VoltageOutputsList_Voltage_Entry_TextContentList.insert(int(VoltageOutputChannel), StringVar())
            self.VoltageOutputsList_Voltage_Entry_TextInputBoxList.append(Entry(self.VoltageOutputButtonsFrame,
                                                font=("Helvetica", int(8)),
                                                state="normal",
                                                width=20,
                                                textvariable=self.VoltageOutputsList_Voltage_Entry_TextContentList[VoltageOutputChannel],
                                                justify='center'))

            self.VoltageOutputsList_Voltage_Entry_TextContentList[VoltageOutputChannel].set(self.VoltageOutputsList_Voltage[VoltageOutputChannel])
            self.VoltageOutputsList_Voltage_Entry_TextInputBoxList[VoltageOutputChannel].grid(row=VoltageOutputChannel, column=1, padx=0, pady=0, columnspan=1, rowspan=1)
            print("GUI VoltageOutputChannel: " + str(VoltageOutputChannel))
            self.VoltageOutputsList_Voltage_Entry_TextInputBoxList[VoltageOutputChannel].bind('<Return>', lambda event, channel = VoltageOutputChannel: self.VoltageOutputsList_Voltage_Entry_EventResponse(event, channel))
        ###################################################

        ########################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=75)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=0, column=2, padx=1, pady=1, columnspan=1, rowspan=10)
        ########################

        ########################
        if self.RootIsOwnedExternallyFlag == 0: #This class object owns root and must handle it properly
            self.root.protocol("WM_DELETE_WINDOW", self.ExitProgram_Callback)

            self.root.after(self.GUI_RootAfterCallbackInterval_Milliseconds, self.GUI_update_clock)
            self.GUI_ready_to_be_updated_flag = 1
            self.root.mainloop()
        else:
            self.GUI_ready_to_be_updated_flag = 1
        ########################

        ########################
        if self.RootIsOwnedExternallyFlag == 0: #This class object owns root and must handle it properly
            self.root.quit()  # Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
            self.root.destroy()  # Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
        ########################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:

            #######################################################
            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                #######################################################
                try:
                    #######################################################
                    for VoltageOutputChannel in range(0, 4):
                        if self.VoltageOutputsList_EnabledState[VoltageOutputChannel] == 1:
                            self.VoltageOutputsList_EnabledState_ButtonObjects[VoltageOutputChannel]["bg"] = self.TKinter_LightGreenColor
                        elif self.VoltageOutputsList_EnabledState[VoltageOutputChannel] == 0:
                            self.VoltageOutputsList_EnabledState_ButtonObjects[VoltageOutputChannel]["bg"] = self.TKinter_LightRedColor
                        else:
                            self.VoltageOutputsList_EnabledState_ButtonObjects[VoltageOutputChannel]["bg"] = self.TKinter_DefaultGrayColor
                    #######################################################

                    #######################################################
                    self.VoltageOutputs_Label["text"] = "\nEnabledStates: " + str(self.VoltageOutputsList_EnabledState) + \
                                                "\nVoltages: " + str(self.VoltageOutputsList_Voltage) + \
                                                "\nTime: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromMainThread, 0, 3) + \
                                                "\nMain Thread Frequency: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromMainThread, 0, 3)
                    #######################################################

                    #######################################################
                    for VoltageOutputChannel in range(0, 4):
                        if self.VoltageOutputsList_Voltage_Entry_TextContentList_NeedsToBeUpdatedFlag[VoltageOutputChannel] == 1:
                            self.VoltageOutputsList_Voltage_Entry_TextContentList[VoltageOutputChannel].set(self.VoltageOutputsList_Voltage[VoltageOutputChannel])
                            self.VoltageOutputsList_Voltage_Entry_TextContentList_NeedsToBeUpdatedFlag[VoltageOutputChannel] = 0
                    #######################################################

                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("PhidgetAnalog4Output1002_ReubenPython2and3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
                    traceback.print_exc()
                #######################################################
                #######################################################

                #######################################################
                #######################################################
                if self.RootIsOwnedExternallyFlag == 0:  # This class object owns root and must handle it properly
                    self.root.after(self.GUI_RootAfterCallbackInterval_Milliseconds, self.GUI_update_clock)
                #######################################################
                #######################################################

            #######################################################
            #######################################################
            #######################################################

        #######################################################
        #######################################################
        #######################################################
        #######################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageOutputsList_Voltage_Entry_EventResponse(self, event, channel):

        try:
            EntryInput_TEMP = self.VoltageOutputsList_Voltage_Entry_TextContentList[channel].get()
            EntryInput_TEMP_LIMITED = self.LimitTextEntryInput(self.VoltageOutputsList_MinVoltage[channel], self.VoltageOutputsList_MaxVoltage[channel], EntryInput_TEMP, self.VoltageOutputsList_Voltage_Entry_TextContentList[channel])

            self.VoltageOutputsList_Voltage_ToBeSet[channel] = EntryInput_TEMP_LIMITED
            self.VoltageOutputsList_Voltage_NeedsToBeChangedFlag[channel] = 1

            self.MyPrint_WithoutLogFile("VoltageOutputsList_Voltage_Entry_EventResponse, channel " + str(channel) + " entry input: " + str(EntryInput_TEMP_LIMITED))
        except:
            exceptions = sys.exc_info()[0]
            print("VoltageOutputsList_Voltage_Entry_EventResponse ERROR: Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def IsInputList(self, input, print_result_flag = 0):

        result = isinstance(input, list)

        if print_result_flag == 1:
            self.MyPrint_WithoutLogFile("IsInputList: " + str(result))

        return result
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers=4, number_of_decimal_places=3):
        IsListFlag = self.IsInputList(input)

        if IsListFlag == 0:
            float_number_list = [input]
        else:
            float_number_list = list(input)

        float_number_list_as_strings = []
        for element in float_number_list:
            try:
                element = float(element)
                prefix_string = "{:." + str(number_of_decimal_places) + "f}"
                element_as_string = prefix_string.format(element)
                float_number_list_as_strings.append(element_as_string)
            except:
                self.MyPrint_WithoutLogFile(self.TellWhichFileWereIn() + ": ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput ERROR: " + str(element) + " cannot be turned into a float")
                return -1

        StringToReturn = ""
        if IsListFlag == 0:
            StringToReturn = float_number_list_as_strings[0].zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
        else:
            StringToReturn = "["
            for index, StringElement in enumerate(float_number_list_as_strings):
                if float_number_list[index] >= 0:
                    StringElement = "+" + StringElement  # So that our strings always have either + or - signs to maintain the same string length

                StringElement = StringElement.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place

                if index != len(float_number_list_as_strings) - 1:
                    StringToReturn = StringToReturn + StringElement + ", "
                else:
                    StringToReturn = StringToReturn + StringElement + "]"

        return StringToReturn
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def VoltageOutputsList_EnabledState_ButtonObjectsResponse(self, VoltageOutputChannel):

        if self.VoltageOutputsList_EnabledState[VoltageOutputChannel] == 1:
            self.VoltageOutputsList_EnabledState_ToBeSet[VoltageOutputChannel] = 0
        else:
            self.VoltageOutputsList_EnabledState_ToBeSet[VoltageOutputChannel] = 1

        self.VoltageOutputsList_EnabledState_NeedsToBeChangedFlag[VoltageOutputChannel] = 1

        self.MyPrint_WithoutLogFile("VoltageOutputsList_EnabledState_ButtonObjectsResponse: Event fired for VoltageOutputChannel " + str(VoltageOutputChannel))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MyPrint_WithoutLogFile(self, input_string):

        input_string = str(input_string)

        if input_string != "":

            #input_string = input_string.replace("\n", "").replace("\r", "")

            ################################ Write to console
            # Some people said that print crashed for pyinstaller-built-applications and that sys.stdout.write fixed this.
            # http://stackoverflow.com/questions/13429924/pyinstaller-packaged-application-works-fine-in-console-mode-crashes-in-window-m
            if self.PrintToConsoleFlag == 1:
                sys.stdout.write(input_string + "\n")
            ################################

            ################################ Write to GUI
            self.PrintToGui_Label_TextInputHistory_List.append(self.PrintToGui_Label_TextInputHistory_List.pop(0)) #Shift the list
            self.PrintToGui_Label_TextInputHistory_List[-1] = str(input_string) #Add the latest value

            self.PrintToGui_Label_TextInput_Str = ""
            for Counter, Line in enumerate(self.PrintToGui_Label_TextInputHistory_List):
                self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + Line

                if Counter < len(self.PrintToGui_Label_TextInputHistory_List) - 1:
                    self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + "\n"
            ################################

    ##########################################################################################################
    ##########################################################################################################
