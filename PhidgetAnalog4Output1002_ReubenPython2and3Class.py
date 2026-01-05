# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com,
www.reubotics.com

Apache 2 License
Software Revision H, 12/28/2025

Verified working on: Python 3.11/12/13 for Windows 10/11 64-bit and Raspberry Pi Bookworm (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

##########################################################################################################
##########################################################################################################

###########################################################
import ReubenGithubCodeModulePaths #Replaces the need to have "ReubenGithubCodeModulePaths.pth" within "C:\Anaconda3\Lib\site-packages".
ReubenGithubCodeModulePaths.Enable()
###########################################################

###########################################################
import os
import sys
import platform
import time
import datetime
import math
import collections
from copy import * #for deepcopy
import inspect #To enable 'TellWhichFileWereIn'
import queue as Queue
import threading
import traceback
###########################################################

###########################################################
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
###########################################################

###########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
###########################################################

###########################################################
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.VoltageOutput import *
###########################################################

##########################################################################################################
##########################################################################################################

class PhidgetAnalog4Output1002_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    #######################################################################################################################
    #######################################################################################################################
    def __init__(self, SetupDict): #Subclass the Tkinter Frame

        print("#################### PhidgetAnalog4Output1002_ReubenPython2and3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = -1
        self.EnableInternal_MyPrint_Flag = 0
        self.MainThread_still_running_flag = 0

        self.NumberOfVoltageOutputs = 4

        #########################################################
        self.CurrentTime_CalculatedFromMainThread = -11111.0
        self.StartingTime_CalculatedFromMainThread = -11111.0
        self.LastTime_CalculatedFromMainThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromMainThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromMainThread = -11111.0
        #########################################################

        #########################################################
        self.DetectedDeviceName = "default"
        self.DetectedDeviceID = "default"
        self.DetectedDeviceVersion = "default"
        self.DetectedDeviceSerialNumber = "default"
        #########################################################

        self.ToggleVoltageToMeasureMaxFrequency_ToggleState = -1 #-1 or 1, never 0

        self.VoltageOutputsList_PhidgetsVoltageOutputObjects = list()

        self.VoltageOutputsList_AttachedAndOpenFlag = [-1.0] * self.NumberOfVoltageOutputs
        self.VoltageOutputsList_ErrorCallbackFiredFlag = [-1.0] * self.NumberOfVoltageOutputs

        self.VoltageOutputsList_EnabledState = [-1] * self.NumberOfVoltageOutputs
        self.VoltageOutputsList_EnabledState_NeedsToBeChangedFlag = [1] * self.NumberOfVoltageOutputs
        self.VoltageOutputsList_EnabledState_ToBeSet = [0] * self.NumberOfVoltageOutputs

        self.VoltageOutputsList_Voltage = [-1] * self.NumberOfVoltageOutputs
        self.VoltageOutputsList_Voltage_NeedsToBeChangedFlag = [1]*self.NumberOfVoltageOutputs
        self.VoltageOutputsList_Voltage_ToBeSet = [0] * self.NumberOfVoltageOutputs
        self.VoltageOutputsList_Voltage_Entry_TextContentList_NeedsToBeUpdatedFlag = [0] * self.NumberOfVoltageOutputs

        self.VoltageOutputsList_ListOfOnAttachCallbackFunctionNames = [self.VoltageOutput0onAttachCallback, self.VoltageOutput1onAttachCallback, self.VoltageOutput2onAttachCallback, self.VoltageOutput3onAttachCallback]
        self.VoltageOutputsList_ListOfOnDetachCallbackFunctionNames = [self.VoltageOutput0onDetachCallback, self.VoltageOutput1onDetachCallback, self.VoltageOutput2onDetachCallback, self.VoltageOutput3onDetachCallback]
        self.VoltageOutputsList_ListOfOnErrorCallbackFunctionNames = [self.VoltageOutput0onErrorCallback, self.VoltageOutput1onErrorCallback, self.VoltageOutput2onErrorCallback, self.VoltageOutput3onErrorCallback]

        self.MostRecentDataDict = dict()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
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

        print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "GUIparametersDict" in SetupDict:
            self.GUIparametersDict = SetupDict["GUIparametersDict"]

            #########################################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################

            #########################################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################

            #########################################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################

            #########################################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################

            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################

            #########################################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################

            #########################################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################

            #########################################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################

            #########################################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################

            #########################################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 1.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################

            #########################################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 1.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################

            #########################################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            #########################################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))

        #print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: GUIparametersDict: " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DesiredSerialNumber" in SetupDict:
            try:
                self.DesiredSerialNumber = int(SetupDict["DesiredSerialNumber"])
            except:
                print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: ERROR, DesiredSerialNumber invalid.")
                return
        else:
            self.DesiredSerialNumber = -1
        
        print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: DesiredSerialNumber: " + str(self.DesiredSerialNumber))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in SetupDict:
            self.NameToDisplay_UserSet = str(SetupDict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: NameToDisplay_UserSet: " + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "WaitForAttached_TimeoutDuration_Milliseconds" in SetupDict:
            self.WaitForAttached_TimeoutDuration_Milliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("WaitForAttached_TimeoutDuration_Milliseconds", SetupDict["WaitForAttached_TimeoutDuration_Milliseconds"], 0.0, 60000.0))

        else:
            self.WaitForAttached_TimeoutDuration_Milliseconds = 5000

        print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: WaitForAttached_TimeoutDuration_Milliseconds: " + str(self.WaitForAttached_TimeoutDuration_Milliseconds))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "UsePhidgetsLoggingInternalToThisClassObjectFlag" in SetupDict:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UsePhidgetsLoggingInternalToThisClassObjectFlag", SetupDict["UsePhidgetsLoggingInternalToThisClassObjectFlag"])
        else:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = 1

        print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: UsePhidgetsLoggingInternalToThisClassObjectFlag: " + str(self.UsePhidgetsLoggingInternalToThisClassObjectFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "VoltageOutputsList_MinVoltage" in SetupDict:
            VoltageOutputsList_MinVoltage_TEMP = SetupDict["VoltageOutputsList_MinVoltage"]
            
            if self.IsInputList(VoltageOutputsList_MinVoltage_TEMP) == 1 and len(VoltageOutputsList_MinVoltage_TEMP) == self.NumberOfVoltageOutputs:
                self.VoltageOutputsList_MinVoltage = list()
                
                for VoltageOutputChannel, VoltageValue in enumerate(VoltageOutputsList_MinVoltage_TEMP):
                    MinVoltage = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VoltageOutputsList_MinVoltage, VoltageOutputChannel " + str(VoltageOutputChannel), VoltageValue, -10.0, 10.0)
                    self.VoltageOutputsList_MinVoltage.append(MinVoltage)
            else:
                print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: Error, 'VoltageOutputsList_MinVoltage' must be length " + str(self.NumberOfVoltageOutputs) +".")
                
        else:
            self.VoltageOutputsList_MinVoltage = [-10.0]*self.NumberOfVoltageOutputs

        print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: VoltageOutputsList_MinVoltage: " + str(self.VoltageOutputsList_MinVoltage))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "VoltageOutputsList_MaxVoltage" in SetupDict:
            VoltageOutputsList_MaxVoltage_TEMP = SetupDict["VoltageOutputsList_MaxVoltage"]
            
            if self.IsInputList(VoltageOutputsList_MaxVoltage_TEMP) == 1 and len(VoltageOutputsList_MaxVoltage_TEMP) == self.NumberOfVoltageOutputs:
                self.VoltageOutputsList_MaxVoltage = list()
                
                for VoltageOutputChannel, VoltageValue in enumerate(VoltageOutputsList_MaxVoltage_TEMP):
                    MaxVoltage = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VoltageOutputsList_MaxVoltage, VoltageOutputChannel " + str(VoltageOutputChannel), VoltageValue, -10.0, 10.0)
                    self.VoltageOutputsList_MaxVoltage.append(MaxVoltage)
            else:
                print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: Error, 'VoltageOutputsList_MaxVoltage' must be length " + str(self.NumberOfVoltageOutputs) +".")
                
        else:
            self.VoltageOutputsList_MaxVoltage = [-10.0]*self.NumberOfVoltageOutputs

        print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: VoltageOutputsList_MaxVoltage: " + str(self.VoltageOutputsList_MaxVoltage))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "MainThread_TimeToSleepEachLoop" in SetupDict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", SetupDict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.005

        print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ReadActualVoltageAfterSettingNewValueFlag" in SetupDict:
            self.ReadActualVoltageAfterSettingNewValueFlag = self.PassThrough0and1values_ExitProgramOtherwise("ReadActualVoltageAfterSettingNewValueFlag", SetupDict["ReadActualVoltageAfterSettingNewValueFlag"])
        else:
            self.ReadActualVoltageAfterSettingNewValueFlag = 1

        print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: ReadActualVoltageAfterSettingNewValueFlag: " + str(self.ReadActualVoltageAfterSettingNewValueFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ToggleVoltageToMeasureMaxFrequencyFlag" in SetupDict:
            self.ToggleVoltageToMeasureMaxFrequencyFlag = self.PassThrough0and1values_ExitProgramOtherwise("ToggleVoltageToMeasureMaxFrequencyFlag", SetupDict["ToggleVoltageToMeasureMaxFrequencyFlag"])
        else:
            self.ToggleVoltageToMeasureMaxFrequencyFlag = 1

        print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: ToggleVoltageToMeasureMaxFrequencyFlag: " + str(self.ToggleVoltageToMeasureMaxFrequencyFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:
            for VoltageOutputChannel in range(0, self.NumberOfVoltageOutputs):
                #########################################################
                self.VoltageOutputsList_PhidgetsVoltageOutputObjects.append(VoltageOutput())

                if self.DesiredSerialNumber != -1: #'-1' means we should open the device regardless os serial number.
                    self.VoltageOutputsList_PhidgetsVoltageOutputObjects[VoltageOutputChannel].setDeviceSerialNumber(self.DesiredSerialNumber)

                self.VoltageOutputsList_PhidgetsVoltageOutputObjects[VoltageOutputChannel].setChannel(VoltageOutputChannel)
                self.VoltageOutputsList_PhidgetsVoltageOutputObjects[VoltageOutputChannel].setOnAttachHandler(self.VoltageOutputsList_ListOfOnAttachCallbackFunctionNames[VoltageOutputChannel])
                self.VoltageOutputsList_PhidgetsVoltageOutputObjects[VoltageOutputChannel].setOnDetachHandler(self.VoltageOutputsList_ListOfOnDetachCallbackFunctionNames[VoltageOutputChannel])
                self.VoltageOutputsList_PhidgetsVoltageOutputObjects[VoltageOutputChannel].setOnErrorHandler(self.VoltageOutputsList_ListOfOnErrorCallbackFunctionNames[VoltageOutputChannel])
                self.VoltageOutputsList_PhidgetsVoltageOutputObjects[VoltageOutputChannel].openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
                #########################################################

            self.PhidgetsDeviceConnectedFlag = 1

        except PhidgetException as e:
            self.PhidgetsDeviceConnectedFlag = 0
            print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: Failed to attach, Phidget Exception %i: %s" % (e.code, e.details))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.PhidgetsDeviceConnectedFlag == 1:

            #########################################################
            if self.UsePhidgetsLoggingInternalToThisClassObjectFlag == 1:
                try:
                    Log.enable(LogLevel.PHIDGET_LOG_INFO, os.getcwd() + "\PhidgetAnalog4Output1002_ReubenPython2and3Class_PhidgetLog_INFO.txt")
                    print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: Enabled Phidget Logging.")
                except PhidgetException as e:
                    print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: Failed to enable Phidget Logging, Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceName = self.VoltageOutputsList_PhidgetsVoltageOutputObjects[0].getDeviceName()
                print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: DetectedDeviceName: " + self.DetectedDeviceName)

            except PhidgetException as e:
                print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: Failed to call 'getDeviceName', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceSerialNumber = self.VoltageOutputsList_PhidgetsVoltageOutputObjects[0].getDeviceSerialNumber()
                print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: DetectedDeviceSerialNumber: " + str(self.DetectedDeviceSerialNumber))

            except PhidgetException as e:
                print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: Failed to call 'getDeviceSerialNumber', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceID = self.VoltageOutputsList_PhidgetsVoltageOutputObjects[0].getDeviceID()
                print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: DetectedDeviceID: " + str(self.DetectedDeviceID))

            except PhidgetException as e:
                print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: Failed to call 'getDeviceID', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceVersion = self.VoltageOutputsList_PhidgetsVoltageOutputObjects[0].getDeviceVersion()
                print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: DetectedDeviceVersion: " + str(self.DetectedDeviceVersion))

            except PhidgetException as e:
                print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: Failed to call 'getDeviceVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceLibraryVersion = self.VoltageOutputsList_PhidgetsVoltageOutputObjects[0].getLibraryVersion()
                print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: DetectedDeviceLibraryVersion: " + str(self.DetectedDeviceLibraryVersion))

            except PhidgetException as e:
                print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: Failed to call 'getLibraryVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            if self.DesiredSerialNumber != -1: #'-1' means we should open the device regardless os serial number.
                if self.DetectedDeviceSerialNumber != self.DesiredSerialNumber:
                    print("PhidgetAnalog4Output1002_ReubenPython2and3Class __init__: The desired Serial Number (" + str(self.DesiredSerialNumber) + ") does not match the detected serial number (" + str(self.DetectedDeviceSerialNumber) + ").")
                    self.CloseAllVoltageOutputChannels()
                    time.sleep(0.25)
                    return
            #########################################################

            #########################################################
            self.MainThread_ThreadingObject = threading.Thread(target=self.MainThread, args=())
            self.MainThread_ThreadingObject.start()
            #########################################################

            #########################################################
            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
            #########################################################

        #########################################################
        #########################################################

    #######################################################################################################################
    #######################################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_IntOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = int(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_FloatOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = float(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber, ExitProgramIfFailureFlag=1):

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber must be a numerical value, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1.0:
                return InputNumber_ConvertedToFloat

            else:

                print("PassThrough0and1values_ExitProgramOtherwise Error. '" +
                      str(InputNameString) +
                      "' must be 0 or 1 (value was " +
                      str(InputNumber_ConvertedToFloat) +
                      ").")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()

                else:
                    return -1
                ##########################

            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue, ExitProgramIfFailureFlag=1):

        ##########################################################################################################
        ##########################################################################################################
        try:
            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat_Limited = self.LimitNumber_FloatOutputOnly(RangeMinValue, RangeMaxValue, InputNumber_ConvertedToFloat)

            if InputNumber_ConvertedToFloat_Limited != InputNumber_ConvertedToFloat:
                print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                      str(InputNameString) +
                      "' must be in the range [" +
                      str(RangeMinValue) +
                      ", " +
                      str(RangeMaxValue) +
                      "] (value was " +
                      str(InputNumber_ConvertedToFloat) + ")")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()
                else:
                    return -11111.0
                ##########################

            else:
                return InputNumber_ConvertedToFloat_Limited
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
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

        if self.EXIT_PROGRAM_FLAG == 0:

            return deepcopy(self.MostRecentDataDict) #deepcopy IS required as MostRecentDataDict contains lists.

        else:
            return dict() #So that we're not returning variables during the close-down process.
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
    def LimitTextEntryInput(self, min_val, max_val, test_val, TextEntryObject, NumberOfDecimalPlaces = 3):

        try:
            test_val = float(test_val)  # MUST HAVE THIS LINE TO CATCH STRINGS PASSED INTO THE FUNCTION

            if test_val > max_val:
                test_val = max_val
            elif test_val < min_val:
                test_val = min_val
            else:
                test_val = test_val

            if TextEntryObject != "":
                if isinstance(TextEntryObject, list) == 1:  # Check if the input 'TextEntryObject' is a list or not
                    TextEntryObject[0].set(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(test_val, 0, NumberOfDecimalPlaces))  # Reset the text, overwriting the bad value that was entered.
                else:
                    TextEntryObject.set(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(test_val, 0, NumberOfDecimalPlaces))  # Reset the text, overwriting the bad value that was entered.

            return test_val

        except:
            exceptions = sys.exc_info()[0]
            print("LimitTextEntryInput: Exceptions: %s" % exceptions)
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
    ##########################################################################################################
    ########################################################################################################## unicorn
    def MainThread(self):

        self.MyPrint_WithoutLogFile("Started MainThread for PhidgetAnalog4Output1002_ReubenPython2and3Class object.")
        
        self.MainThread_still_running_flag = 1

        self.StartingTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()

        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:
            try:

                ##########################################################################################################
                self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromMainThread
                ##########################################################################################################

                ##########################################################################################################
                if self.ToggleVoltageToMeasureMaxFrequencyFlag == 1:

                    if self.ToggleVoltageToMeasureMaxFrequency_ToggleState == 1:
                        self.ToggleVoltageToMeasureMaxFrequency_ToggleState = -1
                    else:
                        self.ToggleVoltageToMeasureMaxFrequency_ToggleState = 1

                    for VoltageOutputChannel in range(0, self.NumberOfVoltageOutputs):
                        self.SetVoltage(VoltageOutputChannel, 5.0*self.ToggleVoltageToMeasureMaxFrequency_ToggleState)

                ##########################################################################################################

                ##########################################################################################################
                for VoltageOutputChannel in range(0, self.NumberOfVoltageOutputs):

                    if self.VoltageOutputsList_EnabledState_NeedsToBeChangedFlag[VoltageOutputChannel] == 1:

                        self.VoltageOutputsList_PhidgetsVoltageOutputObjects[VoltageOutputChannel].setEnabled(self.VoltageOutputsList_EnabledState_ToBeSet[VoltageOutputChannel])

                        #################
                        self.VoltageOutputsList_EnabledState[VoltageOutputChannel] = self.VoltageOutputsList_PhidgetsVoltageOutputObjects[VoltageOutputChannel].getEnabled()
                        if self.VoltageOutputsList_EnabledState[VoltageOutputChannel] == self.VoltageOutputsList_EnabledState_ToBeSet[VoltageOutputChannel]:
                            self.VoltageOutputsList_EnabledState_NeedsToBeChangedFlag[VoltageOutputChannel] = 0
                        #################

                ##########################################################################################################

                ##########################################################################################################
                for VoltageOutputChannel in range(0, self.NumberOfVoltageOutputs):

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

                ##########################################################################################################

                ##########################################################################################################
                self.MostRecentDataDict = dict([("VoltageOutputsList_EnabledState", self.VoltageOutputsList_EnabledState),
                                                 ("VoltageOutputsList_Voltage", self.VoltageOutputsList_Voltage),
                                                 ("VoltageOutputsList_ErrorCallbackFiredFlag", self.VoltageOutputsList_ErrorCallbackFiredFlag),
                                                 ("Time", self.CurrentTime_CalculatedFromMainThread)])
                ##########################################################################################################

                ########################################################################################################## USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
                self.UpdateFrequencyCalculation_MainThread()

                if self.MainThread_TimeToSleepEachLoop > 0.0:
                    time.sleep(self.MainThread_TimeToSleepEachLoop)
                ##########################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                print("PhidgetAnalog4Output1002_ReubenPython2and3Class MainThread: Exceptions: %s" % exceptions)
                #traceback.print_exc()

        ##########################################################################################################
        ##########################################################################################################

        self.CloseAllVoltageOutputChannels()

        self.MyPrint_WithoutLogFile("Finished MainThread for PhidgetAnalog4Output1002_ReubenPython2and3Class object.")
        
        self.MainThread_still_running_flag = 0
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CloseAllVoltageOutputChannels(self):

        try:
            for VoltageOutputChannel in range(0, self.NumberOfVoltageOutputs):
                self.VoltageOutputsList_PhidgetsVoltageOutputObjects[VoltageOutputChannel].close()

        except PhidgetException as e:
            print("CloseAllVoltageOutputChannels, Phidget Exception %i: %s" % (e.code, e.details))

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
    def CreateGUIobjects(self, TkinterParent):

        print("PhidgetAnalog4Output1002_ReubenPython2and3Class, CreateGUIobjects event fired.")

        ###################################################
        ###################################################
        self.root = TkinterParent
        self.parent = TkinterParent
        ###################################################
        ###################################################

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
                          columnspan= self.GUI_COLUMNSPAN,
                          sticky = self.GUI_STICKY)
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        ###################################################
        ###################################################

        ###################################################
        #################################################
        self.DeviceInfo_Label = Label(self.myFrame, text="Device Info", width=30)

        self.DeviceInfo_Label["text"] = self.NameToDisplay_UserSet + \
                                         "\nDevice Name: " + self.DetectedDeviceName + \
                                         "\nDevice Serial Number: " + str(self.DetectedDeviceSerialNumber) + \
                                         "\nDevice Version: " + str(self.DetectedDeviceVersion)

        self.DeviceInfo_Label.grid(row=0, column=0, padx=5, pady=1, columnspan=1, rowspan=1)
        #################################################
        ###################################################

        ###################################################
        #################################################
        self.VoltageOutputs_Label = Label(self.myFrame, text="VoltageOutputs_Label", width=70)
        self.VoltageOutputs_Label.grid(row=0, column=1, padx=5, pady=1, columnspan=1, rowspan=1)
        #################################################
        ###################################################

        #################################################
        ###################################################
        self.VoltageOutputButtonsFrame = Frame(self.myFrame)
        self.VoltageOutputButtonsFrame.grid(row = 1, column = 0, padx = 1, pady = 1, rowspan = 1, columnspan = 1)
        #################################################
        ###################################################

        ###################################################
        #################################################
        self.VoltageOutputsList_EnabledState_ButtonObjects = []
        for VoltageOutputChannel in range(0, self.NumberOfVoltageOutputs):
            self.VoltageOutputsList_EnabledState_ButtonObjects.append(Button(self.VoltageOutputButtonsFrame, text="Voltage Enabled " + str(VoltageOutputChannel), state="normal", width=20, command=lambda i=VoltageOutputChannel: self.VoltageOutputsList_EnabledState_ButtonObjectsResponse(i)))
            self.VoltageOutputsList_EnabledState_ButtonObjects[VoltageOutputChannel].grid(row=VoltageOutputChannel, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        #################################################
        ###################################################

        ###################################################
        ###################################################
        self.VoltageOutputsList_Voltage_Entry_TextContentList = list()
        self.VoltageOutputsList_Voltage_Entry_TextInputBoxList = list()
        for VoltageOutputChannel in range(0, self.NumberOfVoltageOutputs):
            self.VoltageOutputsList_Voltage_Entry_TextContentList.append(StringVar())
            self.VoltageOutputsList_Voltage_Entry_TextInputBoxList.append(Entry(self.VoltageOutputButtonsFrame,
                                                font=("Helvetica", int(8)),
                                                state="normal",
                                                width=20,
                                                textvariable=self.VoltageOutputsList_Voltage_Entry_TextContentList[VoltageOutputChannel],
                                                justify='center'))

            self.VoltageOutputsList_Voltage_Entry_TextContentList[VoltageOutputChannel].set(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.VoltageOutputsList_Voltage[VoltageOutputChannel], 0, 3))
            self.VoltageOutputsList_Voltage_Entry_TextInputBoxList[VoltageOutputChannel].grid(row=VoltageOutputChannel, column=1, padx=0, pady=0, columnspan=1, rowspan=1)
            self.VoltageOutputsList_Voltage_Entry_TextInputBoxList[VoltageOutputChannel].bind('<Return>', lambda event, channel = VoltageOutputChannel: self.VoltageOutputsList_Voltage_Entry_EventResponse(event, channel))
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=150)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=2, column=0, padx=10, pady=10, columnspan=10, rowspan=10)
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.GUI_ready_to_be_updated_flag = 1
        ###################################################
        ###################################################

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
                    for VoltageOutputChannel in range(0, self.NumberOfVoltageOutputs):
                        if self.VoltageOutputsList_EnabledState[VoltageOutputChannel] == 1:
                            self.VoltageOutputsList_EnabledState_ButtonObjects[VoltageOutputChannel]["bg"] = self.TKinter_LightGreenColor
                        elif self.VoltageOutputsList_EnabledState[VoltageOutputChannel] == 0:
                            self.VoltageOutputsList_EnabledState_ButtonObjects[VoltageOutputChannel]["bg"] = self.TKinter_LightRedColor
                        else:
                            self.VoltageOutputsList_EnabledState_ButtonObjects[VoltageOutputChannel]["bg"] = self.TKinter_DefaultGrayColor
                    #######################################################

                    #######################################################
                    self.VoltageOutputs_Label["text"] = "\nEnabledStates: " + str(self.VoltageOutputsList_EnabledState) + \
                                                "\nVoltages: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.VoltageOutputsList_Voltage, 0, 3) + \
                                                "\nTime: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromMainThread, 0, 3) + \
                                                "\nMain Thread Frequency: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromMainThread, 0, 3)
                    #######################################################

                    #######################################################
                    for VoltageOutputChannel in range(0, self.NumberOfVoltageOutputs):
                        if self.VoltageOutputsList_Voltage_Entry_TextContentList_NeedsToBeUpdatedFlag[VoltageOutputChannel] == 1:
                            self.VoltageOutputsList_Voltage_Entry_TextContentList[VoltageOutputChannel].set(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.VoltageOutputsList_Voltage[VoltageOutputChannel], 0, 3))
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

            #self.MyPrint_WithoutLogFile("VoltageOutputsList_Voltage_Entry_EventResponse, channel " + str(channel) + " entry input: " + str(EntryInput_TEMP_LIMITED))
        except:
            exceptions = sys.exc_info()[0]
            print("VoltageOutputsList_Voltage_Entry_EventResponse ERROR: Exceptions: %s" % exceptions)
            traceback.print_exc()
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

        #self.MyPrint_WithoutLogFile("VoltageOutputsList_EnabledState_ButtonObjectsResponse: Event fired for VoltageOutputChannel " + str(VoltageOutputChannel))

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

    ##########################################################################################################
    ##########################################################################################################
    def IsInputList(self, InputToCheck):

        result = isinstance(InputToCheck, list)
        return result
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

        number_of_decimal_places = max(1, number_of_decimal_places) #Make sure we're above 1

        ListOfStringsToJoin = []

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if isinstance(input, str) == 1:
            ListOfStringsToJoin.append(input)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, int) == 1 or isinstance(input, float) == 1:
            element = float(input)
            prefix_string = "{:." + str(number_of_decimal_places) + "f}"
            element_as_string = prefix_string.format(element)

            ##########################################################################################################
            ##########################################################################################################
            if element >= 0:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
                element_as_string = "+" + element_as_string  # So that our strings always have either + or - signs to maintain the same string length
            else:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1 + 1)  # +1 for sign, +1 for decimal place
            ##########################################################################################################
            ##########################################################################################################

            ListOfStringsToJoin.append(element_as_string)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, list) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, tuple) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append("TUPLE" + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, dict) == 1:

            if len(input) > 0:
                for Key in input: #RECURSION
                    ListOfStringsToJoin.append(str(Key) + ": " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a dict()
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        else:
            ListOfStringsToJoin.append(str(input))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if len(ListOfStringsToJoin) > 1:

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            StringToReturn = ""
            for Index, StringToProcess in enumerate(ListOfStringsToJoin):

                ################################################
                if Index == 0: #The first element
                    if StringToProcess.find(":") != -1 and StringToProcess[0] != "{": #meaning that we're processing a dict()
                        StringToReturn = "{"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[0] != "(":  # meaning that we're processing a tuple
                        StringToReturn = "("
                    else:
                        StringToReturn = "["

                    StringToReturn = StringToReturn + StringToProcess.replace("TUPLE","") + ", "
                ################################################

                ################################################
                elif Index < len(ListOfStringsToJoin) - 1: #The middle elements
                    StringToReturn = StringToReturn + StringToProcess + ", "
                ################################################

                ################################################
                else: #The last element
                    StringToReturn = StringToReturn + StringToProcess

                    if StringToProcess.find(":") != -1 and StringToProcess[-1] != "}":  # meaning that we're processing a dict()
                        StringToReturn = StringToReturn + "}"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[-1] != ")":  # meaning that we're processing a tuple
                        StringToReturn = StringToReturn + ")"
                    else:
                        StringToReturn = StringToReturn + "]"

                ################################################

            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

        elif len(ListOfStringsToJoin) == 1:
            StringToReturn = ListOfStringsToJoin[0]

        else:
            StringToReturn = ListOfStringsToJoin

        return StringToReturn
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

