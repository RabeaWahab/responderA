import sys
import boto3
import time
import datetime
import json
import argparse

class action:

	def __init__(self):
		self.conf = ""
		self.assumedRoleObject=""

	def load_conf(self, conf_file_location):
		conf_file= open(conf_file_location,'r')
		conf=json.load(conf_file)

		#set global variables 
		self.role=conf['global_conf'][0]['assume_role']
		self.revert_logs_bucket=conf['global_conf'][0]['revert_logs_bucket']
		self.revert_logs_role=conf['global_conf'][0]['revert_logs_role']
		self.revert_logs_account=conf['global_conf'][0]['revert_logs_account']
		return conf

	#Assume Role on a certain AWS account
	def assume_role(self,aws_account,role):
		sts_client = boto3.client('sts')
		assumedRoleObject = sts_client.assume_role(
			RoleArn="arn:aws:iam::" + aws_account + ":role/" + role,
			RoleSessionName="ResponderA_Session"
			)
		return assumedRoleObject

	def save_revert_log_file(self,revert_log,exec_name):
		self.revert_log_file="revert_logs" + "/revert_log" + '{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now()) + ".json"
		with open(self.revert_log_file, mode='a') as file:
			file.write(revert_log)
			file.closed

    	#Print revert help tip
		output = "Saving revert log to: " + self.revert_log_file + "\nTo revert the response run:" + exec_name +" --run revert_response --revert_log " + self.revert_log_file
		return output

	def upload_to_s3(self,file_name,bucket_name):

		self.assumedRoleObject=self.assume_role(self.revert_logs_account,self.revert_logs_role)			
		s3 = boto3.resource('s3',
			aws_access_key_id = self.assumedRoleObject['Credentials']['AccessKeyId'],
			aws_secret_access_key = self.assumedRoleObject['Credentials']['SecretAccessKey'],
			aws_session_token = self.assumedRoleObject['Credentials']['SessionToken']
			)
		s3.meta.client.upload_file(file_name, self.revert_logs_bucket,file_name)
