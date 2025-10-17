from datetime import datetime
import allure
import pytest
from dotenv import load_dotenv
import os
import re
from playwright.sync_api import Browser, Page, sync_playwright

from page_opjects.autorization_page import AutorizationPage

load_dotenv()  # Загружаем переменные из .env

AUTH_USERNAME = os.getenv("AUTH_USERNAME")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD")
PROXY_HOST = os.getenv("PROXY_HOST")
PROXY_PORT = os.getenv("PROXY_PORT")
PROXY_USER = os.getenv("PROXY_USER")
PROXY_PASS = os.getenv("PROXY_PASS")

proxy_settings = {
    "server": f"http://{PROXY_HOST}:{PROXY_PORT}",
    "username": PROXY_USER,
    "password": PROXY_PASS
}

BROWSER_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
BROWSER_VIEWPORT = {"width": 1920, "height": 1080}

BROWSER_INIT_SCRIPT = """
Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
window.chrome = window.chrome || {};
window.chrome = { runtime: {} };
Object.defineProperty(navigator, 'languages', { get: () => ['ru-RU', 'ru'] });
"""

chromium_args = [
    "--window-size=1920,1080",
    "--disable-infobars",
    "--no-sandbox"
]


def ensure_auth_states_dir_exists() -> str:
    project_root = os.path.dirname(os.path.abspath(__file__))
    auth_states_dir = os.path.join(project_root, 'auth_states')
    os.makedirs(auth_states_dir, exist_ok=True)
    return auth_states_dir

def get_env_from_url(base_url: str) -> str:
    if "stage" in base_url or "review-site" in base_url:
        return "stage"
    return "prod"

def build_auth_state_path(role: str, env: str) -> str:
    return os.path.join(ensure_auth_states_dir_exists(), f"auth_{role}_state_{env}.json")


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=chromium_args,
            #proxy=proxy_settings,  # если нужно
            #ignore_default_args=['--enable-automation']
        )
        yield browser
        browser.close()


def page_factory(
    browser: Browser,
    base_url: str,
    role: str = None,
    use_manual_login: bool = False
) -> Page:
    env = get_env_from_url(base_url)
    ctx_kwargs = {
        "user_agent": BROWSER_USER_AGENT,
        "viewport": BROWSER_VIEWPORT,
        "locale": "ru-RU",
        "color_scheme": "light"
    }
    if role:
        storage_state_path = build_auth_state_path(role, env)
        ctx_kwargs["storage_state"] = storage_state_path

    context = browser.new_context(**ctx_kwargs)
    page = context.new_page()
    page.add_init_script(BROWSER_INIT_SCRIPT)

    if env == "stage" and not use_manual_login and role:
        from dotenv import load_dotenv
        load_dotenv()
        user = os.getenv("AUTH_USERNAME")
        pwd = os.getenv("AUTH_PASSWORD")
        auth_url = base_url.replace("https://", f"https://{user}:{pwd}@")
        page.goto(auth_url)
        context.storage_state(path=storage_state_path)
    return page

@pytest.fixture()
def page_fixture(browser: Browser, request, base_url):
    pages = []

    def create_page(role: str = None, use_manual_login: bool = False):
        page = page_factory(browser, base_url, role, use_manual_login)
        pages.append(page)
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_name = re.sub(r'[\\/*?:"<>|\[\]]', '_', request.node.name)
        trace_path = os.path.join(os.getcwd(), f'traces/{safe_name}_{current_time}_{len(pages)}.zip')
        os.makedirs(os.path.dirname(trace_path), exist_ok=True)
        page.context.tracing.start(screenshots=True, snapshots=True)
        page._trace_path = trace_path
        return page

    yield create_page

    for page in pages:
        trace_path = getattr(page, "_trace_path", None)
        if trace_path:
            if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
                page.context.tracing.stop(path=trace_path)
                allure.attach.file(trace_path, name="trace", attachment_type='application/zip', extension='.zip')
                allure.attach(name="failure_screenshot", body=page.screenshot(full_page=True), attachment_type=allure.attachment_type.PNG)
                allure.attach(name="page_source", body=page.content(), attachment_type=allure.attachment_type.HTML)
            else:
                page.context.tracing.stop()
        page.context.close()


@pytest.fixture(scope="session")
def autorization_fixture(browser: Browser, base_url):
    env = get_env_from_url(base_url)
    role_to_auth_method = {
        "vi_test": "vi_test_authorize"
    }

    for role, auth_method in role_to_auth_method.items():
        context = browser.new_context()
        page = context.new_page()
        auth_page = AutorizationPage(page)
        auth_page.open(base_url)
        getattr(auth_page, auth_method)()
        context.storage_state(path=build_auth_state_path(role, env))
        context.close()


@pytest.fixture
def delete_user_fixture(base_url, page_fixture):
    state = {
        "user_created": False,
        "user_deleted": False
    }
    def mark_user_created():
        state["user_created"] = True
        print("=== USER CREATED ===")
        allure.attach("Пользователь создан", name="DEBUG", attachment_type=allure.attachment_type.TEXT)

    def mark_user_deleted():
        state["user_deleted"] = True
        print("=== USER DELETED MANUALLY ===")
        allure.attach("Пользователь удалён вручную", name="DEBUG", attachment_type=allure.attachment_type.TEXT)

    yield mark_user_created, mark_user_deleted

    print("=== TEARDOWN STARTED ===")
    allure.attach("Teardown начался", name="DEBUG", attachment_type=allure.attachment_type.TEXT)

    if state["user_created"] and not state["user_deleted"]:
        try:
            with allure.step("Удаляю пользователя в teardown"):
                from page_opjects.settings_account_page import SettingsAccountPage
                from page_opjects.home_page import HomePage
                admin_page = page_fixture()
                authorization_page = AutorizationPage(admin_page)
                settings_account_page = SettingsAccountPage(admin_page)
                home_page = HomePage(admin_page)
                settings_account_page.open(base_url)
                authorization_page.admin_buyer_authorize()
                home_page.click_settings_button()
                settings_account_page.click_users_button()
                settings_account_page.delete_last_created_user()
                allure.attach("Пользователь удалён в teardown", name="DEBUG", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(str(e), "Ошибка в teardown при удалении пользователя", allure.attachment_type.TEXT)

def pytest_addoption(parser):
    parser.addoption("--url", default="https://ya.ru/")

@pytest.fixture(scope="session")
def base_url(request):
    url = request.config.getoption('--url')
    return url

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)
    if report.outcome == "failed" and item.get_closest_marker("rerun"):
        allure.dynamic.label("rerun", "Test Rerun")
