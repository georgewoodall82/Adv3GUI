import Adv3Api

def main():
    ip = input("Enter Printer IP:")
    if Adv3Api.Connect(ip):
        print("Connected to " + ip)
    else:
        print("Connection failed")
        return
    
    while True:
        gcode = input(f"<{ip}>")
        if gcode == "":
            continue
        print(Adv3Api.SendGCode(gcode))

if __name__ == "__main__":
    main()