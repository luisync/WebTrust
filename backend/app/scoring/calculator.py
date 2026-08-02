from app.scoring.evidence import CompanyEvidence
from app.scoring import rules

# Use calcaulating rules to compute a value -- the company's index.
def calculate_score(evidence: CompanyEvidence) -> int:
    score = rules.BASE_SCORE

    # Apply breach penelties.
    score += evidence.major_breaches * rules.BREACH_MAJOR
    score += evidence.minor_breaches * rules.BREACH_MINOR

    # Apply positive security features.
    if evidence.mfa_supported:
        score += rules.MFA_SUPPORTED

    if evidence.passkey_supported:
        score += rules.PASSKEY_SUPPORTED

    if evidence.bug_bounty:
        score += rules.BUG_BOUNTY

    if evidence.iso27001:
        score += rules.ISO_27001

    if evidence.soc2:
        score += rules.SOC2

    if evidence.security_txt:
        score += rules.SECURITY_TXT

    # Apply positive header fields.
    if evidence.hsts:
        score += rules.HSTS

    if evidence.csp:
        score += rules.CSP

    if evidence.x_frame_options:
        score += rules.X_FRAME_OPTIONS

    if evidence.x_content_type_options:
        score += rules.X_CONTENT_TYPE_OPTIONS

    if evidence.referrer_policy:
        score += rules.REFERRER_POLICY

    # Ensure score stays between 0 and 100.
    score = max(score, 0)
    score = min(score, 100)

    return score