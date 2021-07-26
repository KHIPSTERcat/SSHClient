import paramiko


class SshAuvSession(object):

    def __init__(self, ip, user, password, port):
        self._ip = ip
        self._user = user
        self._password = password
        self._port = port
        self._clients = []
        self._sftp_sessions = []
        self._fileList = []
        for i in range(len(self._ip)):
            self._clients.append(paramiko.SSHClient())
            self._clients[-1].set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connection(self):
        for i in range(len(self._ip)):
            try:
                self._clients[i].connect(self._ip[i], self._port, self._user, self._password)
            except paramiko.SSHException:
                return i+1
        return 0

    def open_sftp_sessions(self):
        for client in self._clients:
            self._sftp_sessions.append(client.open_sftp())

    def get_file_list(self):
        files_list = []
        for sftp_session in self._sftp_sessions:
            now_file_list = sftp_session.listdir()
            files_list = files_list + now_file_list
            for file in now_file_list:
                if self._fileList.count(file) == 0:
                    self._fileList.append(file)
        return files_list

    def close(self):
        for client in self._clients:
            client.close()


