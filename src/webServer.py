import socket
from flask import Flask, render_template, request, jsonify
from settings import Settings
from palWorldControl import startServer, stopServer, updateCurrentServerInfo
from autoStop import stopServerVariables
import logging

IP = "Unknown"
PlayerNo = 0
app = Flask(__name__)

# Function to get the server IP address
def getServerIP():
    global IP
    try:
        IP = socket.gethostbyname(socket.gethostname())
        IP = IP + ":" + str(Settings.palworldServerPort)
    except Exception as e:
        logging.error(f"Error while getting server IP, {e}")
        IP ="unknown"
    return IP


# Route for the main page
@app.route("/")
def index():
    currentServerInfo = updateCurrentServerInfo()
    if Settings.showServerIPAddress:
        currentServerInfo["IPAddress"] = getServerIP()
    else:
        currentServerInfo["IPAddress"] = "Unknown"

    print("showAction", Settings.showAction)

    return render_template(
        "index.html",
        showAction=Settings.showAction,
        showServerOnBtn=Settings.showServerOnBtn,
        showServerOffBtn=Settings.showServerOffBtn,
        showUpdateServerStatusBtn=Settings.showUpdateServerStatusBtn,
        showServerIPAddress=Settings.showServerIPAddress,
        data=currentServerInfo,
        ServerAutoStopSeconds=round(Settings.ServerAutoStopSeconds),
        isRunningStopwatchToStopServer=round(stopServerVariables["isRunningStopwatchToStopServer"]),
        leftTimeToStopServer=round(stopServerVariables["leftTimeToStopServer"])
    )


# Route to handle server actions
@app.route("/action", methods=["POST"])
def webServerAction():
    action = request.form.get("action")

    currentServerInfo = updateCurrentServerInfo()

    if action == "startServer":
        startServer()
    elif action == "stopServer":
        stopServer(1)
    #elif action == "getStatus":
        # do nothing

    return jsonify(
        data=currentServerInfo,
        ServerAutoStopSeconds=round(Settings.ServerAutoStopSeconds),
        isRunningStopwatchToStopServer=round(stopServerVariables["isRunningStopwatchToStopServer"]),
        leftTimeToStopServer=round(stopServerVariables["leftTimeToStopServer"])
    )


def runWebServer():
    logging.info("Start webserver")
    app.run(host=Settings.webServerHost, port=Settings.webServerPort, debug=False)