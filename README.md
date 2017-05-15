SSHer version 1.0


This program has been developed by * to crack SSH default login credentials. SSHer uses paramiko as its main module. It also works with multithreading to speed the process. 

Dependencies:
	- paramiko

Default settings:
	- Port: 22
	- Threads: 10
	- Output: cracked-ips.txt
	- Verbose: False

Examples:
	python -u root -p toor -M ips.txt -t 20
	python -u usernames.txt -p passwords.txt -M ips.txt -o kaliMachines.txt
	python -u admin -p admin -M ips.txt --verbose --port=1000


