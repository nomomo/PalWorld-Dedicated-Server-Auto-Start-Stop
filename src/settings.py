import json

Settings = {
    # PalWorld
    "palworldExePath": r"C:\steamcmd\steamapps\common\PalServer\PalServer.exe", #PalWorld Server exe file
    "palworldServerIP": "0.0.0.0",          # PalWorld Server IP. This is used for "Auto Start". use "0.0.0.0" to open to all. use "localhost" for testing.
    "palworldServerPort": 8211,             # PalWorld Server PublicPort. This is used for "Auto Start".
    "palworldRCONHost": "localhost",        # RCON host. use "0.0.0.0" to open to all. use "localhost" for testing.
    "palworldRCONPort": 25575,              # RCON Post. default is 25575
    "palworldAdminPassword": "topSecretPassword",   # AdminPassword

    # Web Server
    "useWebServer": True,                   # Use simple admin page
    "webServerHost": "localhost",           # webserver hostname. use "0.0.0.0" to open to all. use "localhost" for testing.
    "webServerPort": 8212,                  # webserver port
    "showAction": True,                     # show action area
    "showServerOnBtn": True,                # show "Server On" button
    "showServerOffBtn": True,               # show "Server Off" button
    "showUpdateServerStatusBtn": True,      # show "Update Server Status" button
    "showServerIPAddress": True,            # show IP Address
    
    # Auto Start
    "useAutoStart": True,                   # when user try to access, start the server automatically

    # Auto Stop
    "useAutoStop": True,                    # if True && there is are no players online, server will automatically stop
    "ServerAutoStopSeconds": 600.0,         # the server will automatically stop after ServerAutoStopSeconds seconds.
    "ServerAutoStopCheckInterval": 10.0,    # AutoStop event is checked every ServerAutoStopCheckInterval seconds.

    # Advanced
    "palworldMainProcessName": "PalServer-Win64-Test-Cmd.exe",    # don't change, if there is no problem
    "firstPacketPattern": b'\x09\x08\x00\x04\x40\x84\x92\x34\x01'
}
