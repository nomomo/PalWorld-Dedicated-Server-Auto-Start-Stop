<div align="center">

[![ko](https://img.shields.io/badge/lang-ko--kr-green.svg)](https://github.com/nomomo/PalWorld-Dedicated-Server-Auto-Start-Stop/blob/main/README.ko.md)

Translated by ChatGPT

</div>

# PalWorld-Dedicated-Server-Auto-Start-Stop

- This is a simple Python script for automatically turning on and off the Palworld Windows server.
- When the PalWorld server is not running, it automatically starts when a user attempts to connect.
- When the PalWorld server is running and there are no online users, it automatically shuts down after a certain period.
- Provides an Admin Page through the Webserver to turn the server on and off.

## Limitations

- This tool is a script created for personal use and is currently in development. It is not well-coded and may have many bugs.
- Only supports Windows environment.
- Tested only on small-scale servers.
- Be cautious as unknown security issues may arise.

## How to Use

If you want to try it out, follow the steps below. As of January 28, 2024, it works correctly with PalWorld v0.1.3.0.

### Prerequisites

To use RCON, set `RCONEnabled=True` in the `PalWorldSettings.ini` file.

This file is created when the server is first run and is located at `{PalServerPath}\PalServer\Pal\Saved\Config\WindowsServer\PalWorldSettings.ini`. If the file is empty, paste the contents of `{PalServerPath}\PalServer\DefaultPalWorldSettings.ini` into `PalWorldSettings.ini`.

### Download

Download the code from this repository using the "Download ZIP" feature or execute the following command:

```Python
git clone https://github.com/nomomo/PalWorld-Dedicated-Server-Auto-Start-Stop.git
```

### Install Dependencies

This script has been tested with Python 3.10. To install dependencies, execute the following command in the command prompt:

```Python
pip install flask psutil schedule git+https://github.com/ttk1/py-rcon.git
```

### Modify setting.py File

Modify the `src\settings.json` file according to your server settings.

For the `palworldExePath`, enter the path to `{PalServerPath}\PalServer\PalServer.exe`.

```json
{
    # PalWorld
    "palworldExePath": "C:\\steamcmd\\steamapps\\common\\PalServer\\PalServer.exe", #PalWorld Server exe file
    "palworldServerIP": "0.0.0.0",          # PalWorld Server IP. This is used for "Auto Start". Use "0.0.0.0" to open to all. use "localhost"
    "palworldServerPort": 8211,             # PalWorld Server PublicPort in PalWorldSettings.ini. This is used for "Auto Start".
    "palworldRCONHost": "localhost",        # RCON host. use "0.0.0.0" to open to all. use "localhost".
    "palworldRCONPort": 25575,              # RCONPort in PalWorldSettings.ini. Default is 25575
    "palworldAdminPassword": "topSecretPassword",   # AdminPassword in PalWorldSettings.ini

    # Web Server
    "useWebServer": true,                   # Use simple admin page
    "webServerHost": "localhost",           # webserver hostname. use "0.0.0.0" to open to all. use "localhost"
    "webServerPort": 8212,                  # webserver port
    "showAction": true,                     # show action area
    "showServerOnBtn": true,                # show "Server On" button
    "showServerOffBtn": true,               # show "Server Off" button
    "showUpdateServerStatusBtn": true,      # show "Update Server Status" button
    "showServerIPAddress": true,            # show IP Address

    # Auto Start
    "useAutoStart": true,                   # when user try to access, start the server automatically

    # Auto Stop
    "useAutoStop": true,                    # if True && there is are no players online, server will automatically stop
    "ServerAutoStopSeconds": 600.0,         # the server will automatically stop after ServerAutoStopSeconds seconds.
    "ServerAutoStopCheckInterval": 10.0,    # AutoStop event is checked every ServerAutoStopCheckInterval seconds.
    "palworldMainProcessName": "PalServer-Win64-Test-Cmd.exe"    # don't change, if there is no problem
}
```

### Run main.py

Navigate to the `src` folder in the command prompt and execute the following command:

```Python
python main.py
```

The console window is automatically on and the log is printed. The log is written in the `app.log` file.

If `"useWebServer": True` is set in the configuration, check if the Admin Page is accessible. The default URL is `http://localhost:8212/`.

<img src="https://github.com/nomomo/PalWorld-Dedicated-Server-Auto-Start-Stop/blob/main/images/AdminPageSample.png?raw=true" width="300px">

## How does this script work?

### Automatic Server Start

1. When the PalWorld server is not running, it opens port 8211 to receive packets.
2. It waits for a packet starting with `\x09\x08\x00`.
3. Once the packet is received, it closes port 8211 and executes the file located at `palworldExePath` to start the server.

### Automatic Server Shutdown

1. It checks the number of players currently on the server through RCON (`ShowPlayers` command).
2. If the number of players is 0, it uses RCON to gracefully shut down the server with the `Shutdown` command.

## Future Works

Timing uncertain:

- Code cleanup
- Support for pip install
- Beautify the Admin page
- Automatically restart the server at regular intervals. Notify in advance through server messages before restarting.
- Auto backup
- IP Blacklist

## Change Logs

### 0.0.2 (2024-02-03)

- Changed to edit settings.json instead of settings.py file for settings
- Fixed an issue where UDT connections were terminated when random packets were input to the socket.

### 0.0.1 (2024-01-28)

- Initial commit

## License

MIT

## Dependencies

- [py-rcon](https://github.com/ttk1/py-rcon)
- [psutil](https://pypi.org/project/psutil/)
- [Schedule](https://pypi.org/project/schedule/)
- [Flask](https://pypi.org/project/Flask/)

## Happy??

<a href="https://www.buymeacoffee.com/nomomo" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-yellow.png" alt="Buy Me A Coffee" height="60"></a>
