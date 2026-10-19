import re
from datetime import date, datetime
from decimal import Decimal

import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait

from helpers.api_helper import get_balance
from modals.bet_success_modal import BetSuccessModal
from pages.match_list_page import MatchListPage


def _decimal_from_text(text: str) -> Decimal:
    match = re.search(r"-?\d+(?:[.,]\d+)?", text)
    assert match is not None, f"No numeric value found in {text!r}"
    return Decimal(match.group().replace(",", "."))


@allure.epic("Sports Betting")
@allure.feature("Match list")
class TestSportsBettingTests:
    @pytest.fixture(scope="class", autouse=True)
    @classmethod
    def initialize_pages(cls, driver, url):
        cls.match_list_page = MatchListPage(driver)
        cls.match_list_page.open_page(url)
        cls.match_list_page.wait_page_loaded()
        cls.bet_success_modal = BetSuccessModal(driver)

    @allure.title("Sports betting page has the expected browser title")
    @allure.story("Page navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description_html(
        "<p>Open the sports betting application and verify the browser title "
        "identifies the page.</p>"
    )
    def test_page_title(self):
        with allure.step("Read the browser page title"):
            actual_title = self.match_list_page.driver.title
        assert actual_title == "Sports Betting QA"

    @allure.title("Header displays the Sports Betting QA title")
    @allure.story("Page header")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description_html(
        "<p>Verify the main application title is visible in the page header.</p>"
    )
    def test_header_title(self):
        assert self.match_list_page.header_title.is_displayed()
        assert self.match_list_page.header_title.text == "Sports Betting QA"

    @allure.title("Header balance matches the balance API")
    @allure.story("Account balance")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description_html(
        "<p>Compare the euro balance shown in the page header with the value "
        "returned by the authenticated balance API.</p>"
    )
    def test_header_balance_is_displayed(self, user_id):
        with allure.step("Read the account balance from the API"):
            expected_balance = get_balance(user_id)
        with allure.step("Verify the displayed balance matches the API"):
            assert self.match_list_page.header_balance_container.is_displayed()
        assert (
            self.match_list_page.header_balance.text
            == f"Balance: €{expected_balance:.2f}"
        )

    @allure.title("Match-list heading and filters are visible")
    @allure.story("Match-list controls")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description_html(
        "<p>Verify the Upcoming Football Matches heading and the default date "
        "and odds filters are displayed.</p>"
    )
    def test_match_list_heading_and_filters_are_displayed(self):
        assert self.match_list_page.match_list_title.is_displayed()
        assert "Upcoming Football Matches" in self.match_list_page.match_list_title.text
        assert self.match_list_page.date_filter.is_displayed()
        assert "Date: All" in self.match_list_page.date_filter.text
        assert self.match_list_page.odds_filter.is_displayed()
        assert "Odds: All" in self.match_list_page.odds_filter.text

    @allure.title("Displayed match count matches the API response")
    @allure.story("Match data")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description_html(
        "<p>Verify both the count label and the rendered match cards agree with "
        "the number of matches returned by the API.</p>"
    )
    def test_match_count_matches_api_response(self, matches):
        expected_count = len(matches)
        assert self.match_list_page.shown_match_count == expected_count
        assert len(self.match_list_page.match_card) == expected_count

    @allure.title("Past matches are excluded from the match list")
    @allure.story("Match eligibility")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description_html(
        "<p>Compare the displayed match IDs with API matches whose kickoff date "
        "is earlier than today. The API does not provide kickoff times, so this "
        "check cannot identify matches earlier on the current date.</p>"
    )
    def test_past_matches_are_not_displayed(self, matches):
        displayed_match_ids = self.match_list_page.match_ids
        past_match_ids = {
            match["id"]
            for match in matches
            # The API provides dates without kickoff times, so matches earlier today cannot be identified.
            if date.fromisoformat(match["kickoffDate"]) < datetime.now().date()
        }
        displayed_past_match_ids = displayed_match_ids & past_match_ids

        assert not displayed_past_match_ids, (
            f"Past matches are displayed: {sorted(displayed_past_match_ids)}"
        )

    @allure.title("Match-card dates match API dates and use a consistent format")
    @allure.story("Match data")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description_html(
        "<p>Compare each card's displayed date with the API kickoff date using "
        "the abbreviated weekday, abbreviated month, and zero-padded day format. "
        "Today and tomorrow are excluded because the UI labels them relatively.</p>"
    )
    def test_match_dates_use_api_date_in_consistent_format(self, matches):
        mismatches = []

        for match in matches:
            match_date = date.fromisoformat(match["kickoffDate"])
            # The UI intentionally labels today's and tomorrow's fixtures relatively.
            if (match_date - date.today()).days in (0, 1):
                continue
            # Match the UI's abbreviated weekday, month, and zero-padded day format.
            expected_date = match_date.strftime("%a %d %b")
            displayed_date = self.match_list_page.get_match_date(match["id"])

            if displayed_date != expected_date:
                mismatches.append(
                    f"{match['id']}: expected {expected_date!r} for API date "
                    f"{match['kickoffDate']!r}, got {displayed_date!r}"
                )

        assert not mismatches, "Match date display mismatches:\n" + "\n".join(
            mismatches
        )

    @allure.title("Place a home-win bet on Arsenal vs Man City")
    @allure.story("Single bet placement")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description_html(
        "<p>Place a €10 home-win bet on Arsenal vs Man City, verify the bet slip "
        "and success receipt, then confirm the account balance was debited.</p>"
    )
    def test_place_arsenal_man_city_home_win_bet(self, user_id, matches):
        page = self.match_list_page
        driver = page.driver
        initial_balance = get_balance(user_id)
        assert initial_balance >= Decimal("10"), (
            f"Cannot place a €10 bet with balance €{initial_balance:.2f}"
        )
        assert page.header_balance.text == f"Balance: €{initial_balance:.2f}"

        match = next(
            (
                item
                for item in matches
                if item["homeTeam"] == "Arsenal" and item["awayTeam"] == "Man City"
            ),
            None,
        )
        assert match is not None, "Arsenal vs Man City was not found in the matches API"
        match_id = match["id"]
        assert match_id in page.match_ids, (
            f"Arsenal vs Man City match {match_id!r} is not displayed"
        )
        assert Decimal(str(match["odds"]["home"])) == Decimal("2.85")

        with allure.step("Select the Arsenal home-win outcome"):
            page.select_match_home_win(match_id)
            WebDriverWait(driver, 10).until(
                lambda _: page.bet_slip_content.is_displayed()
            )
        assert page.bet_selection_teams.text == "Arsenal vs Man City"
        assert "Home" in page.bet_selection_market.text
        assert _decimal_from_text(page.bet_selection_odds.text) == Decimal("2.85")

        with allure.step("Enter a €10 stake and verify the bet slip totals"):
            page.bet_slip_stake_input.clear()
            page.bet_slip_stake_input.send_keys("10")
            WebDriverWait(driver, 10).until(
                lambda _: "10" in page.bet_slip_total_stake.text
                and "28.5"
                in page.bet_slip_potential_payout.text.replace(",", ".")
            )
        assert _decimal_from_text(page.bet_slip_total_stake.text) == Decimal("10")
        assert _decimal_from_text(page.bet_slip_potential_payout.text) == Decimal(
            "28.5"
        )

        with allure.step("Place the bet and verify the success receipt"):
            page.bet_slip_place_bet_button.click()
            modal = BetSuccessModal(driver)
            WebDriverWait(driver, 10).until(
                lambda _: modal.success_label.is_displayed()
            )
            assert modal.success_label.text == "Bet Placed Successfully!"
            assert modal.match.text == "Arsenal vs Man City"
            assert _decimal_from_text(modal.stake.text) == Decimal("10")
            assert _decimal_from_text(modal.odds.text) == Decimal("2.85")
            assert _decimal_from_text(modal.payout.text) == Decimal("28.5")

        with allure.step("Close the receipt and verify the balance was debited"):
            modal.close_button.click()
            WebDriverWait(driver, 10).until(
                lambda _: not modal.success_label.is_displayed()
            )
            expected_balance = initial_balance - Decimal("10")
            WebDriverWait(driver, 10).until(
                lambda _: page.header_balance.text
                == f"Balance: €{expected_balance:.2f}"
            )
            assert get_balance(user_id) == expected_balance
            assert page.header_balance.text == f"Balance: €{expected_balance:.2f}"

    @allure.title("Displayed teams and odds match the API response")
    @allure.story("Match data")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description_html(
        "<p>For every match, verify the home and away team order and all three "
        "displayed odds values against the API response.</p>"
    )
    def test_rendered_teams_and_odds_match_api_response(self, matches):
        for match in matches:
            with allure.step(f"Verify teams and odds for match {match['id']}"):
                assert self.match_list_page.get_match_teams(match["id"]) == [
                    match["homeTeam"],
                    match["awayTeam"],
                ]
                assert self.match_list_page.get_match_odds(match["id"]) == [
                    f"{match['odds']['home']:.2f}",
                    f"{match['odds']['draw']:.2f}",
                    f"{match['odds']['away']:.2f}",
                ]
