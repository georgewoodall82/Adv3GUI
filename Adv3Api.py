#An api to send and receive GCode commands and files to the Adventurer 3 3D Printer via TCP.

import socket
import os.path
import threading

socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT = 8899

def parse_temperature_string(temperature_string):
    """
    Parses a temperature string and returns a dictionary of temperatures.
    
    Args:
        temperature_string (str): A string containing temperature values in the format "key1:temp1/target1 key2:temp2/target2 ...".
    
    Returns:
        dict: A dictionary where the keys are the temperature keys and the values are dictionaries with keys "temp" and "target".
              The "temp" key corresponds to the temperature value and the "target" key corresponds to the target value.
    """
    temperatures = {}
    parts = temperature_string.split()
    
    for part in parts:
        try:
            key, value = part.split(":")
        except:
            print(temperature_string)
            exit()
        temp, target = value.split("/")
        
        temperatures[key] = {
            "temp": int(temp),
            "target": int(target)
        }
    
    return temperatures

def parse_sd_status_string(sd_status_string):
    """
    Parses a SD status string and returns a tuple of SD status.

    Args:
        sd_status_string (str): A string containing SD status values in the format "SD printing byte 0/100".
    
    Returns:
        tuple: A tuple of SD status.
            the first value is the current byte, and the second value is the target byte
    """
    parts = sd_status_string.split()
    key, value = parts[-1].split("/")
    return int(key), int(value)

def parse_print_status_string(print_status_string):
    """
    Parses a given print status string and returns a dictionary containing the parsed information.

    Parameters:
    - print_status_string (str): The print status string to be parsed.

    Returns:
    - out (dict): A dictionary containing the parsed information from the print status string. The dictionary has the following keys:
        - "CurrentFile" (str): The name of the currently printing file. If no file is currently printing, this value will be blank.
        - "MachineStatus" (str): The machine status. Possible values are "READY" if the machine is ready, "BUILDING_FROM_SD" if the machine is building from SD, and possibly more status values.
        - "xEndstop" (bool): The state of the x-axis endstop. True if the endstop is triggered, False otherwise.
        - "yEndstop" (bool): The state of the y-axis endstop. True if the endstop is triggered, False otherwise.
        - "zEndstop" (bool): The state of the z-axis endstop. True if the endstop is triggered, False otherwise.
    """
    lines = print_status_string.split("\n")

    out = {}

    for line in lines:
        if "CurrentFile" in line:
            out["CurrentFile"] = ":".join(line.split(":")[1:]).strip()
            #Name of currently printing file, blank if not printing.
        if "MachineStatus" in line:
            out["MachineStatus"] = line.split(":")[1].strip()
            #READY if ready, BUILDING_FROM_SD if building from SD. there may be more.
        if "Endstop" in line:
            endstops = line.split(" ")[1:]
            out["xEndstop"] = endstops[0].split(":")[1] == "1"
            out["yEndstop"] = endstops[1].split(":")[1] == "1"
            out["zEndstop"] = endstops[2].split(":")[1] == "1"
            #Each endstop is True if triggered, and False if not.
    #print(print_status_string)
    #print(out)
    return out

# print(parse_print_status_string("""Sent: M119
# Output:
# CMD M119 Received.
# Endstop: X-max:0 Y-max:0 Z-max:0
# MachineStatus: READY
# MoveMode: READY
# Status: S:1 L:0 J:0 F:0
# LED: 1
# CurrentFile: 
# ok
# """))

connectedip = (None, None) # (ip, port)

def Connect(ip: str, port=PORT):
    global connectedip
    """
    Connect to the printer at the given ip and port.
    Returns:
        socket.socket: The socket :)
    """
    try:
        socket1.connect((ip, port))
    except:
        return False
    print("Connected")
    socket1.close()
    #return socket1
    connectedip = (ip, port)
    return True

def SendGCode(gcode, wait=True, smart=True):
    """
    Send the given gcode to the printer.
    Returns:
        str: The response from the printer (if wait is True)
    """
    if smart:
        split = gcode.split(" ")
        if split[0] == "G0":
            split[0] = "G1"
        gcode = " ".join(split)
    gcode = "~" + gcode + "\r\n"
    #print(gcode)

    result = SendTCP(gcode, wait)

    #print(result)

    return result

socket_lock = threading.Lock()

def SendTCP(data, wait=True):
    """
    Send the given data to the printer.
    Returns:
        str: The response from the printer (if wait is True)
    """
    with socket_lock:
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket1.connect(connectedip)
        socket1.send(data.encode())
        if wait:
            socket1.settimeout(2)  # Set a timeout of 2 seconds
            try:
                response = socket1.recv(1024).decode()
            except socket.timeout:
                response = "Timeout"  # Return "Timeout" if there is no response within 2 seconds
            socket1.close()
            return response
        socket1.close()

def SendFile(filename, outname="adv3api.gcode"):
    """
    Send the given file to the printer.
    Returns:
        None
    """
    SendGCode("M29")
    SendGCode(f"M28 {os.path.getsize(filename)} 0:/user/{outname}")

    with open(filename, "r", errors="ignore", encoding="ascii") as f:
        chunk = f.read(4096)
        while chunk:
            SendTCP(chunk, False)
            chunk = f.read(4096)
    
    SendGCode("M29", False)

def PrintFile(filename):
    """
    Print a file by sending the G-code command to the printer.

    Parameters:
        filename (str): The name of the file to be printed.

    Returns:
        None
    """
    SendGCode(f"M23 0:/user/{filename}")

def Disconnect():
    """
    Disconnect from the printer but keep the socket open.
    Returns:
        None
    """
    if isConnected():
        socket1.close()

def isConnected():
    """
    Check if the printer is connected.

    Returns:
        bool: True if connected, False otherwise.
    """
    try:
        # Send a test message to the printer
        socket1.send("~".encode())
        return True
    except:
        return False
    
def getTemperatures():
    """
    Parses a temperature string and returns a dictionary of temperatures.
    
    Args:
        temperature_string (str): A string containing temperature values in the format "key1:temp1/target1 key2:temp2/target2 ...".
    
    Returns:
        dict: A dictionary where the keys are the temperature keys and the values are dictionaries with keys "temp" and "target".
              The "temp" key corresponds to the temperature value and the "target" key corresponds to the target value.
    """
    return parse_temperature_string(SendGCode("M105").split("\n")[1])

def getSDPrintStatus():
    """
    Parses a SD status string and returns a tuple of SD status.

    Args:
        sd_status_string (str): A string containing SD status values in the format "SD printing byte 0/100".
    
    Returns:
        tuple: A tuple of SD status.
    """
    return parse_sd_status_string(SendGCode("M27").split("\n")[1])

def getPrintStatus():
    """
    Parses a given print status string and returns a dictionary containing the parsed information.

    Parameters:
    - print_status_string (str): The print status string to be parsed.

    Returns:
    - out (dict): A dictionary containing the parsed information from the print status string. The dictionary has the following keys:
        - "CurrentFile" (str): The name of the currently printing file. If no file is currently printing, this value will be blank.
        - "MachineStatus" (str): The machine status. Possible values are "READY" if the machine is ready, "BUILDING_FROM_SD" if the machine is building from SD, and possibly more status values.
        - "xEndstop" (bool): The state of the x-axis endstop. True if the endstop is triggered, False otherwise.
        - "yEndstop" (bool): The state of the y-axis endstop. True if the endstop is triggered, False otherwise.
        - "zEndstop" (bool): The state of the z-axis endstop. True if the endstop is triggered, False otherwise.
    """
    output = SendGCode("M119")
    print("START")
    print(output)
    print("END")
    return parse_print_status_string(output)

def jogPrinter(x=0, y=0, z=0, absolute=False, speed=-1):
    """
    Jog the printer by the given amount.

    Args:
        x (int, optional): The amount to move the X axis. Defaults to 0.
        y (int, optional): The amount to move the Y axis. Defaults to 0.
        z (int, optional): The amount to move the Z axis. Defaults to 0.
        absolute (bool, optional): Whether to move the axis to absolute position or relative. Defaults to False.
        speed (int, optional): The speed to jog at. Defaults to -1 mm/min. (-1 means default speed).
    """

    if absolute:
        SendGCode("G90")
    else:
        SendGCode("G91")
    
    if speed > -1:
        SendGCode(f"G0 X{x} Y{y} Z{z} F{speed}")
    else:
        SendGCode(f"G0 X{x} Y{y} Z{z}")