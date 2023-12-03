def printMenu():
    print("------------------------------------------------------------")
    print("  1. list instance                2. available zones        ")
    print("  3. start instance               4. available regions      ")
    print("  5. stop instance                6. create instance        ")
    print("  7. reboot instance              8. list images            ")
    print("                                 99. quit                   ")
    print("------------------------------------------------------------")


def getCommand():
    try:
        command = int(input(">> Command: "))
        return command
    except Exception as e:
        print(f">> Error: {e}")
        exit(-1)


def runCommand(command):
    if command == 1:
        listInstances()
    elif command == 2:
        availableZones()
    elif command == 3:
        startInstance()
    elif command == 4:
        availableRegions()
    elif command == 5:
        stopInstance()
    elif command == 6:
        createInstance()
    elif command == 7:
        rebootInstance()
    elif command == 8:
        listImages()
    elif command == 99:
        print(">> Quit Program.")
    else:
        print(">> Invalid input.")


printMenu()
runCommand(getCommand())
