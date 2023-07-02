import paramiko
import subprocess
import logging

from paramiko.ssh_exception import AuthenticationException, SSHException


class SSHPython:
    def __init__(self):
        self.__ssh = None

    def connect(self, hostname, username=None, password=None, pkey=None):
        """
        Подключение к virtualbox
        :param str hostname:
        :param str username:
        :param str password:
        :param pkey:
        :return:
        """
        logging.info("Подключение к virtualbox")
        try:
            self.__ssh = paramiko.SSHClient()
            self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.__ssh.connect(hostname=hostname, username=username, password=password, pkey=pkey, timeout=15_000)
        except AuthenticationException:
            logging.error("Подключиться не удалось. AuthenticationException")
        except SSHException:
            logging.error("Подключиться не удалось. SSHException")


    def run_package(self, name_package):
        """
        Запуск пакета
        :param str name_package:
        :return:
        """
        logging.info("Запуск пакета удаленно")
        try:
            ssh_stdin, ssh_stdout, ssh_stderr = self.__ssh.exec_command(command=f'cd /usr/bin && ./{name_package}',
                                                                        timeout=15_000)
            ssh_stdin.write('y\n')
            logging.info(ssh_stdout.readlines())
            logging.info(ssh_stderr.readlines())
        except SSHException:
            logging.error("Подключиться не удалось. SSHException")


    def install_package(self, name_package):
        """
        Установка пакета
        :param str name_package:
        :return:
        """
        logging.info("Установка пакета")
        try:
            ssh_stdin, ssh_stdout, ssh_stderr = self.__ssh.exec_command(command=f'pkg install {name_package} && y')
            ssh_stdin.write('y\n')
            logging.info(ssh_stdout.readlines())
            logging.info(ssh_stderr.readlines())
        except SSHException:
            logging.error("Подключиться не удалось. SSHException")

    # TODO
    def download(self,
                 name_package=None,
                 path=None,
                 remotepath="~/"):
        """
        Загрузка исходного кода на сервер
        :param str name_package:
        :param str path:
        :param str remotepath:
        :return:
        """
        if name_package:
            self.install_package(name_package=name_package)
            return
        else:
            process = subprocess.run(
                ['cmd', f'scp -pw "qwerty" -r {path} 0.0.0.0:{remotepath}'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', timeout=15_000)

    def close(self):
        """
        Закрытие соединения
        :return:
        """
        self.__ssh.close()
