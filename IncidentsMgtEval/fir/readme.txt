sebtno/sebtno
ifconfig to get the <IPaddress>
cd dev/FIR
./startFIR.sh
From VM machine, open http://localhost:8000/ or http://<IPaddress:8000>
From Host machine, open http://<IPaddress:8000>
From external external machine, open http://<IPaddress:8000>

For local VM
Open http://192.168.9.128:8000

For Office VM
Connect to office wi-fi "TNO Singapore Local" 
Open http://192.168.0.55:8000

UserID/Password
dev/dev
admin/admin

https://heldercorreia.com/how-to-keep-a-process-running-66a7c6472930
https://stackoverflow.com/questions/10656147/how-do-i-keep-my-django-server-running-even-after-i-close-my-ssh-session
https://stackoverflow.com/questions/1188542/django-runserver-permanent

Technical specs
FIR is written in Python (but you probably already knew that), using Django 1.9. It uses Bootstrap 3 and some Ajax and d3js to make it pretty. We use it with a MySQL back-end, but feel free to use any other DB adaptor you might want - as long as it's compatible with Django, you shouldn't run into any major issues.

FIR is not greedy performance-wise. It will run smoothly on a Ubuntu 14.04 virtual machine with 1 core, a 40 GB disk and 1 GB RAM.


vCPU	ECU	Memory (GiB)	Instance Storage (GB)	Linux/UNIX Usage
t2.nano	 1	Variable	0.5	EBS Only	$0.0073 per Hour
t2.micro 1	Variable	1	EBS Only	$0.0146 per Hour
t2.small 1	Variable	2	EBS Only	$0.0292 per Hour

EBS-Optimized Usage
Standard Instances
m1.large	$0.025 per Hour
m1.xlarge	$0.05 per Hour




