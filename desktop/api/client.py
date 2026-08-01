import requests

BASE_URL = "http://127.0.0.1:8000"

# Get the health status of the API.
def health():
    # Attempt to connect to the API for 5 minutes and return the result.
    try:
        response = requests.get(
            f"{BASE_URL}/health",
            timeout=5
        )

        return response.json()

    # API is unresponsive.
    except requests.RequestException:
        return {
            "status": "Offline"
        }

# Get a list of all the companies in the database.
def get_companies():
    # Attempt the request for 5 minutes.
    try:
        response = requests.get(
            f"{BASE_URL}/companies",
            timeout=5
        )

        return response.json()

    # API is unresponsive.
    except requests.RequestException:
        return[]