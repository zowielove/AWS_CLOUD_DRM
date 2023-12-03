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

    try:
        ec2 = boto3.client('ec2', regionName=regionName, accessID=accessID,
                           accessKey=accessKey)
        ssm = boto3.client('ssm', regionName=regionName, accessID=accessID,
                           accessKey=accessKey)
        cloudwatch = boto3.client('cloudwatch', regionName=regionName, accessID=accessID,
                                  accessKey=accessKey)
        sts = boto3.client('sts', accessID=accessID, accessKey=accessKey)
    except Exception as e:
        print(f"Error: {e}")
        exit(-1)


def printMenu():
    print("------------------------------------------------------------")
    print("  1. List Instance                2. Available Zones        ")
    print("  3. Start Instance               4. Available Regions      ")
    print("  5. Stop Instance                6. Create Instance        ")
    print("  7. Reboot Instance              8. List Images            ")
    print("                                 99. Quit                   ")
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


def listInstances():
    print(">> [ List instances ]")

    try:
        for rsv in ec2.describe_instances()['Reservations']:
            for inst in rsv['Instances']:
                print(f"\t[id] {inst['InstanceId']}")
                print(f"\t[AMI] {inst['ImageId']}")
                print(f"\t[type] {inst['InstanceType']}")
                print(f"\t[state] {inst['State']['Name']}")
                print(f"\t[monitoring state] {inst['Monitoring']['State']}\n")
    except Exception as e:
        print(f">> Error: {e}")
        exit(-1)


def availableZones():
    print(">> [ Available Zones ]")

    try:
        for zone in ec2.describe_availability_zones()['AvailabilityZones']:
            print(f"\t[id] {zone['ZoneId']}")
            print(f"\t[region] {zone['RegionName']}")
            print(f"\t[zone] {zone['ZoneName']}\n")
    except Exception as e:
        print(f">> Error: {e}")
        exit(-1)


def startInstance():
    print(">> [ Start Instance]")

    try:
        instanceID = input(">> Instance ID: ")

        rsp = ec2.describe_instances(InstanceIds=[instanceID])
        state = rsp['Reservations'][0]['Instances'][0]['State']['Name']

        if state == 'stopped':
            print(f">> Starting {instanceID}")
            try:
                ec2.start_instances(InstanceIds=[instanceID])
                print(f">> Instance {instanceID} started.")
            except Exception as e:
                print(f">> Error: {e}")
        elif state == 'running':
            print(f">> Instance {instanceID} is already running.")
        else:
            print(f">> Instance {instanceID} cannot started.")
            print(f">> Current State: {state}")
    except Exception as e:
        print(f">> Error: {e}")
        exit(-1)


def availableRegions():
    print(">> [ Available Regions ]")

    try:
        for region in ec2.describe_regions()['Regions']:
            print(f"\t[region] {region['RegionName']}")
            print(f"\t[endpoint] {region['Endpoint']}\n")
    except Exception as e:
        print(f">> Error: {e}")
        exit(-1)


def run():
    checkKey()
    initCloud()
    printMenu()
    runCommand(getCommand())


run()
