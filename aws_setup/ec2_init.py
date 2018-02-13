#!/usr/bin/env python3

import boto3
import sys

session = boto3.Session(profile_name='personal')

def main():
    # read arguments from the command line and
    # check whether at least two elements were entered
    if len(sys.argv) < 2:
        print("Usage: python aws.py {start|stop}\n")
        sys.exit(0)
    else:
        action = sys.argv[1]

    if action == "start":
        startInstance()
    elif action == "stop":
        stopInstance()
    else:
        print("Usage: python aws.py {start|stop}\n")

def startInstance():
    print("Starting the instance...")

    try:
        ec2 = session.client('ec2')

    except Exception as e1:
        error1 = "Error1: %s" % str(e1)
        print(error1)
        sys.exit(0)

    # change instance ID appropriately
    try:
        ec2.start_instances(
            InstanceIds = [
                'i-087c81221d8f56851',
            ],
            DryRun = False
        )

    except Exception as e2:
        error2 = "Error2: %s" % str(e2)
        print(error2)
        sys.exit(0)

def stopInstance():
    print("Stopping the instance...")

    try:
        ec2 = session.client('ec2')

    except Exception as e1:
        error1 = "Error1: %s" % str(e1)
        print(error1)
        sys.exit(0)

    try:
        ec2.stop_instances(
            InstanceIds = [
                'i-087c81221d8f56851',
            ],
            DryRun = False,
            Force  = False
        )

    except Exception as e2:
        error2 = "Error2: %s" % str(e2)
        print(error2)
        sys.exit(0)

if __name__ == '__main__':
    main()
