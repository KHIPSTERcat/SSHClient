import paramiko
import SshAuvLib

host = ['localhost']
username = 'chesh'
secret = input()
port = 22

# client = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# # Подключение
# client.connect(host, port, username, secret)
#
# ftp = client.open_sftp()
# files = ftp.listdir()
# print(files)

session = SshAuvLib.SshAuvSession(host, username, secret, port)

if session.connection() != 0:
    print ('Lol')
    exit(1)

session.open_sftp_sessions()

print(session.get_file_list())

session.close()

# client.close()