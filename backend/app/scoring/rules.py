# Scoring weights used when calculating a company's WebTrust score.
# Each company begins with the same nuetral trust level.
BASE_SCORE = 50

BREACH_MAJOR = -15
BREACH_MINOR = -5

MFA_SUPPORTED = 5
PASSKEY_SUPPORTED = 3

BUG_BOUNTY = 6

ISO_27001 = 8
SOC2 = 6

SECURITY_TXT = 2