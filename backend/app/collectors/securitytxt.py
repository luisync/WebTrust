import requests

# Search for the company's security.txt.
def has_securitytxt(domain: str) -> bool:
    urls = [
        f"https://{domain}/.well-known/security.txt",
        f"https://{domain}/security.txt"
    ]

    for url in urls:
        try:
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                return True

        except requests.RequestException:
            continue

    return False

