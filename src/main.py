from settings import Settings, readSettings
from webServer import runWebServer
from autoStart import listenPalworldAccess
from autoStop import checkEventStopServer
import threading
import logging
import traceback

if __name__ == '__main__':
    try:
        # Configure logging to write messages to the console and a file
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),  # Log to console
                logging.FileHandler('app.log')  # Log to a file
            ]
        )

        # read settings if settings.json exists
        readSettings("settings.json")

        if Settings.useAutoStart:
            listenPalworldAccess()

        if Settings.useAutoStop:
            checkEventStopServer()

        if Settings.useWebServer:
            runWebServer()

    except Exception as e:
        logging.error(f"Error from main routine: {e}")
        logging.error(traceback.format_exc())