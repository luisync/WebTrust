from app.scoring.evidence import CompanyEvidence
from app.scoring.calculator import calculate_score
from app.scoring.ratings import get_rating


evidence = CompanyEvidence(
    major_breaches=1,
    minor_breaches=2,
    mfa_supported=True,
    passkey_supported=True,
    bug_bounty=True,
    iso27001=True,
    soc2=True,
    security_txt=True
)

def test_calculate_score():
    assert calculate_score(evidence) is not None

def test_get_rating():
    assert get_rating(calculate_score(evidence)) is not None