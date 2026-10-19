import re

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait


class MatchListPage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def open_page(self, url: str) -> None:
        self.driver.get(url)

    def wait_page_loaded(self, timeout: int = 30) -> None:
        elements = (
            lambda: self.header_title,
            lambda: self.header_balance_container,
            lambda: self.header_balance,
            lambda: self.match_list_title,
            lambda: self.match_list_count,
            lambda: self.date_filter,
            lambda: self.odds_filter,
            lambda: self.match_list,
            lambda: self.match_card,
            lambda: self.match_meta,
            lambda: self.match_teams,
            lambda: self.odds_grid,
        )
        for get_element in elements:
            WebDriverWait(self.driver, timeout).until(
                lambda _, getter=get_element: bool(getter())
            )

    @property
    def header_title(self) -> WebElement:
        return self.driver.find_element(By.ID, "header-title")

    @property
    def header_balance_container(self) -> WebElement:
        return self.driver.find_element(By.ID, "header-balance")

    @property
    def header_balance(self) -> WebElement:
        return self.header_balance_container.find_element(
            By.XPATH, ".//span[contains(., 'Balance')]"
        )

    @property
    def match_list_title(self) -> WebElement:
        return self.driver.find_element(By.ID, "match-list-title")

    @property
    def match_list_count(self) -> WebElement:
        return self.driver.find_element(By.ID, "match-list-count")

    @property
    def date_filter(self) -> WebElement:
        return self.driver.find_element(By.ID, "date-filter")

    @property
    def odds_filter(self) -> WebElement:
        return self.driver.find_element(By.ID, "odds-filter")

    @property
    def bet_slip_content(self) -> WebElement:
        return self.driver.find_element(By.CLASS_NAME, "betSlipContent")

    @property
    def bet_selection_teams(self) -> WebElement:
        return self.driver.find_element(By.CLASS_NAME, "betSelectionTeams")

    @property
    def bet_selection_market(self) -> WebElement:
        return self.driver.find_element(By.CLASS_NAME, "betSelectionMarket")

    @property
    def bet_selection_odds(self) -> WebElement:
        return self.driver.find_element(
            By.CSS_SELECTOR, "div.betSelectionBottom span.betSelectionOdds"
        )

    @property
    def bet_slip_stake_input(self) -> WebElement:
        return self.driver.find_element(By.ID, "bet-slip-stake-input")

    @property
    def bet_slip_total_stake(self) -> WebElement:
        return self.driver.find_element(By.ID, "bet-slip-total-stake")

    @property
    def bet_slip_potential_payout(self) -> WebElement:
        return self.driver.find_element(By.ID, "bet-slip-potential-payout")

    @property
    def bet_slip_place_bet_button(self) -> WebElement:
        return self.driver.find_element(By.ID, "bet-slip-place-bet")

    @property
    def match_list(self) -> WebElement:
        return self.driver.find_element(By.ID, "match-list")

    @property
    def match_card(self) -> list[WebElement]:
        return self.match_list.find_elements(By.CSS_SELECTOR, "div.card.matchCard")

    @property
    def match_cards_by_id(self) -> dict[str, WebElement]:
        cards_by_id = {}
        for card in self.match_card:
            card_id = card.get_attribute("id")
            if card_id is None or not card_id.startswith("match-card-"):
                raise ValueError(f"Unexpected match card ID: {card_id!r}")
            cards_by_id[card_id.removeprefix("match-card-")] = card
        return cards_by_id

    @property
    def match_ids(self) -> set[str]:
        return set(self.match_cards_by_id)

    @property
    def shown_match_count(self) -> int:
        count_text = self.match_list_count.text
        count_match = re.fullmatch(r"Showing (\d+) matches", count_text)
        if count_match is None:
            raise ValueError(f"Unexpected match count text: {count_text!r}")
        return int(count_match.group(1))

    def get_match_date(self, match_id: str) -> str:
        card = self.match_cards_by_id[match_id]
        return card.find_element(By.CSS_SELECTOR, "div.matchMeta").text.splitlines()[-1]

    def get_match_teams(self, match_id: str) -> list[str]:
        card = self.match_cards_by_id[match_id]
        return [team.text for team in card.find_elements(By.CSS_SELECTOR, ".teamName")]

    def get_match_odds(self, match_id: str) -> list[str]:
        card = self.match_cards_by_id[match_id]
        return [
            odd.text for odd in card.find_elements(By.CSS_SELECTOR, ".oddsButtonValue")
        ]

    def select_match_home_win(self, match_id: str) -> None:
        card = self.match_cards_by_id[match_id]
        card.find_element(By.CSS_SELECTOR, ".oddsButtonValue").click()

    @property
    def match_meta(self) -> list[WebElement]:
        return [
            card.find_element(By.CSS_SELECTOR, "div.matchMeta")
            for card in self.match_card
        ]

    @property
    def match_teams(self) -> list[WebElement]:
        return [
            card.find_element(By.CSS_SELECTOR, "div.teams") for card in self.match_card
        ]

    @property
    def odds_grid(self) -> list[WebElement]:
        return [
            card.find_element(By.CSS_SELECTOR, "div.oddsGrid")
            for card in self.match_card
        ]
