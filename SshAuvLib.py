import paramiko
import os
import tarfile


class SshAuvSession(object):

    def __init__(self, ip, user, password, port):
        self._ip = ip
        self._user = user
        self._password = password
        self._port = port
        self._clients = []
        self._sftp_sessions = []
        self._file_list = {}
        self._downloaded_files = []
        self._work_path = os.getcwd()
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

    def get_sftp_file_list(self):
        files_list = []
        for sftp_session in self._sftp_sessions:
            now_file_list = sftp_session.listdir()
            files_list = files_list + now_file_list
            for file in now_file_list:
                if file not in self._file_list:
                    self._file_list[file] = sftp_session
        files_list.sort()
        return files_list

    def sftp_close(self):
        for sftp in self._sftp_sessions:
            sftp.close()

    def close(self):
        for client in self._clients:
            client.close()

    def get_file_list(self):
        return os.listdir(self._work_path)

    def change_work_path(self, path):
        os.chdir(path)
        self._work_path = os.getcwd()
        return self.get_file_list()

    def change_sftp_work_path(self, path):
        for sftp_session in self._sftp_sessions:
            sftp_session.chdir(path)
        return self.get_sftp_file_list()

    @staticmethod
    def _get_date(file):
        return file.split("_")[0]

    def download_and_extract_files(self, files):
        dirs = []
        for file in files:
            if file not in self._downloaded_files and file.split(".")[-1] == 'tgz':
                dir_name = self._get_date(file)
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                if dir_name not in dirs:
                    dirs.append(dir_name)
                self._file_list[file].get(file, dir_name + '\\' + file)
                self._downloaded_files.append(file)
        self._extract_from_dir(dirs)

    @staticmethod
    def _extract_from_dir(dirs):
        for now_dir in dirs:
            files = os.listdir(now_dir)
            for file in files:
                if file.split(".")[-1] == 'tgz':
                    tar = tarfile.open(now_dir + '\\' + file, 'r:gz')
                    tar.extractall(now_dir)
                    tar.close()
                    os.remove(now_dir + '\\' + file)

    def delete_files(self, files):
        for file in files:
            self._file_list[file].remove(file)


