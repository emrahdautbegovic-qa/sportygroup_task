import json
from typing import Any
from urllib.parse import quote, quote_plus, urlencode

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from helpers.api_helper import get_matches


BASE_URL = "https://qae-assignment-tau.vercel.app/"


def _redact_user_id(text: str, user_id: str | None) -> str:
    if not user_id:
        return text

    for value in {user_id, quote(user_id, safe=""), quote_plus(user_id)}:
        if value:
            text = text.replace(value, "[REDACTED]")
    return text


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--user-id",
        action="store",
        default=None,
        help="user ID to use for tests",
    )


@pytest.fixture(scope="session")
def user_id(request: pytest.FixtureRequest) -> str:
    value = request.config.getoption("--user-id")
    if value is None:
        pytest.fail(
            "--user-id is required when using the user_id fixture", pytrace=False
        )
    return value


@pytest.fixture(scope="session")
def url(user_id: str) -> str:
    # Keep the user ID within the query parameter if it contains special characters.
    return f"{BASE_URL}?{urlencode({'user-id': user_id})}"


@pytest.fixture
def matches(user_id: str) -> list[dict[str, Any]]:
    return get_matches(user_id)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]):
    outcome = yield
    report = outcome.get_result()
    if not report.failed:
        return

    browser = item.funcargs.get("driver")
    if browser is None:
        return

    user_id = item.config.getoption("--user-id")
    allure.attach(
        browser.get_screenshot_as_png(),
        name="Failure screenshot",
        attachment_type=allure.attachment_type.PNG,
    )
    allure.attach(
        _redact_user_id(
            f"Failure phase: {report.when}\nURL: {browser.current_url}\n"
            f"Title: {browser.title}",
            user_id,
        ),
        name="Browser details",
        attachment_type=allure.attachment_type.TEXT,
    )
    allure.attach(
        _redact_user_id(browser.page_source, user_id),
        name="Page source",
        attachment_type=allure.attachment_type.HTML,
    )
    allure.attach(
        _redact_user_id(json.dumps(browser.get_log("browser"), indent=2), user_id),
        name="Browser console logs",
        attachment_type=allure.attachment_type.JSON,
    )


@pytest.fixture(scope="session")
def driver():
    options = Options()
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    browser = webdriver.Chrome(options=options)
    try:
        browser.maximize_window()
        yield browser
    finally:
        browser.quit()
