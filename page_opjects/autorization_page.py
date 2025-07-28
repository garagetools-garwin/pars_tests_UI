import os
import time

import allure
import requests
from playwright.sync_api import Page
from dotenv import load_dotenv

load_dotenv()

ADMIN_BUYER_EMAIL = os.getenv("ADMIN_BUYER_EMAIL")
ADMIN_BUYER_PASSWORD = os.getenv("ADMIN_BUYER_PASSWORD")
TEST_BUYER_PASSWORD = os.getenv("TEST_BUYER_PASSWORD")
ADMIN_SELLER_EMAIL = os.getenv("ADMIN_SELLER_EMAIL")
ADMIN_SELLER_PASSWORD = os.getenv("ADMIN_SELLER_PASSWORD")
PURCHASER_EMAIL = os.getenv("PURCHASER_EMAIL")
PURCHASER_PASSWORD = os.getenv("PURCHASER_PASSWORD")
CONTRACT_MANAGER_EMAIL = os.getenv("CONTRACT_MANAGER_EMAIL")
CONTRACT_MANAGER_PASSWORD = os.getenv("CONTRACT_MANAGER_PASSWORD")
TESTMAIL_JSON_ = os.getenv("TESTMAIL_JSON_")
TESTMAIL_ADRESS_ = os.getenv("TESTMAIL_ADRESS_")

class AutorizationPage:
    def __init__(self, page: Page):
        self.page = page

    PATH = ""

    EMAIL_INPUT = "#email"
    PASSWORD_INPUT = "#password"
    CONFIRM_PASSWORD_INPUT = "#passwordConfirm"
    SUBMIT_BUTTON = "div button[type='submit']"
    USER_CARD_NOTIFICATION = ".notification__container .text-tag"


    def open(self, base_url):
        with allure.step(f"Открываю {base_url}"):
            return self.page.goto(base_url)


    @allure.step("Авторизуюсь на vi")
    def vi_test_authorize(self):
        self.page.goto("https://www.vseinstrumenti.ru/")
        pass

