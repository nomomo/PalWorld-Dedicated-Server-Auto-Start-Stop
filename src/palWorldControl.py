import psutil
import subprocess
from rcon import Console
import logging
import time
import threading
from settings import Settings
import traceback

currentServerInfo = {
    "running": False,
    "playerCount": 0,
    "players": []
}
isPalWorldServerStarting = False
ServerStartingCoolTime = 5  # second
lastServerStartedTime = 0
ServerStoppingCoolTime = 5  # second
lastServerStoppedTime = 0


triggeredTimeCheckStoppedEvent = -1    # reference time when stop event is triggered
isTriggeredCheckStoppedEvent = False   # true if stop event is running

def isPalWorldProcessRunning():
    ProcName = Settings["palworldMainProcessName"]
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == ProcName:
            return True
    return False

# Function to send RCON command
def sendRCONCommand(command):
    try:
        console = Console(host=Settings["palworldRCONHost"], port=Settings["palworldRCONPort"], password=Settings["palworldAdminPassword"])
        response = console.command(command)
        logging.info(f"[PALWORLD_RCON]: {str(response)}")
        console.close()
        return response
    except Exception as e:
        logging.error(f"Error from sendRCONCommand. command={command}")
        logging.error(traceback.format_exc())
        return None

def startServer():
    from autoStart import closePalworldPortSocket

    global isPalWorldServerStarting, lastServerStartedTime, ServerStartingCoolTime, lastServerStoppedTime, ServerStoppingCoolTime
    logging.info("The server start has been triggered.")
    palworldExePath = Settings["palworldExePath"]
    currentTime = time.time()

    if isPalWorldProcessRunning():
        logging.error("The attempt to start the Palworld server was made, but it is already running.")
        return False
    
    # filter 1
    if isPalWorldServerStarting:
        logging.warn("Palworld Server is already starting.")
        return False
    
    # filter 2: start cooltime
    if currentTime - lastServerStartedTime < ServerStartingCoolTime:
        logging.warn("Tried to start the server too quickly multiple times. This attempt will be ignored.")
        return False
    
    # filter 3: stop cooltime
    if currentTime - lastServerStoppedTime < ServerStoppingCoolTime:
        logging.warn("You attempted to restart the server too quickly shortly after trying to stop it. This attempt will be ignored.")
        return False
    
    # filter 4: isStopEventRunning
    if isStopEventRunning():
        logging.warn(f"Stop event is running. starting server is ignored")
        return
    
    # close socket if opened
    closePalworldPortSocket()

    returnVal = True

    # start server exe
    try:
        isPalWorldServerStarting = True
        subprocess.run(palworldExePath, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred while executing the Palworld executable file : {e}")
        returnVal = False
    finally:
        isPalWorldServerStarting = False
        lastServerStartedTime = time.time()

    return returnVal

# terminate process with 
def terminateProcess(processName):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == processName:
            pid = process.info['pid']
            try:
                process = psutil.Process(pid)
                process.terminate()
                print(f"Process {processName} with PID {pid} terminated.")
            except psutil.NoSuchProcess as e:
                print(f"Error: {e}")
            return
        

# Check if the PalWorld processor has been terminated, and start listenPalworldAccess
def checkIsStoppedPalworldProcessCore(timeout=60):
    from autoStart import listenPalworldAccess

    global isTriggeredCheckStoppedEvent, triggeredTimeCheckStoppedEvent
    #isTriggeredCheckStoppedEvent = True
    triggeredTimeCheckStoppedEvent = time.time()
    while True:
        if not isPalWorldProcessRunning():
            logging.info("PalWorld Process termination confirmed")
            time.sleep(1)
            listenPalworldAccess()
            break

        currentTime = time.time()
        if(currentTime - triggeredTimeCheckStoppedEvent > timeout):
            break
        
        time.sleep(1)
    isTriggeredCheckStoppedEvent = False

def isStopEventRunning():
    return isTriggeredCheckStoppedEvent

# stop server
def stopServer(delaySeconds, force=False):
    global lastServerStoppedTime, ServerStoppingCoolTime, isTriggeredCheckStoppedEvent
    logging.info("The server shutdown has been triggered.")

    if not isTriggeredCheckStoppedEvent:
        isTriggeredCheckStoppedEvent = True
        thread = threading.Thread(target=checkIsStoppedPalworldProcessCore)
        thread.start()

    if force:
        # not tested. delay ignored
        terminateProcess(Settings["palworldMainProcessName"])
    else:    
        # filter 1
        if not isPalWorldProcessRunning():
            logging.error("The attempt to stop the Palworld server was made, but it is not running.")
            return
        
        # filter 2: stop cooltime
        currentTime = time.time()
        if currentTime - lastServerStoppedTime < ServerStoppingCoolTime:
            logging.warn("You attempted to restart the server too quickly shortly after trying to stop it. This attempt will be ignored.")
            return

        if delaySeconds < 1.0:
            delaySeconds = 1.0
        sendRCONCommand(f"Shutdown {delaySeconds} Server is shutting down")
    
    lastServerStoppedTime = time.time()


# Function to get players information
def updateCurrentServerInfo():
    global currentServerInfo
    try:
        currentTime = time.time()
        if not isPalWorldProcessRunning() or isTriggeredCheckStoppedEvent or (currentTime - lastServerStoppedTime < ServerStoppingCoolTime):
            #logging.info("Tried to update server information, but the server is not running.")
            currentServerInfo["running"] = False
            currentServerInfo["playerCount"] = 0
            currentServerInfo["players"] = []
            return currentServerInfo

        currentServerInfo["running"] = True

        # get player count
        ShowPlayers = sendRCONCommand("ShowPlayers")
        SplitText = ShowPlayers.splitlines()
        currentServerInfo["playerCount"] = len(ShowPlayers.splitlines()) - 1
        
        # get player name
        if currentServerInfo["playerCount"] >= 1:
            currentServerInfo["players"] = []
            for i in range(currentServerInfo["playerCount"]):
                currentServerInfo["players"].append(SplitText[i + 1].split(','))
        else:
            currentServerInfo["players"] = []

        return currentServerInfo
    
    except Exception as e:
        logging.error(f"Error from updateCurrentServerInfo, {e}")
        logging.error(traceback.format_exc())
        return None
    


def getServerStatus():
    if not isPalWorldProcessRunning():
        return False
    
