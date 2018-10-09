#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import sys
import boto3
import time
import datetime
import json
import argparse

import isolate_instance
import block_cidr

def display_banner():

    print("                                     _            ___")  
    print("                                    | |          / _ \ ")
    print(" _ __ ___  ___ _ __   ___  _ __   __| | ___ _ __/ /_\ \\")
    print("| '__/ _ \/ __| '_ \ / _ \| '_ \ / _` |/ _ \ '__|  _  |")
    print("| | |  __/\__ \ |_) | (_) | | | | (_| |  __/ |  | | | |")
    print("|_|  \___||___/ .__/ \___/|_| |_|\__,_|\___|_|  \_| |_/")
    print("              | |                                      ")
    print("              |_|                                      ")

    return

def revert_response(revert_log):
    revert_log_file= open(revert_log,'r')
    revert_log=json.load(revert_log_file)

    for log in revert_log['revert_metadata']:
        #print(log['type'])
        if log['type'] == "acl":
            action = block_cidr.block_cidr()
            action.conf = action.load_conf(conf_file)
            action.revert_block_cidr_acl(log)

        elif log['type'] == "isolate_instance":
            action=isolate_instance.isolate_instance()
            action.conf=action.load_conf(conf_file)
            action.revert_isolate_instance(log)    
    return


####### Main starts here ####### 

display_banner()

parser = argparse.ArgumentParser()
parser.add_argument('--run', required=1)
parser.add_argument('--cidr')
parser.add_argument('--instance_id')
parser.add_argument('--region')
parser.add_argument('--aws_account')
parser.add_argument('--revert_log')
parser.add_argument('--conf_file')
args = parser.parse_args()

conf_file="conf/aws_responder.conf"

if args.run == "isolate_instance":
    action=isolate_instance.isolate_instance()
    action.conf = action.load_conf(conf_file)
    revert_log=action.isolate_instance(args.instance_id, args.region, args.aws_account)
    print (action.save_revert_log_file(revert_log,sys.argv[0]))

elif args.run == "block_cidr":
    action = block_cidr.block_cidr()
    action.conf = action.load_conf(conf_file)
    revert_log = action.block_cidr_acl(args.cidr)
    print(action.save_revert_log_file(revert_log,sys.argv[0]))
    action.upload_to_s3(action.revert_log_file, action.revert_logs_bucket)
    
elif args.run == "revert_response":
    revert_response(args.revert_log)
else:
    print ("Usage: ir_aws.py [response] Parameters")

