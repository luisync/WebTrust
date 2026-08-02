import os
import re
import time
import requests

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Iterable
from sqlalchemy.orm import Session
from app.models.company import Company
from app.models.report import Report

# Values set by the NVD.
NVD_BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
REQUEST_TIMEOUT_SECONDS = 30
DEFAULT_RESULTS_PER_PAGE = 2000
MAX_DATE_WINDOW_DAYS = 120
DEFAULT_DAYS_BACK = 30
SLEEP_WITH_API_KEY_SECONDS = 1.0
SLEEP_WITHOUT_API_KEY_SECONDS = 6.0

# Summary of a report according to the details in the NVD.
@dataclass
class NVDIngestSummary:
    company_id: int
    company_name: str
    company_domain: str
    searched_terms: list[str]
    fetched: int = 0
    created: int = 0
    updated: int = 0

# If you're using an api key.
def _get_api_key() -> str | None:
    value = os.getenv("NVD_API_KEY", "").strip()
    return value or None

# Construct headers for requests.
def _request_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/json",
        "User-Agent": "WebTrust/0.1 (+https://localhost)",
    }

    api_key = _get_api_key()
    if api_key:
        headers["apiKey"] = api_key

    return headers

# Sleep for a certain duration depending on whether you have an API key or not.
def _sleep_seconds() -> float:
    return SLEEP_WITH_API_KEY_SECONDS if _get_api_key() else SLEEP_WITHOUT_API_KEY_SECONDS

# Convert date format to ISO format.
def _to_nvd_iso(value: datetime) -> str:
    return (
        value.astimezone(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )

# Define the rules for keeping the time since last database update within 120 days.
def _iter_windows(start: datetime, end: datetime) -> Iterable[tuple[datetime, datetime]]:
    current = start

    while current < end:
        window_end = min(current + timedelta(days=MAX_DATE_WINDOW_DAYS), end)
        yield current, window_end
        current = window_end

# Format data output.
def _normalize_terms(company: Company) -> list[str]:
    terms: list[str] = []

    name = (company.name or "").strip()
    domain = (company.domain or "").strip().lower().removeprefix("www.")

    if name:
        terms.append(name)
        terms.extend(
            token for token in re.split(r"[\s\-/_.]+", name)
            if len(token.strip()) > 2
        )

    if domain:
        terms.append(domain)
        root = domain.split(".")[0]
        if root and len(root) > 2:
            terms.append(root)

    seen: set[str] = set()
    cleaned: list[str] = []

    for term in terms:
        normalized = " ".join(term.split()).strip()
        if not normalized:
            continue

        key = normalized.lower()
        if key in seen:
            continue

        seen.add(key)
        cleaned.append(normalized)

    return cleaned

# Get descriptions of incidents.
def _extract_description(cve: dict) -> str:
    descriptions = cve.get("descriptions") or []
    for item in descriptions:
        if item.get("lang") == "en" and item.get("value"):
            return item["value"].strip()
    return ""

# Get references of breaches.
def _extract_reference_urls(cve: dict) -> list[str]:
    references = cve.get("references") or []

    # Accept dicts and lists as reports.
    if isinstance(references, dict):
        reference_data = references.get("referenceData") or []
    elif isinstance(references, list):
        reference_data = references
    else:
        reference_data = []

    urls: list[str] = []

    for item in reference_data:
        if isinstance(item, dict):
            url = (item.get("url") or "").strip()
        elif isinstance(item, str):
            url = item.strip()
        else:
            continue

        if url and url not in urls:
            urls.append(url)

    return urls

# Get severity.
def _extract_severity(cve: dict) -> str:
    metrics = cve.get("metrics") or {}

    for metric_key in ("cvssMetricV40", "cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
        for metric in metrics.get(metric_key, []) or []:
            cvss_data = metric.get("cvssData") or {}

            severity = (cvss_data.get("baseSeverity") or "").strip().upper()
            if severity:
                return severity

            base_score = cvss_data.get("baseScore")
            if base_score is not None:
                try:
                    score = float(base_score)
                except (TypeError, ValueError):
                    continue

                if score >= 9.0:
                    return "CRITICAL"
                if score >= 7.0:
                    return "HIGH"
                if score >= 4.0:
                    return "MEDIUM"
                if score > 0.0:
                    return "LOW"

    return "UNKNOWN"

# Link NVS severity to the databases' severity.
def _map_nvd_severity_to_report_severity(severity: str) -> str:
    severity = (severity or "").strip().upper()

    # Map the classifiers defined when extracting the severity to the ones seen in the databse.
    if severity in {"CRITICAL", "HIGH"}:
        return "Major"

    if severity in {"MEDIUM", "LOW"}:
        return "Minor"

    return "Unknown"

# Create the report's description.
def _build_report_description(cve: dict) -> str:
    cve_id = (cve.get("id") or "").strip()
    description = _extract_description(cve)
    reference_urls = _extract_reference_urls(cve)

    detail_url = f"https://nvd.nist.gov/vuln/detail/{cve_id}" if cve_id else "https://nvd.nist.gov/"

    parts: list[str] = []

    if description:
        parts.append(description)

    if cve_id:
        parts.append(f"NVD record: {cve_id}")

    parts.append(f"NVD URL: {detail_url}")

    # Add the references.
    if reference_urls:
        preview = reference_urls[:5]
        parts.append("References:\n" + "\n".join(f"- {url}" for url in preview))

    return "\n\n".join(parts)

# Fetch each CVE in the NVD's response.
def _fetch_cve_page(
    *,
    keyword: str,
    start_index: int,
    results_per_page: int,
    mode: str,
    window_start: datetime,
    window_end: datetime,
) -> dict:
    params: dict[str, str | int] = {
        "keywordSearch": keyword,
        "noRejected": "",
        "startIndex": start_index,
        "resultsPerPage": results_per_page,
    }

    if mode == "modified":
        params["lastModStartDate"] = _to_nvd_iso(window_start)
        params["lastModEndDate"] = _to_nvd_iso(window_end)
    elif mode == "published":
        params["pubStartDate"] = _to_nvd_iso(window_start)
        params["pubEndDate"] = _to_nvd_iso(window_end)
    else:
        raise ValueError("Mode must be 'modified' or 'published'.")

    response = requests.get(
        NVD_BASE_URL,
        params=params,
        headers=_request_headers(),
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    response.raise_for_status()
    return response.json()

# Updates reports or inserts it if doesn't already exist.
def _upsert_nvd_report(db: Session, company: Company, cve: dict) -> bool:
    cve_id = (cve.get("id") or "").strip()
    if not cve_id:
        return False

    # Get it's publiished date.
    published = cve.get("published")
    if published:
        published_dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
    else:
        published_dt = datetime.now(timezone.utc)

    # Get it's security and description.
    severity = _map_nvd_severity_to_report_severity(_extract_severity(cve))
    description = _build_report_description(cve)

    # Query the database for it.
    existing = (
        db.query(Report)
        .filter(
            Report.company_id == company.id,
            Report.source == "NVD",
            Report.title == cve_id,
        )
        .first()
    )

    # Return false if it already exists.
    if existing:
        existing.description = description
        existing.report_date = published_dt.date()
        existing.severity = severity
        return False

    # Add it to the database and return true if it didn't.
    report = Report(
        company_id=company.id,
        title=cve_id,
        description=description,
        report_date=published_dt.date(),
        severity=severity,
        source="NVD",
    )

    db.add(report)
    return True

# Ensures a company's record is synced with the NVD.
def sync_company_from_nvd(
    db: Session,
    company: Company,
    *,
    days_back: int = DEFAULT_DAYS_BACK,
    mode: str = "modified",
    results_per_page: int = DEFAULT_RESULTS_PER_PAGE,
) -> NVDIngestSummary:
    terms = _normalize_terms(company)
    summary = NVDIngestSummary(
        company_id=company.id,
        company_name=company.name,
        company_domain=company.domain,
        searched_terms=terms,
    )

    if not terms:
        return summary

    end = datetime.now(timezone.utc)
    start = end - timedelta(days=max(1, days_back))

    seen_cves: set[str] = set()
    sleep_seconds = _sleep_seconds()

    try:
        for term in terms:
            for window_start, window_end in _iter_windows(start, end):
                start_index = 0

                while True:
                    payload = _fetch_cve_page(
                        keyword=term,
                        start_index=start_index,
                        results_per_page=results_per_page,
                        mode=mode,
                        window_start=window_start,
                        window_end=window_end,
                    )

                    vulnerabilities = payload.get("vulnerabilities") or []
                    total_results = int(payload.get("totalResults") or 0)
                    current_page_size = int(payload.get("resultsPerPage") or results_per_page)

                    if not vulnerabilities and start_index == 0:
                        break

                    for item in vulnerabilities:
                        cve = item.get("cve") or {}
                        cve_id = (cve.get("id") or "").strip()
                        if not cve_id or cve_id in seen_cves:
                            continue

                        seen_cves.add(cve_id)
                        summary.fetched += 1

                        created = _upsert_nvd_report(db, company, cve)
                        if created:
                            summary.created += 1
                        else:
                            summary.updated += 1

                    start_index += current_page_size

                    if start_index >= total_results:
                        break

                    time.sleep(sleep_seconds)

        db.flush()
        from app.scoring.service import update_score
        update_score(db)
        db.commit()
        db.refresh(company)

        return summary

    except Exception:
        # Roll back the database in the case of an error.
        db.rollback()
        raise

# Sync all companies form the NVD into the database.
def sync_all_companies_from_nvd(
    db: Session,
    *,
    days_back: int = DEFAULT_DAYS_BACK,
    mode: str = "modified",
    results_per_page: int = DEFAULT_RESULTS_PER_PAGE,
) -> list[NVDIngestSummary]:
    companies = db.query(Company).all()
    summaries: list[NVDIngestSummary] = []

    for company in companies:
        summary = sync_company_from_nvd(
            db,
            company,
            days_back=days_back,
            mode=mode,
            results_per_page=results_per_page,
        )
        summaries.append(summary)

    return summaries


