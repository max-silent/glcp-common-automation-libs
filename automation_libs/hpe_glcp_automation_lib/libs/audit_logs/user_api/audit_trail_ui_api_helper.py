import logging

from hpe_glcp_automation_lib.libs.audit_logs.user_api.audit_trail_user_api import (
    AuditTrail,
)

log = logging.getLogger(__name__)


class ATUIAPIHelper(AuditTrail):
    """
    AuditTrail UI API Helper Class
    """

    def __init__(self, host, user, password, pcid):
        log.info("Initializing Audit Trail UI API Helper for UI Api calls")
        super().__init__(host, user, password, pcid)
