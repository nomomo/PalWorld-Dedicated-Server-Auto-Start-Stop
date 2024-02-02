import json
import logging
import traceback

class settings:
    def __init__(self):
        # PalWorld
        self.palworldExePath = r"C:\steamcmd\steamapps\common\PalServer\PalServer.exe"
        self.palworldServerIP = "0.0.0.0"
        self.palworldServerPort = 8211
        self.palworldRCONHost = "localhost"
        self.palworldRCONPort = 25575
        self.palworldAdminPassword = "topSecretPassword"

        # Web Server
        self.useWebServer = True
        self.webServerHost = "localhost"
        self.webServerPort = 8212
        self.showAction = True
        self.showServerOnBtn = True
        self.showServerOffBtn = True
        self.showUpdateServerStatusBtn = True
        self.showServerIPAddress = True

        # Auto Start
        self.useAutoStart = True

        # Auto Stop
        self.useAutoStop = True
        self.ServerAutoStopSeconds = 600.0
        self.ServerAutoStopCheckInterval = 10.0

        # Advanced
        self.palworldMainProcessName = "PalServer-Win64-Test-Cmd.exe"
        self.firstPacketPattern = b'\x09\x08\x00'   # 09 08 00 04 98 5D F6 7E

Settings = settings();


def readSettings(file_path):
    try:
        global Settings
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            
            # Update settings in the instance if keys exist in the JSON file
            for key, value in json_data.items():
                if hasattr(Settings, key):
                    setattr(Settings, key, value)
            print("Settings loaded successfully.")
    except FileNotFoundError:
        logging.info(f"Error: File {file_path} not found.")
    except json.JSONDecodeError:
        logging.warn(f"Error: Invalid JSON format in {file_path}.")
    except Exception as e:
        logging.error(f"Error from readSettings: {e}")
        logging.error(traceback.format_exc())


def updateSettings(options):
    try:
        global Settings
        # Update settings in the instance if keys exist in the options dictionary
        for key, value in options.items():
            if hasattr(Settings, key):
                setattr(Settings, key, value)
        logging.info("Settings updated successfully.")
    except Exception as e:
        logging.error(f"Error from updateSettings: {e}")
        logging.error(traceback.format_exc())
