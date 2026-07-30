from sqlalchemy.orm import Session
from app.models.company import Company
from app.schemas.company import CompanyCreate
from app.models.report import Report
from app.schemas.report import ReportCreate

# Defines the creation and fetching of companies.
def create_company(db: Session, company: CompanyCreate):
    db_company = Company(
        name=company.name,
        domain=company.domain,
        trust_score=50,
        rating="Unknown"
    )

    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    return db_company


def get_companies(db: Session):
    return db.query(Company).all()

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

    return db_report

def get_reports(db: Session):
    return db.query(Report).all()