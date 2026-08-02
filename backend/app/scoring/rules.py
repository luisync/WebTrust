# Scoring weights used when calculating a company's WebTrust score.
# Each company begins with the same nuetral trust level.
BASE_SCORE = 50

# Amount of data beaches.
BREACH_MAJOR = -15
BREACH_MINOR = -5

# User password privacy protection.
MFA_SUPPORTED = 5
PASSKEY_SUPPORTED = 3

BUG_BOUNTY = 6

# Security certifications.
ISO_27001 = 8
SOC2 = 6

SECURITY_TXT = 2

# Headers.
HSTS = 2
CSP = 4
X_FRAME_OPTIONS = 1
X_CONTENT_TYPE_OPTIONS = 1
REFERRER_POLICY = 1