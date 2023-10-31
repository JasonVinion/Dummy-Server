# Dummy Server Control Application

This application offers a GUI control panel to manage a Flask-based dummy server. Users can start, stop, check connections, and terminate connections to the server. It also provides a feature to toggle between dark and light themes.

## Quick Start:
To quickly get started, you can simply use the provided executable:

1. **Download**:
   - Download the `dummy_server.exe` from the repository.

2. **Run**:
   - Double-click on the `dummy_server.exe` to launch the application.
   - Use the GUI buttons to control the server and view its status.

## For Developers and Advanced Users:

If you wish to access, edit, or use the raw Python file:

1. **Access the Source**:
   - Navigate to the `Source Code` folder in the repository.
   - Find the `dummy_server.py` file which contains the source code for the application.

2. **Edit and Use**:
   - Ensure you have Python installed on your machine.
   - Install the required libraries:
     ```bash
     pip install Flask PyQt5 psutil requests
     ```
   - Open `dummy_server.py` in your preferred code editor for modifications.
   - To run the script, use the command:
     ```bash
     python dummy_server.py
     ```

## Features:

1. **Start/Stop Server**:
   - Launch the server at `http://127.0.0.1:5000`.
   - Gracefully shut down the server.

2. **Check Connections**:
   - Display IPs currently connected to the server.

3. **Terminate Connections**:
   - Forcefully close all established connections to the server.

4. **Dark Mode**:
   - A feature to switch between dark and light themes for the application interface.

## Overview:

The program is built using Flask for the server backend and PyQt5 for the graphical interface. It uses threading to ensure the server runs without blocking the GUI operations. Additionally, it utilizes the `psutil` library to manage network connections and the `requests` library for HTTP requests.

For in-depth details, code documentation, and further modifications, refer directly to the comments within the `dummy_server.py` source file.

Total:   [![HitCount](https://hits.dwyl.com/JasonVinion/Dummy-Server.svg?style=flat)](http://hits.dwyl.com/JasonVinion/Dummy-Server)

Unique:   [![HitCount](https://hits.dwyl.com/JasonVinion/Dummy-Server.svg?style=flat&show=unique)](http://hits.dwyl.com/JasonVinion/Dummy-Server)
