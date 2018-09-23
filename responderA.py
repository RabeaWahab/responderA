#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import sys
import boto3
import time
import datetime
import json
import argparse

import aws
import isolate_instance
import block_cidr
#import isolate_bucket

conf_location='conf/aws_responder.conf'




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

            role=conf['global_conf'][0]['assume_role'] 
            assumedRoleObject=aws.assume_role(log['aws_account'],role)

            response=block_cidr.block_cidr()
            response.revert_block_cidr_acl(log , assumedRoleObject)

        elif log['type'] == "isolate_instance":

            role=conf['global_conf'][0]['assume_role'] 
            assumedRoleObject=aws.assume_role(log['aws_account'],role)

            response=isolate_instance.isolate_instance(-1, -1, -1,log, assumedRoleObject)
            response.revert_isolate_instance()
    return

def read_conf():

    conf_file= open(conf_location,'r')
    conf=json.load(conf_file)

    return conf

def save_revert_log_file(revert_log):
    revert_log_file="revert_logs_folder" + "/revert_log" + '{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now()) + ".json"
    with open(revert_log_file, mode='a') as file:
        file.write(revert_log)
    file.closed

    #Print revert help tip
    print ("Saving revert log to: " + revert_log_file + "\nTo revert the response run:")
    print(sys.argv[0] +" --run revert_response --revert_log " + revert_log_file)
    return

####### Main starts here ####### 

display_banner()

#Delerations
conf = read_conf()
revert_logs_folder = conf['global_conf'][0]['revert_logs_folder']

parser = argparse.ArgumentParser()
parser.add_argument('--run', required=1)
parser.add_argument('--cidr')
parser.add_argument('--instance_id')
parser.add_argument('--region')
parser.add_argument('--aws_account')
parser.add_argument('--revert_log')

args = parser.parse_args()

if args.run == "isolate_instance":
    role=conf['global_conf'][0]['assume_role']  
    assumedRoleObject=aws.assume_role(args.aws_account,role)

    response=isolate_instance.isolate_instance(args.instance_id, args.region, args.aws_account,-1, assumedRoleObject)
    revert_log=response.isolate_instance()

    save_revert_log_file(revert_log)
    
elif args.run == "block_cidr":
    
    #Assume role will happen inside block_cidr_acl
    
    response=block_cidr.block_cidr()
    revert_log = response.block_cidr_acl( args.cidr, conf )
    
    save_revert_log_file(revert_log)
    
#elif args.run == "isolate_bucket":
    #revert_log=isolate_bucket.isolate_bucket( sys.argv[2] , sys.argv[3] )
    #save_revert_log_file(revert_log)

elif args.run == "revert_response":
    revert_response(args.revert_log)
else:
    print ("Usage: ir_aws.py [response] Parameters")

