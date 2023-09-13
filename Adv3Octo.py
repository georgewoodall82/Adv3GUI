#An OctoPrint Emulation API that recieves commands and sends them through Adv3Api

#Not finished, you can try it though.

import Adv3Api
import flask
import json

Adv3Api.Connect("192.168.1.5")

PORT = 8080

app = flask.Flask(__name__)

@app.post("/api/printer/command")
def printer_command():
    data = flask.request.json
    #Adv3Api.SendGCode(data["command"])
    #json can be command for one gcode command, or commands for a list of gcode commands
    if "command" in data:
        print(data["command"])
        Adv3Api.SendGCode(data["command"])
    elif "commands" in data:
        print(data["commands"])
        for command in data["commands"]:
            Adv3Api.SendGCode(command)
    else:
        return '', 400
    return '', 204

#return json
@app.get("/api/printer")
def printer():
    temperautres = Adv3Api.getTemperatures()
    sdstatus = Adv3Api.getSDPrintStatus()
    return json.dumps(
        {
            "temperature": 
            {
                "tool0": 
                {
                    "actual": temperautres['T0']['temp'],
                    "target": temperautres['T0']['target'],
                    "offset": 0
                },
                "bed":
                {
                    "actual": temperautres['B']['temp'],
                    "target": temperautres['B']['target'],
                    "offset": 0
                }
            },
            "sd":
            {
                "ready": sdstatus[0] == 0
            },
            "state":
            {
                "text": "Operational",
                "flags":
                {
                    "operational": True,
                    "paused": False,
                    "printing": sdstatus[0] != 0,
                    "cancelling": False,
                    "pausing": False,
                    "sdReady": sdstatus[0] == 0,
                    "error": False,
                    "ready": sdstatus[0] == 0,
                    "closedOrError": False
                }
            }
        }
    ), 200

@app.post("/api/printer/printhead")
def printer_printhead():
    data = dict(flask.request.json)
    if data['command'] == "jog":
        Adv3Api.jogPrinter(data.get('x', 0), data.get('y', 0), data.get('z', 0), data.get('absolute', False), data.get('speed', -1))
    elif data['command'] == "home":
        Adv3Api.SendGCode("G28")
    elif data['command'] == "feedrate":
        Adv3Api.SendGCode(f"M663 S{data['factor']}")
    return '', 204

@app.get("/api/printer/tool")
def printer_tool():
    temperatures = Adv3Api.getTemperatures()
    return json.dumps({"tool0": {"actual": temperatures['T0']['temp'], "target": temperatures['T0']['target'], "offset": 0}}), 200

@app.get("/api/printer/bed")
def printer_bed():
    temperatures = Adv3Api.getTemperatures()
    return json.dumps({"bed": {"actual": temperatures['B']['temp'], "target": temperatures['B']['target'], "offset": 0}}), 200

#file is recieved as an octet-stream, save it to a temp file with the name "uploadtemp.gcode"
@app.post("/api/files/<location>")
def upload_file(location):
    file = flask.request.files['file']
    printnow = flask.request.form.get("print")
    file.save("uploadtemp.gcode")
    fnsplit = file.filename.split(".")
    f1 = ".".join(fnsplit[0:-1])
    f2 = fnsplit[-1][0]
    shortname = f1[:35-len(f2)] + "." + f2
    print(shortname)
    Adv3Api.SendFile("uploadtemp.gcode", "lolol.gcode")
    if printnow:
        Adv3Api.PrintFile("lolol.gcode")
    return '', 201

@app.get("/api/version")
def version():
    return json.dumps({"api": "0.1", "server": "1.3.10", "text": "OctoPrint 1.3.10"})

@app.get("/api/settings")
def settings():
    return json.dumps({}), 200

@app.get("/api/printerprofiles")
def printerprofiles():
    return json.dumps({}), 200

@app.post("/api/login")
def login():
    return json.dumps({
        "name": "FlashForge",
        "active": True,
        "user": True,
        "admin": True,
        "apikey": "flashforge",
        "settings": {},
        "session": "flashforge",
        "is_external_client": False
        }), 200

@app.get("/api/job")
def job():
    printstatus = Adv3Api.getPrintStatus()
    sdstatus = Adv3Api.getSDPrintStatus()
    return json.dumps({
        "job": {
            "file": {
                "name": printstatus["CurrentFile"],
                "origin": "sdcard",
                "size": sdstatus[1],
                "date": 69420
            }
        }
    }), 200

@app.get("/api/currentuser")
def currentuser():
    return json.dumps({
        "name": "FlashForge",
        "active": True,
        "user": True,
        "admin": True,
        "apikey": "flashforge",
        "settings": {},
        "session": "flashforge",
        "is_external_client": False,
        }), 200

@app.get("/api/files")
def files():
    return json.dumps({
        "files": [
            {
                "name": "test.gcode",
                "path": "test.gcode",
                "type": "machinecode",
                "typePath": ["machinecode", "gcode"],
                "size": 69420,
                "origin": "sdcard"
            }
        ]
    }), 200

@app.post("/api/printer/sd")
def printer_sd():
    command = flask.request.json["command"]
    if command == "init":
        return '', 204

@app.get("/api/printer/sd")
def printer_sdget():
    return json.dumps({"ready": True}), 200

@app.get("/api/connection")
def connection():
    return json.dumps({
        "current": {
            "state": "Operational",
            "port": "/dev/ttyACM0",
            "baudrate": 115200,
            "printerprofile": "_default"
        },
        "options": {
            "ports": ["/dev/ttyACM0"],
            "baudrates": [115200],
            "printerProfiles": [{"name": "Default", "id": "_default"}],
            "portPreference": "/dev/ttyACM0",
            "baudratePreference": 115200,
            "printerProfilePreference": "_default",
            "autoconnect": True
        }
    }), 200

@app.get("/api/timelapse")
def timelapse():
    return json.dumps({}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)