
from dataclasses import dataclass

# Evidence collected about a company's security posture.
@dataclass
class CompanyEvidence:
    # Amount of data beaches.
    major_breaches: int = 0
    minor_breaches: int = 0

    # User password privacy protection.
    mfa_supported: bool = False
    passkey_supported: bool = False

    bug_bounty: bool = False

    # Security certifications.
    iso27001: bool = False
    soc2: bool = False

    # Securitxt file.
    security_txt: bool = False

    # Header fields.
    hsts: bool = False
    csp: bool = False
    x_frame_options: bool = False
    x_content_type_options: bool = False
    referrer_policy: bool = False