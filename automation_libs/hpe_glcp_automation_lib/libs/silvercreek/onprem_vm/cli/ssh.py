# ==============================================================================
# title              :ssh.py
# description        :Script to do ssh in Jython and Python
# author             :Santhosh
# date               :6-Mar-2017
# version            :0.1
# ==============================================================================

import logging
from threading import current_thread

import paramiko


class SSH:
    """
    Class to do SSH.
    """

    def __init__(self, host, username, password):
        """
        Class initialization
        :param host: Hostname of the VM
        :param username: username to ssh
        :param password: password to ssh
        """
        self.logger = logging.getLogger(current_thread().name)
        self.host = host
        self.username = username
        self.password = password
        self.conn = ""
        self._open_ssh()

    def _open_ssh(self):
        """
        Opening ssh connection
        """
        try:
            self.logger.debug("Opening a SSH Connection")
            self.conn = paramiko.SSHClient()
            self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.conn.connect(self.host, username=self.username, password=self.password)
        except Exception as e:
            self.logger.error(
                "Unable to open SSH connection for host:{}".format(self.host)
            )
            self.logger.error(str(e))
            raise e

    def execute_command(self, command, wait_time=10):
        """
        Execute a command after connection is established
        :param command: command to be used
        :param wait_time: wait_time for the command
        :return: stdout, stderr
        """
        try:
            self.logger.debug("Executing command: %s" % command)
            ssh_stdin, ssh_stdout, ssh_stderr = self.conn.exec_command(
                command, timeout=wait_time
            )
            stdout = ssh_stdout.read().decode("utf-8")
            stderr = ssh_stderr.read().decode("utf-8")
            return stdout, stderr
        except Exception as e:
            # Seeing an intermittent problem where the command actually runs fine but
            # returns an empty exception string. So, handling it as success case and
            # returning a empty string when this happens.
            if not str(e):
                return "", ""
            self.logger.error(
                "Exception:'{}' while running command: '{}' on host:{}".format(
                    str(e), command, self.host
                )
            )
            self.logger.error(str(e))
            raise e

    def close_ssh(self):
        """
        Closing ssh connection
        """
        try:
            self.logger.debug("Closing SSH Connection")
            self.conn.close()
        except Exception as e:
            self.logger.error(str(e))
            raise e
