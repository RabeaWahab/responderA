
# AWS responderA 
AWS responderA is an incident responding tool that is being developed to help Security Responders to rapidly respond to various incidents

It consists of different modules each designed to execute a certain response:

## Isolate_Instance module:
### Execution:
		./responderA.py --run isolate_instance --aws_account <Account NUmber> --region <Region> --instance_id <ID>

### Sample Output

```
responderA 0.3$ ./responderA.py --run isolate_instance --aws_account ******* --region us-east-1 --instance_id i-***********

Running isolate_instance()..

vpc_id identified: vpc-58b62f20

New IR Security Group created: sg-09662bd35222660a6

New AMI Image created: ami-03c54f801d13340fd

Image: ami-03c54f801d13340fd is pending

Image: ami-03c54f801d13340fd is pending

Image: ami-03c54f801d13340fd is pending

Image: ami-03c54f801d13340fd is pending

Image: ami-03c54f801d13340fd is pending

Image: ami-03c54f801d13340fd is pending

Image: ami-03c54f801d13340fd is pending

Image: ami-03c54f801d13340fd is pending

Image: ami-03c54f801d13340fd is pending

Image: ami-03c54f801d13340fd is available

Saving revert log to: revert_logs_folder/revert_log20180914-131714.json
```
### To revert the response run:

```
./responderA.py --run revert_response --revert_log revert_logs_folder/revert_log20180914-131714.json
```
## block_cidr module:

### Execution:
`./responderA.py --run block_cidr --cidr <172.16.1.1/24>`

### Example
``` 
responderA 0.3$ sudo ./responderA.py --run revert_response --revert_log revert_logs_folder/revert_log20180920-164104.json
```
### Sample Output
```
Running revert_block_cidr_acl()..

Removing: {'type': 'acl', 'aws_account': '523256993465', 'region': 'us-east-1', 'acl_id': 'acl-76fee60e', 'rule_number': 2}

Running revert_block_cidr_acl()..

Removing: {'type': 'acl', 'aws_account': '523256993465', 'region': 'us-east-1', 'acl_id': 'acl-045fba261fae47a28', 'rule_number': 2}

Running revert_block_cidr_acl()..

Removing: {'type': 'acl', 'aws_account': '523256993465', 'region': 'us-east-1', 'acl_id': 'acl-0f2f9fdd51f44a81c', 'rule_number': 2}
```