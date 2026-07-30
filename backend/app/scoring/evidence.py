
from dataclasses import dataclass

# Evidence collected about a company's security posture.
@dataclass
class CompanyEvidence:
    major_breaches: int = 0
    minor_breaches: int = 0

    mfa_supported: bool = False
    passkey_supported: bool = False

    bug_bounty: bool = False

    iso27001: bool = False
    soc2: bool = False

    security_txt: bool = False