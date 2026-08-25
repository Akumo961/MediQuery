"""Smoke-test the local FastAPI service from a terminal."""

import requests


BASE_URL = "http://localhost:8000"
TIMEOUT_SECONDS = 5


def quick_test():
    """Call the main public endpoints and print a compact status report."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT_SECONDS)
        print(f"[OK] Health Check: {response.status_code} - {response.json()}")

        response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT_SECONDS)
        print(f"[OK] Main API: {response.status_code}")

        response = requests.get(
            f"{BASE_URL}/api/search/suggestions",
            params={"q": "cancer"},
            timeout=TIMEOUT_SECONDS,
        )
        print(f"[OK] Search Suggestions: {response.status_code}")

    except requests.RequestException as exc:
        print(f"[ERROR] API not running or unreachable: {exc}")


if __name__ == "__main__":
    quick_test()
