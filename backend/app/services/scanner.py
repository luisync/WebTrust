from sqlalchemy.orm import Session
from app.models.company import Company
from app.scoring.service import update_score

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