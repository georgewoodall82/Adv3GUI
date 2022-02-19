# Adv3GUI
A program to send G-code commands to an adventurer 3 (If you have another printer you try this anyway as it has a high chance of working. If it doesn't work, open an Issue.

# Installation
1. Install Python 3 via https://www.python.org/ or if you are on a Linux distro you can use your preferred package installer.

2. Download all the files and extract them into the same folder. Alternatively, download as a zip and extract, or use git clone.

3. In a terminal (Linux Distros/Mac) or Command Prompt (Windows) navigate the the Folder you downloaded the Files into and then run `python3 Adv3GUI` or `python Adv3GUI` if that doesn't work.

4. You should see the GUI and that means you are Done! You are free to use the API/Module for any projects.

# 	Troubleshooting
1. Do not Include the Port in the IP address. For example `192.168.0.213:8899` should just be `192.168.0.213`

2. If you have a printer other than the Adventurer 3, read the top of the README

3. If the SendFile() function in the Adv3Api does not work, this is normal. It is unfinished and probably wont be fixed anytime soon as I have no idea why it isn't working. But if you know why you can open an issue or pull request.

4. If `G28` (Home) doesn't work, this is normal. This is a problem with the printer and you will see that you cannot Home even using the FlashPrint software control panel. (atleast from my experience)

5. Make sure you are on the same network connection as your printer

6. If this does not solve your problem, just open an issue.
