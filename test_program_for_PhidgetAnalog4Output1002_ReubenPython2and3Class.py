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

#########################################################
import ReubenGithubCodeModulePaths #Replaces the need to have "ReubenGithubCodeModulePaths.pth" within "C:\Anaconda3\Lib\site-packages".
ReubenGithubCodeModulePaths.Enable()
#########################################################

###########################################################
from MyPrint_ReubenPython2and3Class import *
from PhidgetAnalog4Output1002_ReubenPython2and3Class import *
###########################################################

###########################################################
import os
import sys
import platform
import time
import datetime
import threading
import collections
import math
import traceback
import keyboard
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

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
def GetLatestWaveformValue(CurrentTime, MinValue, MaxValue, Period, WaveformTypeString="Sine"):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            ##########################################################################################################
            OutputValue = 0.0
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            WaveformTypeString_ListOfAcceptableValues = ["Sine", "Cosine", "Triangular", "Square"]

            if WaveformTypeString not in WaveformTypeString_ListOfAcceptableValues:
                print("GetLatestWaveformValue: Error, WaveformTypeString must be in " + str(WaveformTypeString_ListOfAcceptableValues))
                return -11111.0
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            if WaveformTypeString == "Sine":

                TimeGain = math.pi/Period
                OutputValue = (MaxValue + MinValue)/2.0 + 0.5*abs(MaxValue - MinValue)*math.sin(TimeGain*CurrentTime)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Cosine":

                TimeGain = math.pi/Period
                OutputValue = (MaxValue + MinValue)/2.0 + 0.5*abs(MaxValue - MinValue)*math.cos(TimeGain*CurrentTime)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Triangular":
                TriangularInput_TimeGain = 1.0
                TriangularInput_MinValue = -5
                TriangularInput_MaxValue = 5.0
                TriangularInput_PeriodInSeconds = 2.0

                #TriangularInput_Height0toPeak = abs(TriangularInput_MaxValue - TriangularInput_MinValue)
                #TriangularInput_CalculatedValue_1 = abs((TriangularInput_TimeGain*CurrentTime_CalculatedFromMainThread % PeriodicInput_PeriodInSeconds) - TriangularInput_Height0toPeak) + TriangularInput_MinValue

                A = abs(MaxValue - MinValue)
                P = Period

                #https://stackoverflow.com/questions/1073606/is-there-a-one-line-function-that-generates-a-triangle-wave
                OutputValue = (A / (P / 2)) * ((P / 2) - abs(CurrentTime % (2 * (P / 2)) - P / 2)) + MinValue
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Square":

                TimeGain = math.pi/Period
                MeanValue = (MaxValue + MinValue)/2.0
                SinusoidalValue =  MeanValue + 0.5*abs(MaxValue - MinValue)*math.sin(TimeGain*CurrentTime)

                if SinusoidalValue >= MeanValue:
                    OutputValue = MaxValue
                else:
                    OutputValue = MinValue
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            else:
                OutputValue = 0.0
            ##########################################################################################################
            ##########################################################################################################

            return OutputValue

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("GetLatestWaveformValue: Exceptions: %s" % exceptions)
            #return -11111.0
            traceback.print_exc()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################

###########################################################################################################
##########################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_GUI_FLAG

    global PhidgetAnalog4Output1002_ReubenPython2and3ClassObject
    global PhidgetAnalog4Output1002_OPEN_FLAG
    global SHOW_IN_GUI_PhidgetAnalog4Output1002_FLAG

    global MyPrint_Object
    global MyPrint_OPEN_FLAG
    global SHOW_IN_GUI_MyPrint_FLAG

    if USE_GUI_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################

            #########################################################
            if PhidgetAnalog4Output1002_OPEN_FLAG == 1 and SHOW_IN_GUI_PhidgetAnalog4Output1002_FLAG == 1:
                PhidgetAnalog4Output1002_ReubenPython2and3ClassObject.GUI_update_clock()
            #########################################################

            #########################################################
            if MyPrint_OPEN_FLAG == 1 and SHOW_IN_GUI_MyPrint_FLAG == 1:
                MyPrint_Object.GUI_update_clock()
            #########################################################

            root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
        #########################################################
        #########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback(OptionalArugment = 0):
    global EXIT_PROGRAM_FLAG

    print("ExitProgram_Callback event fired!")

    EXIT_PROGRAM_FLAG = 1
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_Thread():
    global root
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_TABS_IN_GUI_FLAG

    global PhidgetAnalog4Output1002_ReubenPython2and3ClassObject
    global PhidgetAnalog4Output1002_OPEN_FLAG

    global MyPrint_Object
    global MyPrint_OPEN_FLAG

    ################################################# KEY GUI LINE
    #################################################
    root = Tk()

    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.title("test_program_for_PhidgetAnalog4Output1002_ReubenPython2and3Class")
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos, root_Ypos)) # set the dimensions of the screen and where it is placed
    #################################################
    #################################################

    #################################################
    #################################################
    global TabControlObject
    global Tab_MainControls
    global Tab_PhidgetAnalog4Output1002
    global Tab_MyPrint

    if USE_TABS_IN_GUI_FLAG == 1:
        #################################################
        TabControlObject = ttk.Notebook(root)

        Tab_PhidgetAnalog4Output1002 = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_PhidgetAnalog4Output1002, text='   PhidgetAnalog4Output1002   ')

        Tab_MainControls = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MainControls, text='   Main Controls   ')

        Tab_MyPrint = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MyPrint, text='   MyPrint Terminal   ')

        TabControlObject.pack(expand=1, fill="both")  # CANNOT MIX PACK AND GRID IN THE SAME FRAME/TAB, SO ALL .GRID'S MUST BE CONTAINED WITHIN THEIR OWN FRAME/TAB.

        ############# #Set the tab header font
        TabStyle = ttk.Style()
        TabStyle.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
        #############

        #################################################
    else:
        #################################################
        Tab_MainControls = root
        Tab_PhidgetAnalog4Output1002 = root
        Tab_MyPrint = root
        #################################################

    #################################################
    #################################################

    #################################################
    #################################################
    if PhidgetAnalog4Output1002_OPEN_FLAG == 1:
        PhidgetAnalog4Output1002_ReubenPython2and3ClassObject.CreateGUIobjects(TkinterParent=Tab_PhidgetAnalog4Output1002)
    #################################################
    #################################################

    #################################################
    #################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_Object.CreateGUIobjects(TkinterParent=Tab_MyPrint)
    #################################################
    #################################################

    ################################################# THIS BLOCK MUST COME 2ND-TO-LAST IN def GUI_Thread() IF USING TABS.
    #################################################
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    #################################################
    #################################################

    #################################################
    #################################################
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################
    #################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global my_platform

    if platform.system() == "Linux":

        if "raspberrypi" in platform.uname():  # os.uname() doesn't work in windows
            my_platform = "pi"
        else:
            my_platform = "linux"

    elif platform.system() == "Windows":
        my_platform = "windows"

    elif platform.system() == "Darwin":
        my_platform = "mac"

    else:
        my_platform = "other"

    print("The OS platform is: " + my_platform)
    #################################################
    #################################################

    #################################################
    #################################################
    global USE_GUI_FLAG
    USE_GUI_FLAG = 1

    global USE_TABS_IN_GUI_FLAG
    USE_TABS_IN_GUI_FLAG = 1

    global USE_PhidgetAnalog4Output1002_FLAG
    USE_PhidgetAnalog4Output1002_FLAG = 1

    global USE_MyPrint_FLAG
    USE_MyPrint_FLAG = 1

    global USE_KEYBOARD_FLAG
    USE_KEYBOARD_FLAG = 1

    global USE_PeriodicInput_FLAG
    USE_PeriodicInput_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global SHOW_IN_GUI_PhidgetAnalog4Output1002_FLAG
    SHOW_IN_GUI_PhidgetAnalog4Output1002_FLAG = 1

    global SHOW_IN_GUI_MyPrint_FLAG
    SHOW_IN_GUI_MyPrint_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global GUI_ROW_PhidgetAnalog4Output1002
    global GUI_COLUMN_PhidgetAnalog4Output1002
    global GUI_PADX_PhidgetAnalog4Output1002
    global GUI_PADY_PhidgetAnalog4Output1002
    global GUI_ROWSPAN_PhidgetAnalog4Output1002
    global GUI_COLUMNSPAN_PhidgetAnalog4Output1002
    GUI_ROW_PhidgetAnalog4Output1002 = 1

    GUI_COLUMN_PhidgetAnalog4Output1002 = 0
    GUI_PADX_PhidgetAnalog4Output1002 = 1
    GUI_PADY_PhidgetAnalog4Output1002 = 1
    GUI_ROWSPAN_PhidgetAnalog4Output1002 = 1
    GUI_COLUMNSPAN_PhidgetAnalog4Output1002 = 1

    global GUI_ROW_MyPrint
    global GUI_COLUMN_MyPrint
    global GUI_PADX_MyPrint
    global GUI_PADY_MyPrint
    global GUI_ROWSPAN_MyPrint
    global GUI_COLUMNSPAN_MyPrint
    GUI_ROW_MyPrint = 2

    GUI_COLUMN_MyPrint = 0
    GUI_PADX_MyPrint = 1
    GUI_PADY_MyPrint = 1
    GUI_ROWSPAN_MyPrint = 1
    GUI_COLUMNSPAN_MyPrint = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    global CurrentTime_MainLoopThread
    CurrentTime_MainLoopThread = -11111.0

    global StartingTime_MainLoopThread
    StartingTime_MainLoopThread = -11111.0

    global root

    global root_Xpos
    root_Xpos = 900

    global root_Ypos
    root_Ypos = 0

    global root_width
    root_width = 1920 - root_Xpos

    global root_height
    root_height = 1020 - root_Ypos

    global TabControlObject
    global Tab_MainControls
    global Tab_PhidgetAnalog4Output1002
    global Tab_MyPrint

    global GUI_RootAfterCallbackInterval_Milliseconds
    GUI_RootAfterCallbackInterval_Milliseconds = 30

    global PeriodicInput_AcceptableValues
    PeriodicInput_AcceptableValues = ["GUI", "Sine", "Cosine", "Triangular", "Square"]

    global PeriodicInput_Type_1
    PeriodicInput_Type_1 = "Triangular"

    global PeriodicInput_MinValue_1
    PeriodicInput_MinValue_1 = -3.0

    global PeriodicInput_MaxValue_1
    PeriodicInput_MaxValue_1 = 3.0

    global PeriodicInput_Period_1
    PeriodicInput_Period_1 = 1.0

    global PeriodicInput_CalculatedValue_1
    PeriodicInput_CalculatedValue_1 = 0.0
    #################################################
    #################################################

    #################################################
    #################################################
    global PhidgetAnalog4Output1002_ReubenPython2and3ClassObject

    global PhidgetAnalog4Output1002_OPEN_FLAG
    PhidgetAnalog4Output1002_OPEN_FLAG = -1

    global PhidgetAnalog4Output1002_MostRecentDict
    PhidgetAnalog4Output1002_MostRecentDict = dict()

    global PhidgetAnalog4Output1002_MostRecentDict_VoltageOutputsList_EnabledState
    PhidgetAnalog4Output1002_MostRecentDict_VoltageOutputsList_EnabledState = [-1]*4

    global PhidgetAnalog4Output1002_MostRecentDict_VoltageOutputsList_Voltage
    PhidgetAnalog4Output1002_MostRecentDict_VoltageOutputsList_Voltage = [-1]*4

    global PhidgetAnalog4Output1002_MostRecentDict_VoltageOutputsList_ErrorCallbackFiredFlag
    PhidgetAnalog4Output1002_MostRecentDict_VoltageOutputsList_ErrorCallbackFiredFlag = [-1]*4

    global PhidgetAnalog4Output1002_MostRecentDict_Time
    PhidgetAnalog4Output1002_MostRecentDict_Time = -11111.0
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPrint_Object

    global MyPrint_OPEN_FLAG
    MyPrint_OPEN_FLAG = -1
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global PhidgetAnalog4Output1002_ReubenPython2and3ClassObject_GUIparametersDict
    PhidgetAnalog4Output1002_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_PhidgetAnalog4Output1002_FLAG),
                                                                                    ("EnableInternal_MyPrint_Flag", 0),
                                                                                    ("NumberOfPrintLines", 10),
                                                                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                                    ("GUI_ROW", GUI_ROW_PhidgetAnalog4Output1002),
                                                                                    ("GUI_COLUMN", GUI_COLUMN_PhidgetAnalog4Output1002),
                                                                                    ("GUI_PADX", GUI_PADX_PhidgetAnalog4Output1002),
                                                                                    ("GUI_PADY", GUI_PADY_PhidgetAnalog4Output1002),
                                                                                    ("GUI_ROWSPAN", GUI_ROWSPAN_PhidgetAnalog4Output1002),
                                                                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_PhidgetAnalog4Output1002)])

    global PhidgetAnalog4Output1002_ReubenPython2and3ClassObject_SetupDict
    PhidgetAnalog4Output1002_ReubenPython2and3ClassObject_SetupDict = dict([("GUIparametersDict", PhidgetAnalog4Output1002_ReubenPython2and3ClassObject_GUIparametersDict),
                                                                            ("DesiredSerialNumber", -1), #-1 MEANS ANY SN, CHANGE THIS TO MATCH YOUR UNIQUE SERIAL NUMBER
                                                                            ("WaitForAttached_TimeoutDuration_Milliseconds", 5000),
                                                                            ("NameToDisplay_UserSet", "Reuben's Test Analog 4-output 1002"),
                                                                            ("UsePhidgetsLoggingInternalToThisClassObjectFlag", 1),
                                                                            ("VoltageOutputsList_MinVoltage", [-4.0, -3.0, -2.0, -1.0]),
                                                                            ("VoltageOutputsList_MaxVoltage", [4.0, 3.0, 2.0, 1.0]),
                                                                            ("MainThread_TimeToSleepEachLoop", 0.001),
                                                                            ("ReadActualVoltageAfterSettingNewValueFlag", 1),
                                                                            ("ToggleVoltageToMeasureMaxFrequencyFlag", 0)])

    if USE_PhidgetAnalog4Output1002_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            PhidgetAnalog4Output1002_ReubenPython2and3ClassObject = PhidgetAnalog4Output1002_ReubenPython2and3Class(PhidgetAnalog4Output1002_ReubenPython2and3ClassObject_SetupDict)
            PhidgetAnalog4Output1002_OPEN_FLAG = PhidgetAnalog4Output1002_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

            #################################################
            if PhidgetAnalog4Output1002_OPEN_FLAG == 1:
                PhidgetAnalog4Output1002_ReubenPython2and3ClassObject.SetEnabledState(0, 1)
                PhidgetAnalog4Output1002_ReubenPython2and3ClassObject.SetEnabledState(1, 1)
                PhidgetAnalog4Output1002_ReubenPython2and3ClassObject.SetEnabledState(2, 1)
                PhidgetAnalog4Output1002_ReubenPython2and3ClassObject.SetEnabledState(3, 1)
            #################################################

        except:
            exceptions = sys.exc_info()[0]
            print("PhidgetAnalog4Output1002_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions, 0)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_PhidgetAnalog4Output1002_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if PhidgetAnalog4Output1002_OPEN_FLAG != 1:
                print("Failed to open PhidgetAnalog4Output1002_ReubenPython2and3ClassObject_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global MyPrint_Object_GUIparametersDict
    MyPrint_Object_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_MyPrint_FLAG),
                                            ("UseBorderAroundThisGuiObjectFlag", 0),
                                            ("GUI_ROW", GUI_ROW_MyPrint),
                                            ("GUI_COLUMN", GUI_COLUMN_MyPrint),
                                            ("GUI_PADX", GUI_PADX_MyPrint),
                                            ("GUI_PADY", GUI_PADY_MyPrint),
                                            ("GUI_ROWSPAN", GUI_ROWSPAN_MyPrint),
                                            ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_MyPrint)])

    global MyPrint_Object_SetupDict
    MyPrint_Object_SetupDict = dict([("NumberOfPrintLines", 10),
                                    ("WidthOfPrintingLabel", 200),
                                    ("PrintToConsoleFlag", 1),
                                    ("LogFileNameFullPath", os.path.join(os.getcwd(), "TestLog.txt")),
                                    ("GUIparametersDict", MyPrint_Object_GUIparametersDict)])

    if USE_MyPrint_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            MyPrint_Object = MyPrint_ReubenPython2and3Class(MyPrint_Object_SetupDict)
            MyPrint_OPEN_FLAG = MyPrint_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPrint_Object __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPrint_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPrint_OPEN_FLAG != 1:
                print("Failed to open MyPrint_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if USE_KEYBOARD_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        keyboard.on_press_key("esc", ExitProgram_Callback)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## KEY GUI LINE
    ##########################################################################################################
    ##########################################################################################################
    if USE_GUI_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        print("Starting GUI thread...")
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread, daemon=True) #Daemon=True means that the GUI thread is destroyed automatically when the main thread is destroyed
        GUI_Thread_ThreadingObject.start()
    else:
        root = None
        Tab_MainControls = None
        Tab_PhidgetAnalog4Output1002 = None
        Tab_MyPrint = None
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    print("Starting main loop 'test_program_for_PhidgetAnalog4Output1002_ReubenPython2and3Class.")
    StartingTime_MainLoopThread = getPreciseSecondsTimeStampString()

    while(EXIT_PROGRAM_FLAG == 0):

        ###################################################
        ###################################################
        ###################################################
        CurrentTime_MainLoopThread = getPreciseSecondsTimeStampString() - StartingTime_MainLoopThread
        ###################################################
        ###################################################
        ###################################################

        ################################################### GET's
        ###################################################
        ###################################################
        if PhidgetAnalog4Output1002_OPEN_FLAG == 1:

            PhidgetAnalog4Output1002_MostRecentDict = PhidgetAnalog4Output1002_ReubenPython2and3ClassObject.GetMostRecentDataDict()

            if "Time" in PhidgetAnalog4Output1002_MostRecentDict:
                PhidgetAnalog4Output1002_MostRecentDict_VoltageOutputsList_EnabledState = PhidgetAnalog4Output1002_MostRecentDict["VoltageOutputsList_EnabledState"]
                PhidgetAnalog4Output1002_MostRecentDict_VoltageOutputsList_Voltage = PhidgetAnalog4Output1002_MostRecentDict["VoltageOutputsList_Voltage"]
                PhidgetAnalog4Output1002_MostRecentDict_VoltageOutputsList_ErrorCallbackFiredFlag = PhidgetAnalog4Output1002_MostRecentDict["VoltageOutputsList_ErrorCallbackFiredFlag"]
                PhidgetAnalog4Output1002_MostRecentDict_Time = PhidgetAnalog4Output1002_MostRecentDict["Time"]

                #print("PhidgetAnalog4Output1002_MostRecentDict_VoltageOutputsList_EnabledState: " + str(PhidgetAnalog4Output1002_MostRecentDict_VoltageOutputsList_EnabledState))
        ###################################################
        ###################################################
        ###################################################

        ################################################### SET's
        ###################################################
        ###################################################
        if PhidgetAnalog4Output1002_OPEN_FLAG == 1:

            ###################################################
            ###################################################
            if USE_PeriodicInput_FLAG == 1:

                ####################################################
                PeriodicInput_CalculatedValue_1 = GetLatestWaveformValue(CurrentTime_MainLoopThread,
                                                                    PeriodicInput_MinValue_1,
                                                                    PeriodicInput_MaxValue_1,
                                                                    PeriodicInput_Period_1,
                                                                    PeriodicInput_Type_1)
                ###################################################

                ###################################################
                PhidgetAnalog4Output1002_ReubenPython2and3ClassObject.SetVoltage(0, PeriodicInput_CalculatedValue_1)
                ###################################################

            ###################################################
            ###################################################

        ###################################################
        ###################################################
        ###################################################

        time.sleep(0.001)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## THIS IS THE EXIT ROUTINE!
    ##########################################################################################################
    ##########################################################################################################
    print("Exiting main program 'test_program_for_PhidgetAnalog4Output1002_ReubenPython2and3Class.")

    #################################################
    if PhidgetAnalog4Output1002_OPEN_FLAG == 1:
        PhidgetAnalog4Output1002_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_Object.ExitProgram_Callback()
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################