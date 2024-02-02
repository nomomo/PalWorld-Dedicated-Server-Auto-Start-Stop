import logging
import traceback
import schedule
import time
import threading
from settings import Settings
from palWorldControl import isPalWorldProcessRunning, stopServer, updateCurrentServerInfo, isStopEventRunning

stopServerVariables = {
    "stopEventTriggeredTime": 1.0E+100,
    "isRunningStopwatchToStopServer": False,
    "leftTimeToStopServer": -1
}

# check server stop every minute if there is no players
def checkEventStopServerCore(callback):
    try:
        global stopServerVariables
        
        #logging.info("Checking if the conditions for stop server are met")

        # filter 1
        if not isPalWorldProcessRunning():
            #logging.info("The PalWorld server is not running, so the stop server event cannot be triggered.")
            stopServerVariables["isRunningStopwatchToStopServer"] = False
            return

        # filter 2
        if isStopEventRunning():
            logging.info(f"Stop event is running. checkEventStopServerCore ignored")
            return        
        
        # filter 2: player count
        currentServerInfo = updateCurrentServerInfo()
        if currentServerInfo is None:
            logging.error("An error occurred while updating the current server, and as a result, the stop server event cannot be triggered.")
            stopServerVariables["isRunningStopwatchToStopServer"] = False
            return
        playerCount = currentServerInfo["playerCount"]
        if playerCount > 0:
            stopServerVariables["isRunningStopwatchToStopServer"] = False
            return
        
        # check time
        currentTime = time.time()
        if not stopServerVariables["isRunningStopwatchToStopServer"]:
            stopServerVariables["stopEventTriggeredTime"] = time.time()     # save triggered time
            stopServerVariables["isRunningStopwatchToStopServer"] = True    # save flag

        ServerAutoStopSeconds = Settings.ServerAutoStopSeconds
        passedTime = currentTime - stopServerVariables["stopEventTriggeredTime"]
        if passedTime >= ServerAutoStopSeconds:
            logging.info("The server stop conditions are met, attempting to stop the server.")
            logging.info(f"passedTime = {passedTime}")
            stopServer(1)
            stopServerVariables["stopEventTriggeredTime"] = time.time() # to prevent call stopServer multiple times
            stopServerVariables["leftTimeToStopServer"] = 0.0
        else:
            stopServerVariables["leftTimeToStopServer"] = ServerAutoStopSeconds - passedTime
            logging.info(f"The server will automatically stop after {stopServerVariables['leftTimeToStopServer']} seconds.")

    except Exception as e:
        logging.error(f"Error from checkEventStopServerCore: {e}")
        logging.error(traceback.format_exc())
        return None

def runSchedule():
    ServerAutoStopCheckInterval = Settings.ServerAutoStopCheckInterval
    while True:
        schedule.run_pending()
        time.sleep(ServerAutoStopCheckInterval * 0.1)


def checkEventStopServer():
    global stopServerVariables

    logging.info("Start checkEventStopServer")

    # manually start once
    checkEventStopServerCore(None)

    ServerAutoStopCheckInterval = Settings.ServerAutoStopCheckInterval
    schedule.every(ServerAutoStopCheckInterval).seconds.do(checkEventStopServerCore, callback=None)

    thread = threading.Thread(target=runSchedule)
    thread.start()