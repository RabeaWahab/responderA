aws responderA is an incident responding tool that is being developed to help Security Responders to rapidly respond to various incidents 
It consits of different modules each designed to execute a certain response: <br>

<b>Isolate_Instance module:</b>

Execution:
./responderA.py --run isolate_instance --aws_account <Account NUmber> --region <Region> --instance_id <ID> <br>
<br>
Sample Output<br>
responderA 0.3$ ./responderA.py --run isolate_instance --aws_account ******* --region us-east-1 --instance_id i-***********<br>
                                     _            ___ <br>
                                    | |          / _ \ <br>
 _ __ ___  ___ _ __   ___  _ __   __| | ___ _ __/ /_\ \ <br>
| '__/ _ \/ __| '_ \ / _ \| '_ \ / _` |/ _ \ '__|  _  | <br>
| | |  __/\__ \ |_) | (_) | | | | (_| |  __/ |  | | | | <br>
|_|  \___||___/ .__/ \___/|_| |_|\__,_|\___|_|  \_| |_/ <br>
              | |                                       <br>
              |_|                                       <br>
Running isolate_instance().. <br>
vpc_id identified: vpc-58b62f20<br>
New IR Security Group created: sg-09662bd35222660a6<br>
New AMI Image created: ami-03c54f801d13340fd<br>
Image: ami-03c54f801d13340fd is pending<br>
Image: ami-03c54f801d13340fd is pending<br>
Image: ami-03c54f801d13340fd is pending<br>
Image: ami-03c54f801d13340fd is pending<br>
Image: ami-03c54f801d13340fd is pending<br>
Image: ami-03c54f801d13340fd is pending<br>
Image: ami-03c54f801d13340fd is pending<br>
Image: ami-03c54f801d13340fd is pending<br>
Image: ami-03c54f801d13340fd is pending<br>
Image: ami-03c54f801d13340fd is available<br>
Saving revert log to: revert_logs_folder/revert_log20180914-131714.json<br>
To revert the response run:<br>
./responderA.py --run revert_response --revert_log revert_logs_folder/revert_log20180914-131714.json<br>
responderA 0.3$<br>
<br>
block_cidr module:<br>
<br>
./responderA.py --run block_cidr --cidr <172.16.1.1/24><br>
