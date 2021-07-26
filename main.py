import paramiko
import SshAuvLib

host = ['localhost']
username = 'chesh'
secret = 'Ilia211000MICROSOFT'
port = 22

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Подключение
client.connect(host, port, username, secret)

ftp = client.open_sftp()
files = ftp.listdir()
print(files)
client.close()