import paramiko
import sys
client = paramiko.SSHClient()
client.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
client.load_system_host_keys()

def start_socket(ip):

    client.connect( str(ip), port=22, username='mohd', password='thisisadmin' )

    cmds = [ "ngrok tcp 22 > /dev/null &" ]

    for cmd in cmds:
        sys.stdin, sys.stdout, stderr = client.exec_command( cmd )
