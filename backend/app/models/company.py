from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

# Holds basic information about a company's profile.
class Company(Base):
    __tablename__ = "companies"

    # Fields relating to indentifying a company.
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
    )
    domain: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Quantitative and qualitative forms of the rating.
    trust_score: Mapped[int] = mapped_column(
        Integer,
        default=50
    )
    rating: Mapped[str] = mapped_column(
        String(50),
        default="Fair"
    )

    # Security features that a company has.
    mfa_supported: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    passkey_supported: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    bug_bounty: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    iso27001: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    soc2: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    security_txt: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # One-to-many relationship with secutiry reports table.
    reports = relationship(
        "Report",
        back_populates="company",
        cascade="all, delete-orphan"
    )
