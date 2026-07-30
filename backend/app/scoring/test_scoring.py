from app.scoring.evidence import CompanyEvidence
from app.scoring.calculator import calculate_score
from app.scoring.ratings import get_rating


company = CompanyEvidence(
    major_breaches=1,
    minor_breaches=2,
    mfa_supported=True,
    passkey_supported=True,
    bug_bounty=True,
    iso27001=True,
    soc2=True,
    security_txt=True
)

score = calculate_score(company)

print(score)
print(get_rating(score))