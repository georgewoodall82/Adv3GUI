#An api to send and receive GCode commands and files to the Adventurer 3 3D Printer via TCP.

import socket

socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT = 8899

def Connect(ip: str, port=PORT):
    #Connect to the printer at the given ip and port.
    #Returns a socket object.
    socket1.connect((ip, port))
    return socket1

def SendGCode(gcode):
    #Send the given gcode to the printer.
    #Returns the response from the printer.

    gcode = "~" + gcode + "\n"

    return SendTCP(gcode)

def SendTCP(data):
    #Send the given data to the printer.
    #Returns the response from the printer.
    socket1.send(data.encode())
    return socket1.recv(1024).decode()

def SendFile(filename):
    #Send the given file to the printer.
    #Returns nothing.
    #This doesnt work and I have no clue why.
    
    print("this doesnt work")

    SendGCode("M28 145119 0:/user/apitest.gx")


    with open(filename, "r", errors="ignore", encoding="ANSI") as f:
        chunk = f.read(4096)
        while chunk:
            SendTCP(chunk)
            chunk = f.read(4096)
    
    SendGCode("M29")
    SendGCode("M23 0:/user/apitest.gx")

    

def Disconnect():
    #Disconnect from the printer but keep the socket open.
    #Returns nothing.
    if isConnected():
        socket1.close()

def isConnected():
    #Check if the printer is connected.
    #Returns True if connected, False otherwise.
    try:
        socket1.send("~".encode())
        return True
    except:
        return False
