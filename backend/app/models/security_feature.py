from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

# Table of security features that are manually confirmed and added in the database.
class SecurityFeature(Base):
    __tablename__ = "security_features"

    # Company
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        primary_key=True
    )

    # Features
    mfa_supported: Mapped[bool] = mapped_column(
        Boolean, 
        default=False
    )
    passkey_supported: Mapped[bool] = mapped_column(
        Boolean, 
        default=False
    )
    bug_bounty: Mapped[bool] = mapped_column(
        Boolean, 
        default=False
    )
    iso27001: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )
    soc2: Mapped[bool] = mapped_column(
        Boolean, 
        default=False
    )