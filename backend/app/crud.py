from sqlalchemy.orm import Session
from app.models.company import Company
from app.schemas.company import CompanyCreate
from app.models.report import Report
from app.schemas.report import ReportCreate
from app.scoring.service import update_score
from app.services.scanner import scan_company

# Defines the creation and fetching of companies.
def create_company(db: Session, company: CompanyCreate):
    return scan_company(
    db,
    company.name,
    company.domain)

def get_companies(db: Session):
    return db.query(Company).all()

# Returns a company or creates an entry if not currently in the database.
def get_or_create_company(db: Session, name: str, domain: str):
    # Search if the company with the domain.
    company = (
        db.query(Company)
        .filter(Company.domain == domain)
        .first()
    )

    if company:
        return company

    return scan_company(
        db,
        name,
        domain
    )

# Defines the creation and fetching of reports.
def create_report(db: Session, company_id: int, report: ReportCreate):
    db_report = Report(
        company_id=company_id,
        title=report.title,
        description=report.description,
        report_date=report.report_date,
        severity=report.severity,
        source=report.source,
    )

    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    # Update the company's score.
    company = db.get(Company, company_id)
    update_score(db, company)

    return db_report

def get_reports(db: Session):
    return db.query(Report).all()