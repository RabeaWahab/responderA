import sys
import boto3
import time
import datetime
import json

import aws

class block_cidr:

	def revert_block_cidr_acl(self, revert_log, assumedRoleObject):
		print("Running revert_block_cidr_acl().. ")
	
		print ("Removing: " + str(revert_log))

		ec2 = boto3.resource('ec2',
			region_name=revert_log['region'],
			aws_access_key_id = assumedRoleObject['Credentials']['AccessKeyId'],
			aws_secret_access_key = assumedRoleObject['Credentials']['SecretAccessKey'],
			aws_session_token = assumedRoleObject['Credentials']['SessionToken']
			)
		network_acl = ec2.NetworkAcl(revert_log['acl_id'])

		#Delete Ingress rule	
		response = network_acl.delete_entry(
			DryRun=False,
			Egress=False,
			RuleNumber=revert_log['rule_number']
			)
		#Delete Egress rule
		response = network_acl.delete_entry(
			DryRun=False,
			Egress=True,
			RuleNumber=revert_log['rule_number']
		   )

		return

	def block_cidr_acl(self , cidr , conf):

		print("Running block_cidr_acl().. ")

		revert_log="{\n\"revert_metadata\":[\n"

		for acl in conf['acl_ids']:
			aws_account = acl['aws_account']
			region = acl['region']
			acl_id = acl['acl_id']	
			#assume role
			role=conf['global_conf'][0]['assume_role']
			assumedRoleObject=aws.assume_role(aws_account,role)
			ec2 = boto3.resource('ec2',
				region_name=region,
				aws_access_key_id = assumedRoleObject['Credentials']['AccessKeyId'],
				aws_secret_access_key = assumedRoleObject['Credentials']['SecretAccessKey'],
				aws_session_token = assumedRoleObject['Credentials']['SessionToken']
				)
			network_acl = ec2.NetworkAcl(acl_id)
		
			vpc_id = network_acl.vpc_id

			#Validate rule number
			rule_number=1
			rule_number_is_unique=False
			while rule_number_is_unique == False:
				for rule in network_acl.entries:
					rule_number_is_unique=True
					if rule_number == rule['RuleNumber']:
						rule_number_is_unique=0
						rule_number=rule_number + 1

			#Create Ingress blocking rule
			response_ingress = network_acl.create_entry(
				CidrBlock=cidr,
   		 		DryRun=False,
   	 			Egress=True,
   	 			PortRange={
    		    		'From': 0,
    		    		'To': 65535
    		    		},
    	    	Protocol='-1',
    			RuleAction='deny',
    			RuleNumber=rule_number
    			)
			#Create Egress blocking rule
			response_egress = network_acl.create_entry(
				CidrBlock=cidr,
    			DryRun=False,
    			Egress=False,
    			PortRange={
    			    		'From': 0,
    			    		'To': 65535
    			    		},
       		 	Protocol='-1',
    			RuleAction='deny',
    			RuleNumber=rule_number
    			)
			print ("Rule #: %d Created: CIDR: %s Blocked on %s %s in AWS_Account %s" %(rule_number,cidr, acl_id, vpc_id,aws_account))

			revert_log= revert_log + "{ \"type\": \"acl\", " + "\"aws_account\": \"" + aws_account + "\",\"region\": \"" + region + "\", \"acl_id\": \"" + acl_id + "\",\"rule_number\": " + str(rule_number) + "},\n" 
			#end of loop
		revert_log=revert_log[0:len(revert_log)-2]	
		revert_log= revert_log + "\n]}\n"

		return revert_log