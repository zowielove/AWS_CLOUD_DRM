import sys
import boto3

ec2, ssm, cloudwatch, sts = None, None, None, None
accessID, accessKey = None, None
regionName = 'eu-north-1'


def checkKey():
    global accessID, accessKey, regionName

    if len(sys.argv) < 2:
        print('run "python awsCloud.py (Access ID - required) (Access Key - required) (Region - optional)"')
        exit(-1)
    elif len(sys.argv) == 2:
        accessID = sys.argv[1]
        accessKey = sys.argv[2]

    elif len(sys.argv) == 3:
        accessID = sys.argv[1]
        accessKey = sys.argv[2]
        regionName = sys.argv[3]

    print(f"Access ID: {accessID}")
    print(f"Access Key: {accessKey}")
    print(f"Region Name: {regionName}")


def initCloud():
    global ec2, ssm, cloudwatch, sts

    ec2 = boto3.client('ec2', regionName=regionName, accessID=accessID,
                       accessKey=accessKey)
    ssm = boto3.client('ssm', regionName=regionName, accessID=accessID,
                       accessKey=accessKey)
    cloudwatch = boto3.client('cloudwatch', regionName=regionName, accessID=accessID,
                              accessKey=accessKey)
    sts = boto3.client('sts', accessID=accessID, accessKey=accessKey)


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
