
# Adv3GUI
A program to send G-code commands to a flashforge printer (I tested this with an adventurer 3, if you have another printer you try this anyway as it has a high chance of working.

# Tested Printers:
- Adventurer 3
- Creator 4
- Creator 3 Pro

If your printer is not on this list please open an issue, even if your printer works with this software.

# Installation
1. Install Python 3 via https://www.python.org/ or if you are on a Linux distro you can use your preferred package installer.

2. Download all the files and extract them into the same folder. Alternatively, download as a zip and extract, or use git clone.

3. In a terminal (Linux Distros/Mac) or Command Prompt (Windows) navigate the the Folder you downloaded the Files into and then run `python3 Adv3GUI` or `python Adv3GUI` if that doesn't work.
# Installation Scripts
Here are one-liner installation scripts for Windows, Linux, and MacOS. These scripts will install Python 3, clone this repository, and run the program.

## Windows
```powershell
# In PowerShell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1')); choco install python git -y; git clone https://github.com/georgewoodall82/Adv3GUI.git; cd Adv3GUI; python Adv3GUI.py
```

## Linux
```bash
# In Bash
sudo apt update; sudo apt install python3 git -y; git clone https://github.com/georgewoodall82/Adv3GUI.git; cd Adv3GUI; python3 Adv3GUI.py
```

## MacOS
```bash
# In Bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"; brew install python3 git; git clone https://github.com/georgewoodall82/Adv3GUI.git; cd Adv3GUI; python3 Adv3GUI.py
```
4. You should see the GUI and that means you are Done! You are free to use the API/Module for any projects.

# Gcode
There is a pdf file in the files with documentation to flashforge gcode (Thanks to [AJKnabenbauer](https://github.com/AJKnabenbauer))

[Or you can view it here](https://github.com/georgewoodall82/Adv3GUI/blob/main/FlashForge.Gcode.Protocol.open.pdf)

# 	Troubleshooting
1. Do not Include the Port in the IP address. For example `192.168.0.213:8899` should just be `192.168.0.213`

2. If you have a printer other than the Adventurer 3, read the top of the README

3. If the SendFile() function in the Adv3Api does not work, this is normal. It is unfinished and probably wont be fixed anytime soon as I have no idea why it isn't working. But if you know why you can open an issue or pull request.

4. Make sure you are on the same network connection as your printer

5. If this does not solve your problem, just open an issue.

