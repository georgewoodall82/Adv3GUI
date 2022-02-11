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
import tkinter.scrolledtext

def output(text):
    OutputBox.configure(state="normal")
    OutputBox.insert(tk.END, "\n" + text)

    if OutputBox.get(1.0, tk.END)[0] == '\n':
        OutputBox.delete(1.0, 2.0)
    OutputBox.configure(state="disabled")


def connect(ip):
    socket1 = Adv3Api.Connect(ip)
    #when connected, print the currently connected ip
    if socket1.getpeername()[0] == ip:
        output("Connected to " + socket1.getpeername()[0])
        ipBox.destroy()
        connectButton.destroy()
        OutputLabel.grid_configure(row=0, sticky=tk.S)
        OutputBox.grid_configure(row=1)
        GCodeSend.grid_configure(row=2)
        AutoScrollCheck.grid_configure(row=2)
        GCodeSend.grid_configure(row=2)
        GCodeBox.grid_configure(row=2)
        root.rowconfigure(0, weight=1)
    else:
        output("Connection failed")

def sendGCode(gcode):
    output("Sent: " + gcode)
    output("Output:")
    output(Adv3Api.SendGCode(gcode))

root = tk.Tk()
root.title("Adv3 GUI")
root.geometry("600x470")
# set root['bg'] to a dark mode color
root.configure(background='#2f2f2f')


root.columnconfigure(3, weight=1)

root.rowconfigure(1, weight=1)

root.bind('<Control-t>', lambda a: output("Testing!"))

ipBox = tk.Entry(root, bg='#2f2f2f', fg='#ffffff', width=1000)
ipBox.grid(row=0, column=0, columnspan=2)
ipBox.insert(0, "Ip Address")

connectButton = tk.Button(root, text="Connect", bg='#2f2f2f', fg='#ffffff', command=lambda: connect(ipBox.get()))
connectButton.grid(row=0, column=2)

OutputLabel = tk.Label(root, text="Output:", bg='#2f2f2f', fg='white')
OutputLabel.grid(row=1, column=0, columnspan=3, sticky=tk.S)

OutputBox = tkinter.scrolledtext.ScrolledText(root, bg='#2f2f2f', fg='#ffffff', width=1000, state=tk.DISABLED)
OutputBox.grid(row=2, column=0, columnspan=3)

GCodeBox = tk.Entry(root, bg='#2f2f2f', fg='#ffffff', width=1000)
GCodeBox.grid(row=3, column=0)

GCodeSend = tk.Button(root, text="Send", bg='#2f2f2f', fg='#ffffff', command=lambda: sendGCode(GCodeBox.get()))
GCodeSend.grid(row=3, column=1)

cb = tk.IntVar()

AutoScrollCheck = tk.Checkbutton(root, text="Auto Scroll", variable=cb)
AutoScrollCheck.grid(row=3, column=2)

root.grid_columnconfigure(0, weight=1)



while True:
    try:
        if cb.get() == 1:
            OutputBox.see(tk.END)
        root.update()
    except Exception as e:
        if e.args[0].find('application has been destroyed') != -1 or e.args[0] == 'invalid command name ".!frame.!scrolledtext"':
            break