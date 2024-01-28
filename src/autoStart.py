import socket
from settings import Settings
from palWorldControl import isPalWorldProcessRunning, startServer
import logging
import threading
import traceback

sock = None
isBreak = False

# check PalWorld server port is available
def isPortAvailable(port):
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.bind(("localhost", port))
        test_socket.close()
        return True
    except OSError:
        return False


# open socket before listen
def openPalworldPortSocket():
    try:
        global sock, isBreak

        # close before open
        closePalworldPortSocket()
        
        isBreak = False
        palworldServerIP = Settings["palworldServerIP"]
        palworldServerPort = Settings["palworldServerPort"]
        
        logging.info(f"To detect attempts to connect to the PalWorld Server, open the port {palworldServerPort}.")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((palworldServerIP, palworldServerPort))
        return True
    except Exception as e:
        logging.error(f"Error from openPalworldPortSocket: {e}")
        logging.error(traceback.format_exc())
        isBreak = True
        return False


# close socket
def closePalworldPortSocket():
    global sock, isBreak
    isBreak = True
    try:
        if sock is None:
            return
        
        sock.close()
        sock = None
        return True
    except Exception as e:
        logging.error(f"Error from closePalworldPortSocket: {e}")
        logging.error(traceback.format_exc())
        sock = None
        return False


# listen from PalWorld server port
def listenPalworldAccessCore():
    palworldServerPort = Settings["palworldServerPort"]
    firstPacketPattern = Settings["firstPacketPattern"]

    if isPalWorldProcessRunning():
        return

    if not isPortAvailable(palworldServerPort):
        logging.error(f"Palworld process is not running, but cannot open port {palworldServerPort}")
        return
    
    if not openPalworldPortSocket():
        logging.error(f"Unable to open a socket to wait for the Palworld connection packet.")
        return

    logging.info("Detecting attempts to connect to the PalWorld Server.")

    while True:
        try:
            if isBreak:
                closePalworldPortSocket()
                break

            data, addr = sock.recvfrom(1024)
            hex_data = " ".join(format(byte, "02X") for byte in data)
            logging.info(f"[LISTEN_PALWORLD_PORT] {addr}: {hex_data}")

            if data.startswith(firstPacketPattern):
                logging.info("A packet corresponding to a connection attempt has been detected. Attempting to start the server.")
                startServer()
            else:
                print("Not the first packet.")
        except UnicodeDecodeError as e:
            print(f"Error decoding data from {addr}: {e}")

        break


def listenPalworldAccess():
    logging.info("Start listenPalworldAccess")

    thread = threading.Thread(target=listenPalworldAccessCore)
    thread.start()

    #TODO:If the server did not start successfully, reconnect the socket after a certain period of time.