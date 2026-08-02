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

# Returns a company that macthes the parameters or all companies if none are given.
def get_companies(db: Session, name: str | None = None, domain: str | None = None):
    # Determine what parameters the request provided.
    if not name and not domain:
        # Return a list of all companies when no parameter is givem.
        return db.query(Company).all()

    # Prepare query.
    company = db.query(Company)

    # Domain was given.
    if domain:
        # Update query to search the database with the domain.
        return company.filter(Company.domain == domain).first()

    # Name was given.
    elif name:
        # Update query to search the database with the name.
        return company.filter(Company.name == name).first()

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

# Returns all reports are affixed to a company.
def get_reports(db: Session, company_id: int | None = None, domain: str | None = None):
    # Determine what parameters the request provided.
    if not company_id and not domain:
        # Return a list of all companies when no parameter is givem.
        return db.query(Report).all()

    # Prepare query.
    report = db.query(Report)

    # Domain was given.
    if domain:
        # Search the database to for the company with the given domain.
        company = get_companies(db, domain=domain)

        if company is None:
            return []
        
        # Update query to search the database with the domain.
        return report.filter(Report.company_id == company.id).all()

    # Id was given.
    if company_id:
        # Update query to search the database with the name.
        return report.filter(Report.company_id == company_id).all()

    return []