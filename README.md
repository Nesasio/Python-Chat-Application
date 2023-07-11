# Python Chat Application
This is a simple LAN based chat application which allows multiple users to chat and share files over a local network.
For Graphical User Interface customtkinter library was used.

## Features
These are the major features of this application:
- Establishes connection between multiple clients over a local network
- Allows users to transfer files
- Login/signup for chat system
- Chat history is saved

## Requirements
The libraries required for the program are:
- customtkinter
- threading
- socket
- tkinter

## Using the Application
To run the application, one host workstation on a network needs to run `Server.py` and after the server is active, the
remanining workstations which are to be connected need to run `Client.py`. After that a login page will appear and user 
can either login or signup for the application and can join the chat.
