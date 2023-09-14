# Adv3GUI
A program to send G-code commands to a flashforge printer (I tested this with an adventurer 3, if you have another printer you can try this anyway as it has a high chance of working.

# Tested Printers:
- Adventurer 3
- Creator 4
- Creator 3 Pro
- Finder

If your printer is not on this list and works, you can open an issue and I will add it.

# Installation
1. Install Python 3 via https://www.python.org/ or if you are on a Linux distro you can use your preferred package installer.

2. Download all the files and extract them into the same folder. Alternatively, download as a zip and extract, or use git clone.

3. In a terminal (Linux Distros/Mac) or Command Prompt (Windows) navigate the the Folder you downloaded the Files into and then run `python3 Adv3GUI.py` or `python Adv3GUI.py` if that doesn't work. Or, `python3 Adv3CLI` which I prefer.

4. You should see the GUI and that means you are Done! You are free to use the API/Module for any projects.

# Gcode
There is a pdf file in the files with documentation to flashforge gcode (Thanks to [AJKnabenbauer](https://github.com/AJKnabenbauer))

[Or you can view it here](https://github.com/georgewoodall82/Adv3GUI/blob/main/FlashForge.Gcode.Protocol.open.pdf)

# 	Troubleshooting
1. Do not Include the Port in the IP address. For example `192.168.0.213:8899` should just be `192.168.0.213`

2. If you have a printer other than the Adventurer 3, read the top of the README

3. The SendFile() funcitons in Adv3Api is unreliable right now, I will try to make it work and then you can send gcode files from here.

4. Make sure you are on the same network connection as your printer

5. The G28 command doesn't work, it was broke in a recent firmware update. I may release a workaround that goes to the endstops and then sets the position when the G28 command is sent.

6. If this does not solve your problem, just open an issue.
