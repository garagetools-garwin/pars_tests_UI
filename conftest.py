import pytest
from playwright.sync_api import sync_playwright

# --- Минимальный BROWSER_INIT_SCRIPT ---
BROWSER_INIT_SCRIPT = """
Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
window.chrome = window.chrome || {};
window.chrome = { runtime: {} };
Object.defineProperty(navigator, 'languages', { get: () => ['ru-RU', 'ru'] });
"""

# --- Настройки user agent и viewport ---
BROWSER_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
BROWSER_VIEWPORT = { "width": 1920, "height": 1080 }

# --- Аргументы Chromium минимально палящиеся ---
CHROMIUM_ARGS = [
    "--window-size=1920,1080",
    "--disable-infobars"
]

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=CHROMIUM_ARGS,
        )
        yield browser
        browser.close()

@pytest.fixture()
def page_fixture(browser):
    context = browser.new_context(
        user_agent=BROWSER_USER_AGENT,
        viewport=BROWSER_VIEWPORT,
        locale="ru-RU",
        color_scheme="light"
    )
    page = context.new_page()
    page.add_init_script(BROWSER_INIT_SCRIPT)
    # Allure трейсинг:
    context.tracing.start(screenshots=True, snapshots=True)
    yield page
    context.tracing.stop()
    context.close()
