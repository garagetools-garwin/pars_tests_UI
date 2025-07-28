from playwright.sync_api import sync_playwright
import random
import time
import csv


def human_like_delay():
    """Рандомные задержки между действиями"""
    time.sleep(random.uniform(0.5, 2.5))


def scroll_page(page):
    """Имитация человеческой прокрутки"""
    for _ in range(random.randint(2, 5)):
        page.evaluate(f"window.scrollBy(0, {random.randint(200, 500)})")
        human_like_delay()


def scrape_product_data(url):
    with sync_playwright() as p:
        # Настройка браузера с человекообразными параметрами
        browser = p.chromium.launch(
            headless=False,  # Для отладки
            slow_mo=100,  # Замедление действий
            args=[
                '--disable-blink-features=AutomationControlled',
                '--start-maximized'
            ]
        )

        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            viewport={'width': 1366, 'height': 768}
        )

        page = context.new_page()

        try:
            # Переход на страницу с рандомными задержками
            page.goto(url, timeout=60000)
            human_like_delay()
            scroll_page(page)

            # Сбор данных
            products = page.query_selector_all('.product-card')
            results = []

            for product in products:
                try:
                    name = product.query_selector('[data-qa="product-name"]').inner_text()
                    price = product.query_selector('[data-qa="product-price-current"]').inner_text()
                    link = product.query_selector('a.product-card__link').get_attribute('href')
                    results.append({
                        'name': name.strip(),
                        'price': price.strip(),
                        'link': 'https://www.vseinstrumenti.ru' + link if link else ''
                    })
                except Exception as e:
                    print(f"Ошибка парсинга карточки: {e}")
                    continue

            # Сохранение в CSV
            with open('products.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['name', 'price', 'link'])
                writer.writeheader()
                writer.writerows(results)

            # Сохранение сессии
            context.storage_state(path="auth.json")

            return results

        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            browser.close()


# Пример использования
if __name__ == "__main__":
    target_url = "https://www.vseinstrumenti.ru/category/ruchnoy-instrument-1307/"
    data = scrape_product_data(target_url)
    print(f"Собрано {len(data)} товаров")

# tests/test_vi.py
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.ui
def test_vseinstrumenti_prices(page: Page):
    """Тест парсинга цен с сайта"""
    page.goto("https://www.vseinstrumenti.ru/product/akkumulyatornaya-drel-shurupovert-sturm-cd3618-1596056/")
    time.sleep(15)  # Ожидание для ручного ввода капчи (если появится)

    # Ожидаем загрузку цены
    price_locator = page.locator('[data-qa="price-now"]')
    price_locator.wait_for(timeout=10000)  # Явное ожидание вместо sleep

    # Получаем цену и очищаем от лишних символов
    price_text = price_locator.first.inner_text().replace('\u2009', ' ').strip()  # Заменяем тонкий пробел

    # Сохраняем в файл с правильной кодировкой
    with open('prices.txt', 'w', encoding='utf-8') as f:
        f.write(f"Цена: {price_text}\n")

    # Для дебага выводим в консоль
    print(f"Успешно получена цена: {price_text}")


import requests

@pytest.mark.ui
def test_vseinstrumenti_price(page: Page):

# Список ссылок для проверки
    urls = [
        "https://www.vseinstrumenti.ru/product/stroitelnaya-dvuhkolesnaya-oblegchennaya-tachka-sibrteh-90l-230kg-689643-1213728/",
        "https://www.vseinstrumenti.ru/product/usilennaya-dvuhkolesnaya-stroitelnaya-tachka-denzel-obem-140-l-250-kg-koleso-15x6-00-6-69000-6647941/",
        "https://www.vseinstrumenti.ru/product/stroitelnaya-2-h-kolesnaya-usilennaya-tachka-palisad-gruzopodemnost-320-kg-obem-100-l-68923-1401230/",
        "https://www.vseinstrumenti.ru/product/krestovaya-silovaya-otvertka-ph-2-0h38mm-jtc-3466-766726/",
        "https://www.vseinstrumenti.ru/product/golovka-tortsevaya-3-4-torx-e24-110-udarnaya-jtc-j606e-e24-747330/",
        "https://www.vseinstrumenti.ru/product/kombinirovannyj-korotkij-klyuch-force-14mm-755s14-987989/",
        "https://www.vseinstrumenti.ru/product/nakidnoj-razemnyj-klyuch-dlya-trubok-force-12-mm-75112a-794748/",
        "https://www.vseinstrumenti.ru/product/dlinnogubtsy-jonnesway-p118"
    ]

    # Создаем словари для хранения результатов
    status_404 = []
    status_403 = []
    other_status = {}

    # Проходим по каждой ссылке
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            status_code = response.status_code

            # Распределяем по спискам в зависимости от статус-кода
            if status_code == 404:
                status_404.append(url)
            elif status_code == 403:
                status_403.append(url)
            else:
                other_status[url] = status_code

        except requests.exceptions.RequestException as e:
            other_status[url] = f"Error: {str(e)}"

    # Выводим результаты
    print("Ссылки с статусом 404:")
    for url in status_404:
        print(f"- {url}")

    print("\nСсылки с статусом 403:")
    for url in status_403:
        print(f"- {url}")

    print("\nОстальные ссылки с их статусами:")
    for url, status in other_status.items():
        print(f"- {url}: {status}")


import pytest
from playwright.sync_api import Page

import pytest
from playwright.sync_api import Page


@pytest.mark.ui
def test_vseinstrumenti_price(page: Page, manual_page_factory):
    # Инициализируем страницу с вашими настройками и куками
    page = manual_page_factory(role="vi_test")

    # Устанавливаем дополнительные заголовки
    page.set_extra_http_headers({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    })

    # Список ссылок для проверки
    urls = [
        "https://www.vseinstrumenti.ru/product/stroitelnaya-dvuhkolesnaya-oblegchennaya-tachka-sibrteh-90l-230kg-689643-1213728/",
        "https://www.vseinstrumenti.ru/product/usilennaya-dvuhkolesnaya-stroitelnaya-tachka-denzel-obem-140-l-250-kg-koleso-15x6-00-6-69000-6647941/",
        "https://www.vseinstrumenti.ru/product/stroitelnaya-2-h-kolesnaya-usilennaya-tachka-palisad-gruzopodemnost-320-kg-obem-100-l-68923-1401230/",
        "https://www.vseinstrumenti.ru/product/krestovaya-silovaya-otvertka-ph-2-0h38mm-jtc-3466-766726/",
        "https://www.vseinstrumenti.ru/product/golovka-tortsevaya-3-4-torx-e24-110-udarnaya-jtc-j606e-e24-747330/",
        "https://www.vseinstrumenti.ru/product/kombinirovannyj-korotkij-klyuch-force-14mm-755s14-987989/",
        "https://www.vseinstrumenti.ru/product/nakidnoj-razemnyj-klyuch-dlya-trubok-force-12-mm-75112a-794748/",
        "https://www.vseinstrumenti.ru/product/dlinnogubtsy-jonnesway-p118"
    ]

    status_404 = []
    status_403 = []
    other_status = {}

    for url in urls:
        try:
            # Добавляем задержку между запросами (1 секунда)
            page.wait_for_timeout(1000)

            response = page.goto(url, timeout=15000, wait_until="networkidle")
            status_code = response.status

            if status_code == 404:
                status_404.append(url)
            elif status_code == 403:
                status_403.append(url)
            else:
                other_status[url] = status_code

            # Для отладки: делаем скриншот каждой страницы
            page.screenshot(path=f"screenshot_{url.split('/')[-2]}.png")

        except Exception as e:
            other_status[url] = f"Error: {str(e)}"
            # Скриншот при ошибке
            page.screenshot(path=f"error_{url.split('/')[-2]}.png")

    # Вывод результатов
    print("\nРезультаты проверки:")
    if status_404:
        print("\nСсылки с 404 ошибкой:")
        for url in status_404:
            print(f"- {url}")

    if status_403:
        print("\nСсылки с 403 ошибкой:")
        for url in status_403:
            print(f"- {url}")

    if other_status:
        print("\nОстальные статусы:")
        for url, status in other_status.items():
            print(f"- {url}: {status}")

    # Проверяем, что нет критических ошибок
    assert not status_404, f"Найдены битые ссылки (404): {status_404}"
    assert not status_403, f"Найдены запрещённые ссылки (403): {status_403}"