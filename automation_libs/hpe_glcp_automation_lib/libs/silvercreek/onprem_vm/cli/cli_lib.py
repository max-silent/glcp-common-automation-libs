import logging
import os
import subprocess
from threading import current_thread

import pexpect

SSHKEY = "/usr/bin/ssh-keygen -R %s"
SSHCMD = "/usr/bin/ssh %s@%s"

logger = logging.getLogger(current_thread().name)


def remove_known_host_entry(ip):
    """Remove known host entry from ssh hosts using ssh keygen

    :param ip(string): IP string

    :returns: type int. 1 is successfull 0 otherwise

    """
    logger.info("Removing known hosts")
    subprocess.getstatusoutput("sudo ssh-keygen -R %s" % ip)
    _, output = subprocess.getstatusoutput("sudo ssh-keygen -F %s" % ip)
    return 0 if "found" in output else 1


def login_to_vm(vmconfig):
    """Calls login method of CLI_Lib and returns child object"""
    logger.info(">>  Creating object with node ip.")
    cli_lib = CLILib(
        vmconfig["VM"]["IP"],
        vmconfig["VM"]["CLI_USERNAME"],
        vmconfig["VM"]["CLI_PASSWORD"],
    )
    child = cli_lib.login()
    logger.info(">>  returning child object.")
    return child


class CLILib:
    """
    CLI Library Class
    """

    def __init__(self, ip, username="cliadmin", password="cliadmin"):
        """
        Class initialization
        :param ip: IP address of the VM
        :param username: username to connect to VM
        :param password: password to connect to VM
        """
        self.logger = logging.getLogger(current_thread().name)
        self.logger.info("Initializing VM Lib class")
        self.ip = ip
        self.username = username
        self.password = password
        self.logger.info(
            "Login credentials for %s username %s password %s"
            % (self.ip, self.username, self.password)
        )
        self.cmd_timeout = 100  # timeout for pexpect commands in secs
        self.successfull_login = False
        self.child = None

    def login(self):
        """Function to login to VM over SSH protocol

        :returns: type object. pexpect object handler

        """
        dirpath = os.getcwd()
        self.logger.info("Logging into directory path: {}".format(dirpath))
        self.logger.info(
            "Removing previous SSH key for VM IP:{} in known_hosts file".format(self.ip)
        )
        sshkey = SSHKEY % (self.ip)
        self.child = pexpect.spawn(sshkey)
        self.logger.info(
            "Trying SSH login to VM:{} with username:{}".format(self.ip, self.username)
        )
        sshcmd = SSHCMD % (self.username, self.ip)
        try:
            self.child = pexpect.spawn(sshcmd, encoding="utf-8")
            index = self.child.expect(
                [
                    pexpect.TIMEOUT,
                    "password:",
                    "yes/no",
                    "HOST IDENTIFICATION HAS CHANGED",
                    "Connection refused",
                    "Network is unreachable",
                ]
            )
            if index == 3:
                if not remove_known_host_entry(self.ip):
                    raise Exception(
                        "Failed to remove known host entry for %s from ssh/known_hosts"
                        % (self.ip)
                    )
                self.child.close(force=True)
                self.child = pexpect.spawn(sshcmd)
                index = self.child.expect(
                    [
                        pexpect.TIMEOUT,
                        "password:",
                        "yes/no",
                        "HOST IDENTIFICATION HAS CHANGED",
                        "Connection refused",
                        "Network is unreachable",
                    ]
                )
            if index == 0:
                raise Exception("Connection Timed out")
            if index == 4:
                raise Exception("Connection Refused")
            if index == 5:
                raise Exception("Network Unreachable")
            if index == 2:
                self.child.sendline("yes")
                index = self.child.expect([pexpect.TIMEOUT, "password: "])
            self.logger.info(
                "Login to collector %s with username %s password %s"
                % (self.ip, self.username, self.password)
            )
            if index == 1:
                self.child.sendline(self.password)
            else:
                raise Exception("Unable to do ssh")
            index = self.child.expect([pexpect.TIMEOUT, "try again"])
            if index == 2:
                self.child.close(force=True)
                raise Exception("Incorrect SSH password")
            if index == 1:
                self.child.close(force=True)
                raise Exception("SSH Timed out")
            self.successfull_login = True
            self.logger.info("Login successful")
            return self.child
        except Exception as e:
            self.logger.error("Login failed")
            raise Exception(
                "CLI login failed for VM:{}, Exception:{}".format(self.ip, str(e))
            )

    def logout(self):
        """Function to logout from VM with CLI options"""

        if self.successfull_login:
            self.logger.info("Logging out SSH session for user:{}".format(self.username))
        if self.child:
            self.child.sendline("\n")
            self.child.sendline("0")
