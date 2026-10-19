from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class BetSuccessModal:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    @property
    def success_label(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "h2.modalTitle")

    @property
    def bet_id(self) -> WebElement:
        return self.driver.find_element(By.ID, "modal-success-bet-id")

    @property
    def match(self) -> WebElement:
        return self.driver.find_element(By.ID, "modal-success-match")

    @property
    def stake(self) -> WebElement:
        return self.driver.find_element(By.ID, "modal-success-stake")

    @property
    def odds(self) -> WebElement:
        return self.driver.find_element(By.ID, "modal-success-odds")

    @property
    def payout(self) -> WebElement:
        return self.driver.find_element(By.ID, "modal-success-payout")

    @property
    def close_button(self) -> WebElement:
        return self.driver.find_element(By.ID, "modal-success-close")
