from sqlalchemy.orm import Session
from app.models.company import Company
from app.scoring.service import update_score
from app.collectors.breach import sync_all_companies_from_nvd, sync_company_from_nvd

# Updates a company's score after it's created, without this a report would need to be created.
def scan_company(db: Session, name: str, domain: str):
    company = Company(
        name=name,
        domain=domain,
        trust_score=50,
        rating="Unknown"
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    update_score(db, company)

    return company

# Scan the NVD for incidents.
def scan_nvd(
    db: Session,
    domain: str | None = None,
    *,
    days_back: int = 30,
    mode: str = "modified",
):
    if domain is None:
        return sync_all_companies_from_nvd(
            db,
            days_back=days_back,
            mode=mode,
        )

    company = (
        db.query(Company)
        .filter(Company.domain == domain)
        .first()
    )

    if company is None:
        return None

    return sync_company_from_nvd(
        db,
        company,
        days_back=days_back,
        mode=mode,
    )