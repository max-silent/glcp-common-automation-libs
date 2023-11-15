"""
Login Types
"""
from . import okta, pf

LOGIN_TYPES = {
    "okta": okta.Okta,
    "pf": pf.PF,
    "okta_mfa": okta.OktaMFA,
    "okta_sso": okta.Okta_SSO,
}
