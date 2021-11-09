def comment():

    WINDOWS_LINE_ENDING = '\r\n'
    UNIX_LINE_ENDING = '\n'

    with open("apitestcopy.txt", "w", errors="ignore") as fc:
        with open("apitest.gx", errors="ignore") as f:
            for line in f.readlines():
                fc.writelines(line)


    exit()

import Adv3Api
import tkinter as tk
def connect(ip):
    socket1 = Adv3Api.Connect(ip)
    #when connected, print the currently connected ip
    if socket1.getpeername()[0] == ip:
        OutputLabel['text'] = "Output:\nConnected"
        ipLabel['text'] = "Connected to " + socket1.getpeername()[0]
        ipBox.destroy()
        connectButton.destroy()
        ipLabel.grid_configure(columnspan=3)
    else:
        OutputLabel['text'] = "Output:\nConnection failed"

def sendGCode(gcode):
    OutputLabel['text'] = "Output:\n" + Adv3Api.SendGCode(gcode)

root = tk.Tk()
root.title("Adv3 GUI")
root.geometry("300x200")
# set root['bg'] to a dark mode color
root.configure(background='#2f2f2f')


ipLabel = tk.Label(root, text="IP Address:", bg='#2f2f2f', fg='white')
ipLabel.grid(row=0, column=0)

ipBox = tk.Entry(root, bg='#2f2f2f', fg='#ffffff')
ipBox.grid(row=0, column=1)

connectButton = tk.Button(root, text="Connect", bg='#2f2f2f', fg='#ffffff', command=lambda: connect(ipBox.get()))
connectButton.grid(row=0, column=2)

GCodeLabel = tk.Label(root, text="GCode:", bg='#2f2f2f', fg='white')
GCodeLabel.grid(row=1, column=0)

GCodeBox = tk.Entry(root, bg='#2f2f2f', fg='#ffffff')
GCodeBox.grid(row=1, column=1)

GCodeSend = tk.Button(root, text="Send", bg='#2f2f2f', fg='#ffffff', command=lambda: sendGCode(GCodeBox.get()))
GCodeSend.grid(row=1, column=2)

OutputLabel = tk.Label(root, text="Output:", bg='#2f2f2f', fg='white')
OutputLabel.grid(row=2, column=0, columnspan=3)

root.grid_columnconfigure(0, weight=1)





root.mainloop()