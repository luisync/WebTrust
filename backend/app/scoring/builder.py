from sqlalchemy.orm import Session
from app.models.report import Report
from app.scoring.evidence import CompanyEvidence
from app.models.company import Company
from app.collectors.securitytxt import has_securitytxt

# Converts reports into evidence, which can be later calculated into a score.
def build_evidence(db: Session, company_id: int) -> CompanyEvidence:
    # Load all of the reports a cvompany has.
    reports = (
        db.query(Report)
        .filter(Report.company_id == company_id)
        .all()
    )

    # Load the company.
    company = db.get(Company, company_id)

    # Load the company's evidence.
    evidence = CompanyEvidence()

    # Checking the severity of each report.
    for report in reports:
        if report.severity == "Major":
            evidence.major_breaches += 1

        elif report.severity == "Minor":
            evidence.minor_breaches += 1

    # Checking whether the company has a security.txt.
    if company is not None:
        evidence.security_txt = has_securitytxt(company.domain)

    return evidence