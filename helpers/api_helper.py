from decimal import Decimal, InvalidOperation
from typing import Any

import requests

BASE_API_URL = "https://qae-assignment-tau.vercel.app/api"
BALANCE_API_URL = f"{BASE_API_URL}/balance"
MATCHES_API_URL = f"{BASE_API_URL}/matches"


def get_balance(user_id: str) -> Decimal:
    response = requests.get(
        BALANCE_API_URL,
        headers={"x-user-id": user_id},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict) or "balance" not in payload:
        raise ValueError("Balance API response must be an object with a balance")
    try:
        balance = Decimal(str(payload["balance"]))
    except (InvalidOperation, TypeError, ValueError) as error:
        raise ValueError(
            "Balance API response must contain a numeric balance"
        ) from error
    if not balance.is_finite():
        raise ValueError("Balance API response must contain a finite balance")
    return balance


def get_matches(user_id: str) -> list[dict[str, Any]]:
    response = requests.get(
        MATCHES_API_URL,
        headers={"x-user-id": user_id},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list) or not all(
        isinstance(match, dict) for match in payload
    ):
        raise ValueError("Matches API response must be a JSON array of objects")
    return payload
