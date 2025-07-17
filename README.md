# OBD Adapter for Assetto Corsa

A Python application that bridges Assetto Corsa racing simulator with the Freematics OBD-II Emulator to provide realistic OBD data simulation for testing purposes.
This adapter was tested with a Freematics ONE+ to pars received data.

## Overview
The Freematics OBD-II Emulator is the smallest OBD emulator available on the market. It supports KWP2000, CAN Bus, ISO 9141-2, and J1850 protocols, and provides a 16-pin female OBD-II port, identical to those available on modern vehicles.
This allows to test simulated states of a car throughout the live-update of the vehicle state on the emulator, through `pyserial` communication.

## Hardware Requirements

- **Freematics OBD-II Emulator**
- **Power Supply**: 12V, 1A adapter
- **Communication**: USB Type-B cable connected to a PC

## Software Integration

Freematics provides a GUI software called **Freematics Emulator GUI** for device usage and communication. However, this software only allows:
- Protocol selection for emulation
- VIN selection
- DTC selection  
- Modification of simulated values for one PID at a time

Since Freematics also provides a command set for device control via serial communication using ASCII encoding, we developed a custom Python application that controls the emulation more realistically by sequentially changing the values of all PIDs of interest.

## Python Application Features

The **obd_adapter** application was created to control the Freematics OBD-II Emulator state. The application:

- Accesses the simulated vehicle state from Assetto Corsa
- Reads real-time vehicle data
- Maps the data to corresponding PIDs on the emulator via ASCII commands
- Provides a graphical widget within the Assetto Corsa interface for real-time monitoring

### Technical Implementation

- **Serial Communication**: Uses `pyserial` module for sending commands to the emulator
- **GUI Integration**: Utilizes all available Assetto Corsa modules for widget creation and vehicle state reading
- **Threading**: Implements multi-threading to separate visual updates from serial command transmission
  - Main thread: Updates information display in the application widget
  - Secondary daemon thread: Sends values to the OBD emulator

The threading approach was necessary as serial command transmission proved more time-consuming than initially expected.

## Installation & Usage

### Setup
1. Place the `obd_adapter` folder in the `...\apps\python` directory of your Assetto Corsa installation
2. Enable the application in the simulator's configuration menu by checking it as active in the available mods list
3. Ensure the OBD emulator is connected to the PC before starting the driving session

### Operation
1. Start Assetto Corsa and enter a driving session
2. Press the "Drive" button to get in the vehicle
3. Once on track, move the cursor to the right edge of the window
4. A column will appear allowing you to insert the obd_adapter widget
5. Use drag-and-drop to position the widget as desired
6. If configuration is successful, the widget will display "OBD: Connected" and show real-time updated values

## Dependencies

- Python with `pyserial` module
- Assetto Corsa racing simulator
- Freematics OBD-II Emulator
