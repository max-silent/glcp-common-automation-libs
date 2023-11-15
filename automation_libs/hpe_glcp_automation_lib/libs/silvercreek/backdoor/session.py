import base64
import logging

from cryptography.fernet import Fernet

from hpe_glcp_automation_lib.libs.silvercreek.onprem_vm.cli.ssh import SSH

logging.basicConfig(level=logging.INFO)


class OnpremBackdoor(SSH):
    """
    Class providing backdoor utilities for connections to onprem databases. Only meant for TEST automation.
    """

    def __init__(self, host, username, password):
        logging.info(f"Setting up SSH connection to {host}")
        super().__init__(host=host, username=username, password=password)

    def __derive_key(self):
        if len(self.password) <= 32:
            return base64.urlsafe_b64encode(self.password.ljust(32).encode())
        else:
            return base64.urlsafe_b64encode(self.password[0:32].encode())

    def send(self, signal, msg="clear onprem device inventories"):
        """
        Sends a command to run on the onprem-vm datastores.

        :param signal: command sent to the onprem vm (for example: delete records from the ccs activate inventory relations)
        :param msg: debug message describe command/operation
        """
        logging.info(f"{msg} for {self.host}")
        try:
            # Seems unsafe to hardcode commands to delete/clear ccs data stores.. avoid revealing potential vulnerabilites
            self.execute_command(Fernet(self.__derive_key()).decrypt(signal).decode())
            # TODO: log identity of the process/user using this function to perform delete operations
        except Exception as clear_device_exc:
            logging.error(f"Could not {msg}. {str(clear_device_exc)}")

    def close(self):
        """
        Disconnect from the onprem vm.
        """
        logging.info(f"Disconnecting {self.host}")
        self.close_ssh()
