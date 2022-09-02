###########################

PhidgetAnalog4Output1002_ReubenPython2and3Class

Wrapper (including ability to hook to Tkinter GUI) to control Phidget Analog 4-Output (4 analog-out voltages @ 12 bit resolution) 1002 (non VINT).

From Phidgets' website:

"The PhidgetAnalog 4-Output Produces a voltage over -10V to +10V at a maximum of 20mA.
If this current is exceeded an error will be thrown to notify that the voltage may have dropped below the setpoint.
The voltage is produced with 12 bit resolution (4.8mV). The board is not isolated and all 4 channels share a common ground. All the power is supplied by via USB."

PhidgetAnalog 4-Output

ID: 1002_0B

https://www.phidgets.com/?tier=3&catid=2&pcid=1&prodid=1018

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision G, 08/29/2022

Verified working on: 

Python 2.7, 3.8.

Windows 8.1, 10 64-bit

Raspberry Pi Buster 

(no Mac testing yet)

*NOTE THAT YOU MUST INSTALL BOTH THE Phidget22 LIBRARY AS WELL AS THE PYTHON MODULE.*

###########################

########################### Python module installation instructions, all OS's

PhidgetAnalog4Output1002_ReubenPython2and3Class, ListOfModuleDependencies: ['future.builtins', 'Phidget22']

PhidgetAnalog4Output1002_ReubenPython2and3Class, ListOfModuleDependencies_TestProgram: ['MyPrint_ReubenPython2and3Class']

PhidgetAnalog4Output1002_ReubenPython2and3Class, ListOfModuleDependencies_NestedLayers: ['future.builtins']

PhidgetAnalog4Output1002_ReubenPython2and3Class, ListOfModuleDependencies_All: ['future.builtins', 'MyPrint_ReubenPython2and3Class', 'Phidget22']

https://pypi.org/project/Phidget22/#files

To install the Python module using pip:

pip install Phidget22       (with "sudo" if on Linux/Raspberry Pi)

To install the Python module from the downloaded .tar.gz file, enter downloaded folder and type "python setup.py install"

###########################

########################### Library/driver installation instructions, Windows

https://www.phidgets.com/docs/OS_-_Windows

###########################

########################### Library/driver installation instructions, Linux (other than Raspberry Pi)

https://www.phidgets.com/docs/OS_-_Linux#Quick_Downloads

###########################

########################### Library/driver installation instructions, Raspberry Pi (models 2 and above)

https://www.phidgets.com/education/learn/getting-started-kit-tutorial/install-libraries/

curl -fsSL https://www.phidgets.com/downloads/setup_linux | sudo -E bash -

sudo apt-get install -y libphidget22
 
###########################
