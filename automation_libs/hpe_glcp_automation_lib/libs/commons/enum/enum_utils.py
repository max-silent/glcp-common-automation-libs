"""
Enum for GLCP internal events
"""

from enum import Enum


class EventType(str, Enum):
    CUSTOMER_EVENT = "CUSTOMER_EVENT"
    USER_EVENT = "USER_EVENT"
    CUSTOMER_USER = "CUSTOMER_USER"
    APP_PROVISION = "APP_PROVISION"
    DEVICE_PROVISION_INTERNAL_EVENT = "DEVICE_PROVISION_INTERNAL_EVENT"
    DEVICE_UNPROVISION_INTERNAL_EVENT = "DEVICE_UNPROVISION_INTERNAL_EVENT"

    def __str__(self):
        return str(self.value)


class AccountType(str, Enum):
    STANDALONE = "STANDALONE"
    MSP = "MSP"
    TENANT = "TENANT"
    BASIC_ORGANIZATION = "BASIC_ORGANIZATION"

    def __str__(self):
        return str(self.value)


class AccountStatus(str, Enum):
    BLOCKED = "BLOCKED"
    INACTIVE = "INACTIVE"
    ACTIVE = "ACTIVE"
    CREATING = "CREATING"
    CONFIRMED_BLOCKED = "CONFIRMED_BLOCKED"
    DELETE_INITIATED = "DELETE_INITIATED"

    def __str__(self):
        return str(self.value)


class OperationalMode(str, Enum):
    CUSTOMER_OWNED_INVENTORY = "CUSTOMER_OWNED_INVENTORY"
    MSP_OWNED_INVENTORY = "MSP_OWNED_INVENTORY"
    DEFAULT = "DEFAULT"

    def __str__(self):
        return str(self.value)


class Operation(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    HEALTH_CHECK = "HEALTH_CHECK"
    LOG = "LOG"

    def __str__(self):
        return str(self.value)


class OperationStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"

    def __str__(self):
        return str(self.value)


class ProvisionStatus(str, Enum):
    PROVISION_INITIATED = "PROVISION_INITIATED"
    PROVISIONED = "PROVISIONED"
    PROVISION_FAILED = "PROVISION_FAILED"
    UNPROVISION_INITIATED = "UNPROVISION_INITIATED"
    UNPROVISIONED = "UNPROVISIONED"
    UNPROVISION_FAILED = "UNPROVISION_FAILED"

    def __str__(self):
        return str(self.value)


class DeviceSubscriptionAssignmentStatus(str, Enum):
    SUCCESS = "SUCCESS"
    SUBSCRIPTION_LIMIT_EXCEEDED = "SUBSCRIPTION_LIMIT_EXCEEDED"
    SUBSCRIPTION_EXPIRED = "SUBSCRIPTION_EXPIRED"
    SUBSCRIPTION_SUSPENDED = "SUBSCRIPTION_SUSPENDED"
    SUBSCRIPTION_NOT_FOUND = "SUBSCRIPTION_NOT_FOUND"
    DEVICE_SUBSCRIPTION_NOT_ALLOWED = "DEVICE_SUBSCRIPTION_NOT_ALLOWED"
    DEVICE_SUBSCRIPTION_DEPRECATED = "DEVICE_SUBSCRIPTION_DEPRECATED"
    DEVICE_SUBSCRIPTION_ASSIGNMENT_FAILED = "DEVICE_SUBSCRIPTION_ASSIGNMENT_FAILED"
    DEVICE_SUBSCRIPTION_ASSIGNMENT_LIMIT_EXCEEDED = (
        "DEVICE_SUBSCRIPTION_ASSIGNMENT_LIMIT_EXCEEDED"
    )
    DEVICE_NOT_FOUND = "DEVICE_NOT_FOUND"
    DEVICE_SUBSCRIPTION_MISMATCH = "DEVICE_SUBSCRIPTION_MISMATCH"

    def __str__(self):
        return str(self.value)


class DeviceType(str, Enum):
    ALS = "ALS"
    AP = "AP"
    BLE = "BLE"
    COMPUTE = "COMPUTE"
    CONTROLLER = "CONTROLLER"
    DHCI_COMPUTE = "DHCI_COMPUTE"
    DHCI_STORAGE = "DHCI_STORAGE"
    EINAR = "EINAR"
    EINR = "EINR"
    GATEWAY = "GATEWAY"
    IAP = "IAP"
    LTE_MODEM = "LTE_MODEM"
    MC = "MC"
    STORAGE = "STORAGE"
    SWITCH = "SWITCH"
    NW_THIRD_PARTY = "NW_THIRD_PARTY"
    PCE = "PCE"
    SD_WAN_GW = "SD_WAN_GW"
    OPSRAMP_SAAS = "OPSRAMP_SAAS"
    SENSOR = "SENSOR"
    UNKNOWN = "UNKNOWN"

    def __str__(self):
        return str(self.value)


class ExternalDeviceType(str, Enum):
    AP = "AP"
    SWITCH = "SWITCH"
    GATEWAY = "GATEWAY"
    STORAGE = "STORAGE"
    DHCI_STORAGE = "DHCI_STORAGE"
    COMPUTE = "COMPUTE"
    DHCI_COMPUTE = "DHCI_COMPUTE"
    NW_THIRD_PARTY = "NW_THIRD_PARTY"
    PCE = "PCE"
    SD_WAN_GW = "SD_WAN_GW"
    OPSRAMP_SAAS = "OPSRAMP_SAAS"
    SENSOR = "SENSOR"

    def __str__(self):
        return str(self.value)


class SubscriptionType(str, Enum):
    CENTRAL_AP = "CENTRAL_AP"
    CENTRAL_SWITCH = "CENTRAL_SWITCH"
    CENTRAL_CONTROLLER = "CENTRAL_CONTROLLER"
    CENTRAL_GW = "CENTRAL_GW"
    SERVICE = "SERVICE"
    CENTRAL_STORAGE = "CENTRAL_STORAGE"
    CENTRAL_COMPUTE = "CENTRAL_COMPUTE"
    SUPPORT = "SUPPORT"
    CENTRAL_NW_THIRD_PARTY = "CENTRAL_NW_THIRD_PARTY"
    PRIVATE_CLOUD_ENTERPRISE = "PRIVATE_CLOUD_ENTERPRISE"
    OPSRAMP = "OPSRAMP"
    UXI_SENSOR_CLOUD = "UXI_SENSOR_CLOUD"
    UXI_SENSOR_LTE = "UXI_SENSOR_LTE"
    UXI_AGENT_CLOUD = "UXI_AGENT_CLOUD"
    UXI_AGENT_ANDROID = "UXI_AGENT_ANDROID"
    UNKNOWN = "UNKNOWN"

    def __str__(self):
        return str(self.value)