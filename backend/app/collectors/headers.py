import requests

# Checks the headers present in a given domain.
def get_security_headers(domain: str) -> dict:
    try:
        response = requests.get(
            f"https://{domain}",
            timeout=5
        )

        headers = response.headers

        print(headers)
        return {
            "hsts": "Strict-Transport-Security" in headers,
            "csp": "Content-Security-Policy" in headers,
            "x_frame_options": "X-Frame-Options" in headers,
            "x_content_type_options": "X-Content-Type-Options" in headers,
            "referrer_policy": "Referrer-Policy" in headers,
        }

    except requests.RequestException:

        return {
            "hsts": False,
            "csp": False,
            "x_frame_options": False,
            "x_content_type_options": False,
            "referrer_policy": False,
        }
