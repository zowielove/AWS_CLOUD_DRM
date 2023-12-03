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

    print(">> [ Initial Information ]")
    print(f"\tAccess ID: {accessID}")
    print(f"\tAccess Key: {accessKey}")
    print(f"\tRegion Name: {regionName}")


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
        print(f"Error: {e}.")
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
        print(f">> Error: {e}.")
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
                print(f"\tInstance ID: {inst['InstanceId']}")
                print(f"\tInstance Type: {inst['InstanceType']}")
                print(f"\tState: {inst['State']['Name']}")
                print(f"\tImage ID: {inst['ImageId']}")
                print(f"\tMonitoring State: {inst['Monitoring']['State']}\n")
    except Exception as e:
        print(f">> Error: {e}.")
        exit(-1)


def availableZones():
    print(">> [ Available Zones ]")

    try:
        for zone in ec2.describe_availability_zones()['AvailabilityZones']:
            print(f"\tZone ID: {zone['ZoneId']}")
            print(f"\tZone Name: {zone['ZoneName']}\n")
            print(f"\tRegion Name:  {zone['RegionName']}")
    except Exception as e:
        print(f">> Error: {e}.")
        exit(-1)


def startInstance():
    print(">> [ Start Instance]")

    try:
        instanceID = input(">> Instance ID: ")

        rsp = ec2.describe_instances(InstanceIds=[instanceID])
        state = rsp['Reservations'][0]['Instances'][0]['State']['Name']

        if state == 'stopped':
            print(f">> Start {instanceID}.")
            try:
                ec2.start_instances(InstanceIds=[instanceID])
                print(f">> Instance {instanceID} started.")
            except Exception as e:
                print(f">> Error: {e}.")
                exit(-1)
        elif state == 'running':
            print(f">> Instance {instanceID} is already running.")
        else:
            print(f">> Instance {instanceID} cannot started.")
            print(f">> Current State: {state}")
    except Exception as e:
        print(f">> Error: {e}.")
        exit(-1)


def availableRegions():
    print(">> [ Available Regions ]")

    try:
        for region in ec2.describe_regions()['Regions']:
            print(f"\tRegion Name: {region['RegionName']}")
            print(f"\tEndpoint: {region['Endpoint']}\n")
    except Exception as e:
        print(f">> Error: {e}.")
        exit(-1)


def stopInstance():
    print(">> [ Stop Instance ]")

    try:
        instanceID = int(input('Instance ID: '))
        print(f">> Stop {instanceID}.")

        try:
            ec2.stop_instances(InstanceIds=[instanceID])
            print(f">> Instance {instanceID} stopped.")
        except Exception as e:
            print(f">> Error: {e}.")
            exit(-1)
    except Exception as e:
        print(f">> Error: {e}.")
        exit(-1)


def createInstance():
    print(">> [ Create Instance ]")

    try:
        AMI = input(">> AMI ID: ")
        instanceType = input(">> Instance Type(whitespace for t3.micro): ")

        if instanceType == '':
            instanceType = 't3.micro'

        print(f">> Create instance with AMI: {AMI}")

        try:
            instanceID = \
                ec2.run_instances(ImageId=AMI, InstanceType=instanceType, MaxCount=1, MinCount=1)['Instances'][0][
                    'InstanceId']
            print(f"Successfully created EC2 instance {instanceID} based on AMI {AMI}")
        except Exception as e:
            print(f">> Error {e}.")
            exit(-1)
    except Exception as e:
        print(f">> Error {e}.")
        exit(-1)


def rebootInstance():
    print(">> [ Reboot Instance ]")

    try:
        instanceID = input(">> Instance ID: ")
        print(f"Reboot {instanceID}.")
        try:
            ec2.reboot_instances(InstanceIds=[instanceID])
            print(f"Instance {instanceID} rebooted.")
        except Exception as e:
            print(f">> Error {e}.")
            exit(-1)
    except Exception as e:
        print(f">> Error: {e}.")
        exit(-1)


def listImages():
    print(">>[ List Images ]")

    try:
        imgs = ec2.describe_images(Owners=[sts.get_caller_identity().get('Account')])
        for i in imgs['Images']:
            print(f"\tImageID: {i['ImageId']}")
            print(f"\tName: {i['Name']}")
            print(f"\tOwner: {i['OwnerId']}\n")
    except Exception as e:
        print(f">> Error: {e}.")
        exit(-1)


def run():
    checkKey()
    initCloud()
    printMenu()
    runCommand(getCommand())


run()
