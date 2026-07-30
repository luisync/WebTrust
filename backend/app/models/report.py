from datetime import date
from sqlalchemy import Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

# Holds information on security breaches.
class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    # Basic information about the breach.
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False
    )
    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    report_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )
    severity: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    source: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    # Many-to-one relationship with companies table.
    company = relationship(
        "Company",
        back_populates="reports"
    )