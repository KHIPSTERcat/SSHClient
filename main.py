import paramiko
import SshAuvLib

host = ['localhost']
username = 'chesh'
secret = input()
port = 22

session = SshAuvLib.SshAuvSession(host, username, secret, port)

if session.connection() != 0:
    print ('Lol')
    exit(1)

session.open_sftp_sessions()

print(session.get_file_list())

session.close()

# client.close()

