import Adv3Api
import tkinter as tk
import tkinter.scrolledtext
from tkinter import filedialog

def output(text):
    OutputBox.configure(state="normal")
    OutputBox.insert(tk.END, "\n" + text)

    if OutputBox.get(1.0, tk.END)[0] == '\n':
        OutputBox.delete(1.0, 2.0)
    OutputBox.configure(state="disabled")


def connect(ip):
    # socket1 = Adv3Api.Connect(ip)
    success = Adv3Api.Connect(ip)
    # when connected, print the currently connected ip
    # if socket1.getpeername()[0] == ip:
    if success:
        #output("Connected to " + socket1.getpeername()[0])
        output("Connected to " + ip)
        ipBox.destroy()
        connectButton.destroy()
    else:
        output("Connection failed")


def sendGCode(gcode):
    output("Sent: " + gcode)
    output("Output:")
    output(Adv3Api.SendGCode(gcode))


def printGCodeFile():
    file_path = filedialog.askopenfilename(filetypes=[("GCode Files", "*.gcode")])
    if file_path:
        Adv3Api.SendFile(file_path)


def main():
    global ipBox, connectButton, OutputLabel, OutputBox, GCodeSend, AutoScrollCheck, GCodeBox, PrintGCodeButton, root
    print("Adv3GUI Starting")
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

    PrintGCodeButton = tk.Button(root, text="Print GCode File", bg='#2f2f2f', fg='#ffffff', command=printGCodeFile)
    #PrintGCodeButton.grid(row=3, column=2)
    #commented out because not very reliable right how

    cb = tk.IntVar()

    AutoScrollCheck = tk.Checkbutton(root, text="Auto Scroll", variable=cb)
    AutoScrollCheck.grid(row=4, column=0, columnspan=3)

    root.grid_columnconfigure(0, weight=1)

    print("Adv3GUI Started!")

    while True:
        try:
            if cb.get() == 1:
                OutputBox.see(tk.END)
            if not root.winfo_exists():
                break
        except:
            break
        root.update()

if __name__ == "__main__":
    main()