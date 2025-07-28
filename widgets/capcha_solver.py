import os
import base64
import random
import re
from io import BytesIO
from typing import Optional, Tuple
# from PIL import Image
from playwright.sync_api import Page, sync_playwright, TimeoutError as PwTimeout
import pytest
import time
import allure
import requests
from playwright.sync_api import Page
from dotenv import load_dotenv

from conftest import ensure_auth_states_dir_exists

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@allure.title("Проверяю наличие forbidden")
def page_contains_forbidden(page: Page) -> bool:
    try:
        body_text = page.content().lower()
        if "forbidden" in body_text:
            print("На странице найден forbidden — бан или антибот.")
            return True
    except Exception as e:
        print(f"Ошибка при попытке получить текст страницы: {e}")
    return False

class SyncCaptchaSlider:

    def __init__(self, page: Page, gemini_api_key: Optional[str] = None):
        self.page = page
        self.gemini_api_key = gemini_api_key

    CAPCHA_CONTROL_BUTTON = "div.captcha-control-button"
    PASSWORD_INPUT = "#password"
    CONFIRM_PASSWORD_INPUT = "#passwordConfirm"
    SUBMIT_BUTTON = "div button[type='submit']"
    USER_CARD_NOTIFICATION = ".notification__container .text-tag"

    @allure.title("Смотрим наличе капчи на странице, если есть, решаем")
    def capcha_solver(self):
        try:
            # ЯВНО ждем появления слайдера, например до 10 секунд (10000 мс)!
            self.page.wait_for_selector(self.CAPCHA_CONTROL_BUTTON, timeout=10000)
            print("Селектор слайдера появился")
        except Exception:
            print("Капча не появилась в течение 60 секунд")
            return  # или что нужно делать если капчи нет

        # Дальше стандартная логика:
        if self.page.locator(self.CAPCHA_CONTROL_BUTTON).count() > 0:
            print("Обнаружена капча — пытаемся решить...")
            solved = self.solve_with_retries(max_attempts=10)
            if not solved:
                assert False, "Не удалось решить капчу за 10 попыток"
            if page_contains_forbidden(self.page):
                assert False, "Тест остановлен: найден forbidden после решения капчи"
            auth_states_dir = ensure_auth_states_dir_exists()
            storage_path = os.path.join(auth_states_dir, "auth_vi_test_state_prod.json")

            self.page.context.storage_state(path=storage_path)
    def solve_with_retries(self, gemini_mode=False, max_attempts=10):
        for attempt in range(1, max_attempts + 1):
            print(f"\nПопытка #{attempt}")
            if page_contains_forbidden(self.page):
                assert False, f"Тест остановлен: найден forbidden на попытке {attempt}"
            if not self.wait_for_captcha_load(15000):
                print("Капча не найдена")
                continue
            captcha_elements = self.find_captcha_elements()
            if not captcha_elements:
                print("Элементы капчи не найдены")
                continue
            container, _, slider_button = captcha_elements

            if gemini_mode and self.gemini_api_key:
                image = self.capture_captcha_image(container)
                distance = self.solve_captcha_gemini(image) if image else None
                if distance is None:
                    print("Нет ответа от нейронки, двигаем на 90 пикселей")
                    distance = 90.0
            else:
                distance = 90.0

            self.human_like_drag(slider_button, distance)

            # Ждем пропадания кнопки ― динамически, без sleep!
            try:
                self.page.wait_for_selector('div.captcha-control-button', timeout=7000, state='detached')
            except PwTimeout:
                print("Кнопка не исчезла после drag (7 сек), пробуем еще раз!")
                continue

            # Теперь ждем (до 10 сек) появления новой кнопки ― если не появилась, значит, все решено!
            try:
                self.page.wait_for_selector('div.captcha-control-button', timeout=15000)
                print("Капча не пройдена, пробуем еще раз")
            except PwTimeout:
                print("Капча пройдена!")
                return True

        print("Не удалось пройти капчу за 10 попыток")
        return False

    def prepare_human_like_environment(self):
        self.page.context.set_default_timeout(60000)
        self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru', 'en-US', 'en']});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            window.chrome = { runtime: {} };
        """)

    def wait_for_captcha_load(self, timeout: int = 15000) -> bool:
        try:
            self.page.wait_for_selector('div.captcha-control', timeout=timeout)
            return True
        except Exception as e:
            print(f"Капча не загрузилась: {e}")
            return False

    def find_captcha_elements(self):
        try:
            container = self.page.locator('div.captcha-control')
            slider_wrap = self.page.locator('div.captcha-control-wrap')
            slider_button = self.page.locator('div.captcha-control-button')
            if container.count() > 0 and slider_wrap.count() > 0 and slider_button.count() > 0:
                return container, slider_wrap, slider_button
        except Exception as e:
            print(f"Ошибка при поиске элементов: {e}")
        return None

    def capture_captcha_image(self, container: Page) -> Optional[Image.Image]:
        try:
            box = container.bounding_box()
            screenshot = self.page.screenshot()
            full_img = Image.open(BytesIO(screenshot))
            cropped = full_img.crop((box['x'], box['y'], box['x'] + box['width'], box['y'] + box['height']))
            return cropped
        except Exception as e:
            print(f"Ошибка при захвате изображения: {e}")
            return None

    def solve_captcha_gemini(self, image: Image.Image) -> Optional[float]:
        buf = BytesIO()
        image.save(buf, format='PNG')
        base64_img = base64.b64encode(buf.getvalue()).decode('utf-8')
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [
                    {"text": "How many pixels should I move this slider to solve the puzzle? Give a number only."},
                    {"inlineData": {"mimeType": "image/png", "data": base64_img}}
                ]
            }]
        }
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
        try:
            resp = requests.post(url, json=data, headers=headers, timeout=40)
            rj = resp.json()
            print("Gemini ответ:", rj)
            answer = ""
            if 'candidates' in rj and rj['candidates']:
                parts = rj['candidates'][0].get('content', {}).get('parts', [])
                if parts:
                    answer = parts[0].get('text', '')
            nums = re.findall(r"\d{2,4}", answer)
            if nums and 10 <= int(nums[0]) <= 500:
                return float(nums[0])
        except Exception as e:
            print(f"Gemini error: {e}")
        return None

    def human_like_drag(self, slider, target_distance: float) -> bool:
        try:
            box = slider.bounding_box()
            if not box:
                print("Не удалось получить координаты ползунка")
                return False

            # [1] Задержка перед началом - имитация реакции человека (например, 0.7-2.3 сек)
            think_delay = random.uniform(0.7, 2.3)
            print(f"Жду перед действием (имитируем раздумье): {think_delay:.2f} сек")
            time.sleep(think_delay)

            start_x = box['x'] + box['width'] / 2
            start_y = box['y'] + box['height'] / 2

            # [2] Наводим мышь к слайдеру с паузами (движение поступательно, не в одну линию)
            approach_steps = random.randint(5, 8)
            approach_path = []
            for i in range(approach_steps):
                progress = (i + 1) / approach_steps
                inter_x = start_x * progress + (start_x - 150) * (1 - progress) + random.uniform(-8, 8)
                inter_y = start_y + random.uniform(-3, 3)
                approach_path.append((inter_x, inter_y))
            # старт вне зоны, к кнопке с задержками
            self.page.mouse.move(start_x - 150, start_y + random.randint(-10, 10))
            for (x, y) in approach_path:
                self.page.mouse.move(x, y)
                time.sleep(random.uniform(0.06, 0.14))
            # финальное наведение точно на кнопку
            self.page.mouse.move(start_x, start_y)
            time.sleep(random.uniform(0.09, 0.20))

            # [3] Держим кнопку вниз
            self.page.mouse.down()
            time.sleep(random.uniform(0.03, 0.09))

            # [4] Движение с рывками, мини-ступеньками, неравномерно, иногда полностью останавливаемся или дергаем мышку назад или вниз
            path_steps = random.randint(18, 29)
            for i in range(path_steps):
                progress = (i + 1) / path_steps
                # "нервность" — иногда слегка уходим в минус/назад или чуть вниз
                jitter_back = -3 if (random.random() < 0.08 and i > 0) else 0
                jitter_x = random.uniform(-1.5, 1.5) + jitter_back
                jitter_y = random.uniform(-2.3, 2.3)
                if random.random() < 0.12 and i > 4:
                    # Иногда неожиданно делаем паузу прям секундную на середине!
                    print("Пауза внутри движения!")
                    time.sleep(random.uniform(0.12, 0.30))
                # делаем рывок более "ступенчатым"
                step_base = target_distance * progress
                extra_jerk = random.uniform(-2, 3) if (i % 7 == 0) else 0
                cur = step_base + jitter_x + extra_jerk
                self.page.mouse.move(start_x + cur, start_y + jitter_y)
                time.sleep(random.uniform(0.018, 0.057))
            # финальная точка (имитация недодвига и потом быстрого дохвата)
            self.page.mouse.move(start_x + target_distance - random.randint(1, 6), start_y + random.randint(-2, 2))
            time.sleep(random.uniform(0.07, 0.145))
            self.page.mouse.move(start_x + target_distance, start_y)
            time.sleep(random.uniform(0.06, 0.12))
            self.page.mouse.up()
            print("Человеческое движение завершено")
            return True
        except Exception as e:
            print(f"Ошибка drag: {e}")
            return False

    def move_slider_fixed_90_pixels(self):
        max_attempts = 10
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--window-size=1366,768',
            ])
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1366, 'height': 768}
            )
            page = context.new_page()
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru', 'en-US', 'en']});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                window.chrome = { runtime: {} };
            """)

            page.goto("https://www.vseinstrumenti.ru/", wait_until='networkidle')
            if page_contains_forbidden(self.page):
                assert False, "Тест остановлен: найден forbidden после открытия страницы"

            solver = SyncCaptchaSlider(page)
            result = solver.solve_with_retries(max_attempts=max_attempts)
            assert result, "Не удалось пройти капчу за 10 попыток"
            browser.close()

    @pytest.mark.parametrize("run", range(1))
    def captcha_solver_gemini_with_retries(self ,run):
        gemini_api_key = GEMINI_API_KEY
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--window-size=1366,768',
            ])
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1366, 'height': 768}
            )
            page = context.new_page()
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru', 'en-US', 'en']});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                window.chrome = { runtime: {} };
            """)

            page.goto("https://www.vseinstrumenti.ru/", wait_until='networkidle')
            solver = SyncCaptchaSlider(page, gemini_api_key=gemini_api_key)
            result = solver.solve_with_retries(gemini_mode=True, max_attempts=10)
            assert result, "Не удалось пройти капчу за 10 попыток"
            browser.close()
