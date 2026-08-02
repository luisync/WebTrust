from dataclasses import dataclass
from desktop.api.client import get_companies
from backend.app.collectors.securitytxt import has_securitytxt
from backend.app.collectors.headers import get_security_headers

# The object returned after scanning each company's security.
@dataclass
class Scan:
    name: str
    success: bool
    details: str

# Performs all security checks for the companies in the database.
def security_scan():
    results = []

    # Get all companies in the databse.
    companies = get_companies()

    for company in companies:
        # Run each security checking method and append the scan result to results.
        results.append(scan_securitytxt(company["domain"]))
        results.append(scan_headers(company["domain"]))

    return results

# Scan for securitytxt file.
def scan_securitytxt(domain: str) -> Scan:

    # Domain has securitytxt.
    if has_securitytxt:
        return Scan(
            name="Security.txt",
            success=True,
            details=f"{domain} has a security.txt file."
        )

    # Domain lacks securitytxt.
    return Scan(
        name="Security.txt",
        success=False,
        details=f"{domain} doesn't have a security.txt file."
    )
    
# Scan for secutiry headers.
def scan_headers(domain: str) -> Scan:
    # Check the headers enabled.
    headers = get_security_headers(domain)
    headers_enabled = []

    # Search for enabled headers.
    for key, value in headers.items():
        # Note down the security header if it's enabled.
        if value is True:
            headers_enabled.append(key)

    # No headers is enabled.
    if headers_enabled.__len__() == 0:
        return Scan(
            name="Security Headers",
            success=False,
            details=f"{domain} doesn't have any security headers enabled."
        )
    
    # Return a scan object with a list of the headers that are enabled. 
    return Scan(
        name="Security Headers",
        success=True,
        details=f"{domain} has the following headers enabled: {", ".join(headers_enabled)}"
    )