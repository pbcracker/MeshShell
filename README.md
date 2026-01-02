# MeshShell - Remote Command Executor via Mesh Network

## Overview

**MeshShell** is a Python script that interacts with the **Meshtastic** device to execute shell commands remotely via a mesh network. It listens for specific messages from the device and, when a command prefixed with "Master" is received, it runs the command on the system, logs the output, and sends feedback back to the device. This script allows for seamless remote execution of shell commands, suitable for use cases such as remote diagnostics, automation, and control over a mesh network.

The system is designed to interact with a **Meshtastic** device, which enables communication over long ranges using a mesh network.

## Features

- **Command Execution**: The script listens for messages with the prefix "Master" and executes the command found in the message.
- **Logging**: Logs all executed commands and their results with timestamps in a logfile.
- **Remote Feedback**: Sends success or error messages back to the device after a command is executed.
- **File Logging**: Saves command outputs to a separate file with the command name and timestamp.

## Requirements

Before using this script, ensure the following dependencies are installed:

- **Python 3.x**
- **Meshtastic Python Library** 

```
   +-------------------------+                 
   |                         |                 
   |   Linux Computer        |  
   |   +-------------------+ |                 
   |   |                   | |                 
   |   |  Running Script   | |                 
   |   |                   | |                 
   |   +-------------------+ |                 
   |   | Command Processor | |                 
   |   | (Subprocess)       | |                 
   |   +-------------------+ |                 
   |                         |                 
   +-------------------------+                 
            ^                                 
            |                                 
            | Serial                         
            |                                 
            |                                 
            v                                 
   +----------------------------+             
   |                            |             
   |  Meshtastic Radio (Receiver)|             
   |   +----------------------+  |             
   |   |                      |  |             
   |   |   Command Sender     |  |             
   |   |                      |  |             
   |   +----------------------+  |             
   |                            |             
   +----------------------------+             
            ^                                 
            |                                 
            | Wireless (LoRa Waves)          
            |                                 
            v                                 
                           +----------------------------+ 
                           |                            | 
                           |  Meshtastic Radio (Sender) | 
                           |   +----------------------+  | 
                           |   |                      |  | 
                           |   |  Sends Commands       |  | 
                           |   |                      |  | 
                           +----------------------------+  

```
