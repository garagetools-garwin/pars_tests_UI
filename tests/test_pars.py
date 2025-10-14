import time
import re

import allure
import csv
import os
import random
import time
import pytest
import allure
from playwright.sync_api import Page
from widgets.capcha_solver import SyncCaptchaSlider, page_contains_forbidden
import math


"""Хороший тест с рабочими куками, но куки сделаные локально не подходят для CI"""

# #TODO Убрать все лишнее куки не работают
# # тест работает с куками в headless
# PRODUCT_URLS = [
#     "https://www.vseinstrumenti.ru/product/kombinirovannyj-korotkij-klyuch-force-14mm-755s14-987989/",
#     "https://www.vseinstrumenti.ru/product/nakidnoj-razemnyj-klyuch-dlya-trubok-force-12-mm-75112a-794748/",
#     "https://www.vseinstrumenti.ru/product/topor-800-g-fiberglasovoe-toporische-matrix-21647-534021/",
#     "https://www.vseinstrumenti.ru/product/drel-shurupovert-aeg-bs18g4-202c-4935478630-1760653/",
#     "https://www.vseinstrumenti.ru/product/zakrytye-ochki-soyuzspetsodezhda-rosomz-3h11-panorama-prozrachnye-2000000168654-3576162/",
#     "https://www.vseinstrumenti.ru/product/dlinnogubtsy-jonnesway-p118/"
# ]
#
# OUTPUT_FILE = "prices.csv"
# PRICE_LOCATOR = '[data-qa="price-now"]'
#
#
# #TODO Убрать все лишнее куки не работают
# # тест работает с куками в headless
# @pytest.mark.parametrize("url", PRODUCT_URLS)
# @allure.title("Сбор цены с имитацией поведения пользователя")
# def test_get_price_human_like(page_fixture, url):
#     page = page_fixture(role="vi_test")
#     solver = SyncCaptchaSlider(page)
#
#     with allure.step("Переход на главную и прогрев страницы"):
#         page.goto("https://www.vseinstrumenti.ru/", wait_until="domcontentloaded")
#         human_delay(1.2, 2.5)
#
#     with allure.step(f"Переход на товар: {url}"):
#         page.goto(url, wait_until="domcontentloaded")
#
#     human_delay(2, 3)
#
#     with allure.step("Имитируем поведение пользователя: скролл и мышь"):
#         for i in range(0, random.randint(400, 1000), 150):
#             page.mouse.wheel(0, i)
#             human_delay(0.2, 0.5)
#         page.mouse.move(random.randint(100, 600), random.randint(200, 400), steps=10)
#         human_delay(0.5, 1.0)
#
#     with allure.step("Наводим курсор на цену и считываем"):
#         try:
#             price_element = page.locator(PRICE_LOCATOR)
#             price_element.wait_for(timeout=10000)
#             box = price_element.bounding_box()
#             if not box:
#                 raise Exception("No bounding box for price")
#             page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=20)
#             # human_delay(0.5, 1.2)
#             price = price_element.inner_text().strip()
#             print(price)
#         except Exception:
#             price = "-"
#             print(f"Цена не найдена на {url}")
#
#     with allure.step("Сохраняем результат в CSV"):
#         save_to_csv(url, price)
#
#     with allure.step("Вывод результата"):
#         print(f"✔ {url} — {price}")
#         allure.attach(price, name="Цена", attachment_type=allure.attachment_type.TEXT)
#
#     assert "₽" in price or "не найдена" not in price.lower()
#
#
# # ---------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ----------
#
# def human_delay(min_sec=0.5, max_sec=1.5):
#     """Пауза как у человека"""
#     time.sleep(random.uniform(min_sec, max_sec))
#
#
# def save_to_csv(url: str, price: str):
#     file_exists = os.path.isfile(OUTPUT_FILE)
#     with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
#         writer = csv.writer(f)
#         if not file_exists:
#             writer.writerow(["URL", "Цена"])
#         writer.writerow([url, price])


# @allure.title("Открытие всех страниц по ролям")
# def test_open_vi(base_url, manual_page_factory):
#     page = manual_page_factory(role="vi_test")
#     page.goto("https://www.vseinstrumenti.ru/category/akkumulyatornye-dreli-shurupoverty-15/")
#     page.hover("data-qa=products-tile")
#     page.goto("https://www.vseinstrumenti.ru/")
#     time.sleep(20)
#
#
#
# import csv
# import os
# import time
# import random
# import pytest
# import allure
# from playwright.sync_api import Page, Locator
#
# PRODUCT_URLS = [
#     "https://www.vseinstrumenti.ru/product/topor-800-g-fiberglasovoe-toporische-matrix-21647-534021/",
#     "https://www.vseinstrumenti.ru/product/drel-shurupovert-aeg-bs18g4-202c-4935478630-1760653/",
#     "https://www.vseinstrumenti.ru/product/dlinnogubtsy-jonnesway-p118"
# ]
#
# OUTPUT_FILE = "prices.csv"
# PRICE_LOCATOR = '[data-qa="price-now"]'
#
#
# def human_delay(min_sec=0.5, max_sec=1.5):
#     """Пауза как у человека."""
#     time.sleep(random.uniform(min_sec, max_sec))
#
#
# @pytest.mark.parametrize("url", PRODUCT_URLS)
# @allure.title("Сбор цены с имитацией поведения пользователя")
# def test_get_price_human_like(page_fixture, url: str):
#     page = page_fixture(role="vi_test")
#
#     with allure.step(f"Открываем страницу товара {url}"):
#         page.goto(url, timeout=60000)
#         human_delay(1, 2)
#
#     with allure.step("Имитируем просмотр страницы"):
#         page.mouse.move(random.randint(100, 400), random.randint(100, 400))
#         human_delay()
#         page.mouse.wheel(0, random.randint(300, 1000))  # скроллим вниз
#         human_delay()
#
#     with allure.step("Наводим мышку на цену"):
#         price_element = page.locator(PRICE_LOCATOR)
#         price_element.wait_for(timeout=15000)
#         box = price_element.bounding_box()
#         if box:
#             page.mouse.move(box["x"] + 5, box["y"] + 5)
#             human_delay()
#
#     with allure.step("Извлекаем цену"):
#         price = price_element.inner_text().strip()
#         assert price, "Цена не найдена!"
#
#     with allure.step("Сохраняем результат в CSV"):
#         file_exists = os.path.isfile(OUTPUT_FILE)
#         with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
#             writer = csv.writer(f)
#             if not file_exists:
#                 writer.writerow(["URL", "Цена"])
#             writer.writerow([url, price])
#
#     with allure.step("Вывод результата"):
#         print(f"✔ {url} — {price}")



"""Тест законсервирован до лучших времен куки с автоматизации не подходят"""

# import csv
# import os
# import random
# import time
# import pytest
# import allure
# from playwright.sync_api import Page
# from widgets.capcha_solver import SyncCaptchaSlider, page_contains_forbidden
#
#
# PRODUCT_URLS = [
#     "https://www.vseinstrumenti.ru/product/topor-800-g-fiberglasovoe-toporische-matrix-21647-534021/",
#     "https://www.vseinstrumenti.ru/product/drel-shurupovert-aeg-bs18g4-202c-4935478630-1760653/",
#     "https://www.vseinstrumenti.ru/product/zakrytye-ochki-soyuzspetsodezhda-rosomz-3h11-panorama-prozrachnye-2000000168654-3576162/",
#     "https://www.vseinstrumenti.ru/product/dlinnogubtsy-jonnesway-p118/"
# ]
#
# OUTPUT_FILE = "prices.csv"
# PRICE_LOCATOR = '[data-qa="price-now"]'
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
#              "AppleWebKit/537.36 (KHTML, like Gecko) " \
#              "Chrome/122.0.0.0 Safari/537.36"
#
#
# # тест работает с куками в headless
# @pytest.mark.parametrize("url", PRODUCT_URLS)
# @allure.title("Сбор цены с имитацией поведения пользователя")
# def test_get_price_human_like_2(page_fixture, url):
#     page = page_fixture()
#     solver = SyncCaptchaSlider(page)
#
#     # Паттерн антибан настроек
#     page.context.set_extra_http_headers({"User-Agent": USER_AGENT})
#     page.set_viewport_size({"width": 1366, "height": 768})
#     page.add_init_script("""
#     // Отключаем webdriver и подсовываем более "живой" fingerprint
#     Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
#     Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru', 'en-US', 'en']});
#     Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5, 6]});
#     window.chrome = { runtime: {} };
#
#     // Fingerprint: canvas spoof, audio spoof
#     const getFakeData = () => new Uint8ClampedArray([128,128,128,255,128,128,128,255]);
#     HTMLCanvasElement.prototype.toDataURL = function(){ return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Zw8AAjMBi/MaaWkAAAAASUVORK5CYII="; }
#     window.OffscreenCanvas = HTMLCanvasElement;
#
#     // UserAgent spoof внутри navigator (для некоторых js-антиботов)
#     const _orig_ua = navigator.userAgent;
#     Object.defineProperty(navigator, 'userAgent', { get: () => _orig_ua });
#
#     // Timezone spoof
#     Intl.DateTimeFormat = function() { return { resolvedOptions: () => ({ timeZone: 'Europe/Moscow' }) } }
# """)
#
#     with allure.step("Переход на главную и прогрев страницы"):
#         # Заходим на яндекс и ищем "Все инструменты"
#         page.goto("https://mail.ru/", timeout=60000)
#         human_delay(1, 2)
#         search_box = page.locator('input[name="search_source"]')
#         search_box.type("Все инструменты",200)
#         page.keyboard.press("Enter")
#         # Ждём появления результатов и ссылки на vseinstrumenti.ru, кликаем на первую (или где вхождение)
#         page.wait_for_selector('a[href*="vseinstrumenti.ru"]', timeout=60000)
#         first_link = page.locator('a[href*="vseinstrumenti.ru"]').first
#         first_link.click()
#         # Ждём загрузки целевого сайтаhref="https://www.vseinstrumenti.ru/"
#         page.wait_for_url("https://www.vseinstrumenti.ru/*", timeout=15000)
#
#         # Проверяем принудительно — вдруг редирект на /xpvnsulc (или другая капча)
#         curr_url = page.url
#         if re.search(r"/xpvnsulc|forbidden", curr_url) or page_contains_forbidden(page):
#             # Сразу решаем капчу!
#             solver.capcha_solver()
#
#     with allure.step("Проверка 'forbidden' на главной"):
#         if page_contains_forbidden(page):
#             assert False, "Тест остановлен: найден forbidden после перехода на главную"
#
#     with allure.step("Проверка наличия капчи на главной"):
#         solver.capcha_solver()
#
#     human_delay(1.2, 2.5)
#
#     # # Имитируем поведение настоящего браузера
#     # page.context.set_extra_http_headers({"User-Agent": USER_AGENT})
#     #
#     # with allure.step("Переход на главную и прогрев страницы"):
#     #     page.goto("https://www.vseinstrumenti.ru/", wait_until="domcontentloaded")
#     #     human_delay(1.2, 2.5)
#
#
#
#     # with allure.step(f"Переход на товар: {url}"):
#     #     page.goto(url, wait_until="load", timeout=60000)
#     #     human_delay(2, 3)
#
#     with allure.step(f"Переход на товар: {url}"):
#         page.goto(url, wait_until="load", timeout=60000)
#         with allure.step("Go to товар, обработка антибота"):
#             print("Ура, мы на товаре:", page.url)
#         # Проверяем принудительно — вдруг редирект на /xpvnsulc (или другая капча)
#         curr_url = page.url
#         if re.search(r"/xpvnsulc|forbidden", curr_url) or page_contains_forbidden(page):
#             # Сразу решаем капчу!
#             solver.capcha_solver()
#
#     with allure.step(f"Проверка 'forbidden' на: {url}"):
#         if page_contains_forbidden(page):
#             assert False, "Тест остановлен: найден forbidden после перехода на url товара"
#
#     with allure.step(f"Проверка капчи на: {url}"):
#         solver.capcha_solver()
#
#     human_delay(2, 3)
#
#     with allure.step("Имитируем поведение пользователя: скролл и мышь"):
#         for i in range(0, random.randint(400, 1000), 150):
#             page.mouse.wheel(0, i)
#             human_delay(0.2, 0.5)
#         page.mouse.move(random.randint(100, 600), random.randint(200, 400), steps=10)
#         human_delay(0.5, 1.0)
#
#     with allure.step("Наводим курсор на цену и считываем"):
#         try:
#             price_element = page.locator(PRICE_LOCATOR)
#             price_element.wait_for(timeout=10000)
#             box = price_element.bounding_box()
#             if not box:
#                 raise Exception("No bounding box for price")
#             page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=20)
#             human_delay(0.5, 1.2)
#             price = price_element.inner_text().strip()
#         except Exception:
#             price = "-"
#             print(f"Цена не найдена на {url}")
#
#     with allure.step("Сохраняем результат в CSV"):
#         save_to_csv(url, price)
#
#     with allure.step("Вывод результата"):
#         print(f"✔ {url} — {price}")
#         allure.attach(price, name="Цена", attachment_type=allure.attachment_type.TEXT)
#
#     assert "₽" in price or "не найдена" not in price.lower()
#
#
# # ---------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ----------
#
# def human_delay(min_sec=0.5, max_sec=1.5):
#     """Пауза как у человека"""
#     time.sleep(random.uniform(min_sec, max_sec))
#
#
# def save_to_csv(url: str, price: str):
#     file_exists = os.path.isfile(OUTPUT_FILE)
#     with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
#         writer = csv.writer(f)
#         if not file_exists:
#             writer.writerow(["URL", "Цена"])
#         writer.writerow([url, price])

#TODO на каждой странице проверять либо цену либо отсутствие цены (нет в наличии), либо капчу
#TODO
"""Тест законсервирован до лучших времен куки с автоматизации не подходят"""
# def test_ip(page_fixture):
#     page = page_fixture()
#     page.goto("https://httpbin.org/ip")
#     ip_info = page.text_content("body")
#     print(ip_info)


"""Начало рабочего теста"""

import csv
import os
import random
import time
import pytest
import allure
import datetime
from playwright.sync_api import Page
from widgets.capcha_solver import SyncCaptchaSlider, page_contains_forbidden


PRODUCT_URLS = [
    "https://www.vseinstrumenti.ru/product/maslobenzostojkie-perchatki-zubr-mehanik-razmer-xl-11276-xl-z01-1590156/",
    "https://www.vseinstrumenti.ru/product/elastichnye-perchatki-kraftool-expert-r-l-so-vspenennym-nitrilovym-pokrytiem-11285-l-1272671/",
    "https://www.vseinstrumenti.ru/product/otvertka-sl6-0h100-mm-matrix-fusion-anti-slip-11423-549863/",
    "https://www.vseinstrumenti.ru/product/nabor-otvertok-matrix-fusion-18-sht-11452-768422/",
    "https://www.vseinstrumenti.ru/product/montazhnyj-blok-s-kryukom-tor-hqg-l-k1-3-2-t-11531-782411/",
    "https://www.vseinstrumenti.ru/product/bita-s-tortsevoj-golovkoj-magnitnaya-8-mm-65-mm-2-sht-matrix-11573-783696/",
    "https://www.vseinstrumenti.ru/product/strop-tekstilnyj-petlevoj-lim-stp-10-4-300-mm-stp-10-0-4-0-14802845/",
    "https://www.vseinstrumenti.ru/product/tekstilnyj-petlevoj-strop-tor-stp-1-0-t-2-0-m-30-mm-11612-695231/",
    "https://www.vseinstrumenti.ru/product/tekstilnyj-petlevoj-strop-tor-stp-1-0-t-3-0-m-30-mm-11613-695235/",
    "https://www.vseinstrumenti.ru/product/tekstilnyj-petlevoj-strop-tor-stp-1-0-t-4-0-m-30-mm-11614-695247/",
    "https://www.vseinstrumenti.ru/product/tekstilnyj-petlevoj-strop-tor-stp-2-0-t-4-0-m-60-mm-11624-695284/",
    "https://www.vseinstrumenti.ru/product/tekstilnyj-petlevoj-strop-tor-stp-3-0-t-3-0-m-90-mm-11633-695334/",
    "https://www.vseinstrumenti.ru/product/tekstilnyj-petlevoj-strop-tor-stp-3-0-t-4-0-m-90-mm-11634-695342/",
    "https://www.vseinstrumenti.ru/product/tekstilnyj-petlevoj-strop-tor-stp-3-0-t-5-0-m-90-mm-11635-695354/",
    "https://www.vseinstrumenti.ru/product/tekstilnyj-petlevoj-strop-tor-stp-5-0-t-4-0-m-150-mm-11654-695391/",
    "https://www.vseinstrumenti.ru/product/tekstilnyj-petlevoj-strop-tor-stp-5-0-t-6-0-m-150-mm-11656-695418/",
    "https://www.vseinstrumenti.ru/product/metchik-ipk-m-r-m14-1-5-k-t-2620-15592620-15573-2170544/",
    "https://www.vseinstrumenti.ru/product/metchik-ipk-m-r-m33h2-0-k-t-2620-20072620-20053-4868923/",
    "https://www.vseinstrumenti.ru/product/metchik-ipk-m-r-m36-4-0-osn-r6m5-2620-20593-2170564/",
    "https://www.vseinstrumenti.ru/product/metchik-ipk-m-r-m30h3-0-r6m5-2620-19493-8612342/",
    "https://www.vseinstrumenti.ru/product/metchik-ipk-m-r-m42x4-5-osn-r6m5-2620-21673-3038234/",
    "https://www.vseinstrumenti.ru/product/metchik-ipk-m-r-m12-1-5-r6m5-2620-15053-2170514/",
    "https://www.vseinstrumenti.ru/product/lenta-malyarnaya-krepovaya-48-mm-50-m-ekspert-zubr-12115-50-224079/",
    "https://www.vseinstrumenti.ru/product/nabor-kombinirovannyh-klyuchej-10-32-mm-chehol-iz-tetorona-14-predmetov-king-tony-1214mrn-1077685/",
    "https://www.vseinstrumenti.ru/product/nabor-kombinirovannyh-klyuchej-10-32-mm-chehol-iz-tetorona-14-predmetov-king-tony-1214mrn-1077685/",
    "https://www.vseinstrumenti.ru/product/vertikalnyj-zahvat-tor-dhql-g-p-1-0-t-list-0-20-mm-12214-763251/",
    "https://www.vseinstrumenti.ru/product/gorizontalnyj-zahvat-tor-dhqa-g-p-2-0-t-list-0-40-mm-12223-782569/",
    "https://www.vseinstrumenti.ru/product/vertikalnyj-zahvat-tor-dhql-g-p-2-0-t-list-0-25-mm-12224-782587/",
    "https://www.vseinstrumenti.ru/product/balochnyj-zahvat-tor-lj-q-2-g-p-2-t-12226-782473/",
    "https://www.vseinstrumenti.ru/product/signalnaya-lenta-zubr-master-tsvet-krasno-belyj-50mm-h-200m-12240-50-200-958886/",
    "https://www.vseinstrumenti.ru/product/signalnaya-lenta-zubr-master-tsvet-krasno-belyj-75mm-h-200m-12240-75-200-958691/",
    "https://www.vseinstrumenti.ru/product/signalnaya-lenta-stayer-master-tsvet-krasno-belyj-75mm-h-150m-12241-75-150-958481/",
    "https://www.vseinstrumenti.ru/product/razmetochnaya-klejkaya-lenta-zubr-professional-tsvet-krasno-belyj-50mm-h-25m-12248-50-25-958786/",
    "https://www.vseinstrumenti.ru/product/razmetochnaya-klejkaya-lenta-zubr-professional-tsvet-cherno-zheltyj-50mm-h-25m-12249-50-25-958785/",
    "https://www.vseinstrumenti.ru/product/omegoobraznaya-skoba-tor-2-0-t-tip-g209-1230204-782508/",
    "https://www.vseinstrumenti.ru/product/omegoobraznaya-skoba-tor-3-25-t-tip-g209-1233254-783651/",
    "https://www.vseinstrumenti.ru/product/omegoobraznaya-skoba-tor-4-75-t-tip-g209-1234754-783652/",
    "https://www.vseinstrumenti.ru/product/omegoobraznaya-skoba-tor-6-5-t-tip-g2130-1236506-1619862/",
    "https://www.vseinstrumenti.ru/product/omegoobraznaya-skoba-tor-8-5-t-tip-g209-1238504-782510/",
    "https://www.vseinstrumenti.ru/product/kislorodnyj-manometr-bamz-mp-50-1240003-977797/",
    "https://www.vseinstrumenti.ru/product/propanovyj-manometr-kedr-mp-50-1240005-977795/",
    "https://www.vseinstrumenti.ru/product/snegovaya-lopata-tsentroinstrument-finland-s-cherenkom-1243-ch-767680/",
    "https://www.vseinstrumenti.ru/product/trubnaya-plashka-ipk-g-1-1-2-2654-0177-2433838/",
    "https://www.vseinstrumenti.ru/product/plashkoderzhatel-ipk-m12-m20-g1-4-g1-2-posad-d57x38-45-mm-l-355-mm-r-plashderm12-m20r-2186707/",
    "https://www.vseinstrumenti.ru/product/vysokotochnaya-nasadka-m10-x-1-13-mm-pressol-12626-852510/",
    "https://www.vseinstrumenti.ru/product/smazochnaya-nasadka-m10h1-diametr-15-mm-pressol-12631-852519/",
    "https://www.vseinstrumenti.ru/product/vysokotochnaya-nasadka-m10h1-diametr-15mm-pressol-12643-852507/",
    "https://www.vseinstrumenti.ru/product/shlang-m10h1-11h500mm-pressol-12665-852196/",
    "https://www.vseinstrumenti.ru/product/trubka-izognutaya-makita-126756-8-8267193/",
    "https://www.vseinstrumenti.ru/product/professionalnyj-usilennyj-shprits-pressol-m-10x1-12685780-811239/",
    "https://www.vseinstrumenti.ru/product/professionalnyj-usilennyj-shprits-pressol-m-10x1-12686780-811240/",
    "https://www.vseinstrumenti.ru/product/professionalnyj-usilennyj-shprits-pressol-m-10x1-12695-811241/",
    "https://www.vseinstrumenti.ru/product/protirochnaya-bumaga-v-rulone-zubr-23h35-sm-1000-listov-12820-23-1619820/",
    "https://www.vseinstrumenti.ru/product/reversivnaya-kombinirovannaya-otvertka-sibrteh-ph2-sl6-13368-779234/",
    "https://www.vseinstrumenti.ru/product/nabor-klyuchej-trubchatyh-tortsevyh-7-pr-matrix-13719-946502/",
    "https://www.vseinstrumenti.ru/product/freza-otreznaya-tip-2-200h2-0h32-mm-80z-p6m5-ipk-2254-1324-2400106/",
    "https://www.vseinstrumenti.ru/product/freza-otreznaya-tip-2-80h1-6h22-mm-48z-p6m5-ipk-2254-1208-2400460/",
    "https://www.vseinstrumenti.ru/product/molotok-svarschika-shlakootbojnyj-doka-sn-01-dk-0000-03529-1600897/",
    "https://www.vseinstrumenti.ru/product/nabor-instrumentov-stels-82-predmeta-14105-v-chemodane-729601/",
    "https://www.vseinstrumenti.ru/product/nabor-instrumentov-stels-14106-94-predmeta-783966/",
    "https://www.vseinstrumenti.ru/product/nabor-instrumentov-142-sht-stels-14107-729638/",
    "https://www.vseinstrumenti.ru/product/nabor-tortsevyh-golovok-stels-1-2-11-predmetov-14127-720671/",
    "https://www.vseinstrumenti.ru/product/rozhkovyj-klyuch-8x10-mm-zheltyj-tsink-sibrteh-14303-948443/",
    "https://www.vseinstrumenti.ru/product/rozhkovyj-klyuch-17x19-mm-crv-fosfatirovannyj-gost-2839-sibrteh-14328-948437/",
    "https://www.vseinstrumenti.ru/product/rozhkovyj-klyuch-22h24-mm-sibrteh-14330-548661/",
    "https://www.vseinstrumenti.ru/product/rozhkovyj-klyuch-30h32-mm-sibrteh-14332-548663/",
    "https://www.vseinstrumenti.ru/product/rozhkovyj-klyuch-32h36-mm-sibrteh-14333-548664/",
    "https://www.vseinstrumenti.ru/product/polotno-po-metallu-3014-150-bi-metal-5-sht-150h19h0-9-mm-130-mm-18-tpi-wilpu-1441500005-793384/",
    "https://www.vseinstrumenti.ru/product/polotno-po-metallu-3014-200-bi-metall-5-sht-200h19h0-9-mm-180-mm-18-tpi-wilpu-1442000005-793385/",
    "https://www.vseinstrumenti.ru/product/nabor-kombinirovannyh-treschotochnyh-klyuchej-13-sht-matrix-14797-1150898/",
    "https://www.vseinstrumenti.ru/product/kombinirovannyj-treschotochnyj-klyuch-30mm-crv-zerkalnyj-hrom-matrix-14817-1092282/",
    "https://www.vseinstrumenti.ru/product/nozhovka-po-derevu-pila-stayer-cobra-5-500-mm-5-tpi-1506-50-z02-1171654/",
    "https://www.vseinstrumenti.ru/product/freza-shponochnaya-20h88-mm-ts-h-ipk-2234-0383-2491118/",
    "https://www.vseinstrumenti.ru/product/freza-kontsevaya-tverdosplavnaya-10-mm-ts-h-z-4-vk8-ipk-frezvk8ch10z-4-4735464/",
    "https://www.vseinstrumenti.ru/product/press-maslenka-pressol-15113140-1372026/",
    "https://www.vseinstrumenti.ru/product/freza-kontsevaya-36h155-mm-mk3-z-6-ipk-2223-0156-2194483/",
    "https://www.vseinstrumenti.ru/product/freza-kontsevaya-40h188-mm-mk4-z-6-ipk-2223-0019-2978312/",
    "https://www.vseinstrumenti.ru/product/nozhovka-dlya-tochnogo-reza-kraftool-alligator-black-400-mm-11-tpi-3d-zub-15205-40-1291984/",
    "https://www.vseinstrumenti.ru/product/nozhovka-kraftool-expert-kraftmax-laminator-spetsialnyj-zakalennyj-zub-bystryj-i-tochnyj-rez-13-14-tpi-500mm-15225-50-1245747/",
    "https://www.vseinstrumenti.ru/product/razvodnoj-klyuch-150-mm-matrix-15501-516861/",
    "https://www.vseinstrumenti.ru/product/razvodnoj-klyuch-200-mm-matrix-15503-543590/",
    "https://www.vseinstrumenti.ru/product/razvodnoj-klyuch-250-mm-matrix-15505-551013/",
    "https://www.vseinstrumenti.ru/product/razvodnoj-klyuch-300-mm-matrix-15507-543617/",
    "https://www.vseinstrumenti.ru/product/razvodnoj-klyuch-375-mm-matrix-15509-543917/",
    "https://www.vseinstrumenti.ru/product/razvodnoj-klyuch-450-mm-matrix-15511-518741/",
    "https://www.vseinstrumenti.ru/product/razvodnoj-klyuch-sibrteh-tonkie-gubki-fosfatirovanyj-250-mm-15536-982115/",
    "https://www.vseinstrumenti.ru/product/professionalnyj-disk-otreznoj-po-metallu-t41-230h3-0h22-2-profi-cutop-40007t-842716/",
    "https://www.vseinstrumenti.ru/product/professionalnyj-disk-otreznoj-po-metallu-t41-400h4-0h32-profi-cutop-40011t-842721/",
    "https://www.vseinstrumenti.ru/product/disk-otreznoj-po-metallu-150h1-6h22-2-mm-cutop-40012t-1578961/",
    "https://www.vseinstrumenti.ru/product/disk-otreznoj-po-metallu-master-125h2-5h22-2-mm-greatflex-40014t-2196027/",
    "https://www.vseinstrumenti.ru/product/disk-professionalnyj-otreznoj-po-metallu-i-nerzhaveyuschej-stali-t41-230h1-6h22-2-mm-cutop-40016t-1576510/",
    "https://www.vseinstrumenti.ru/product/elektrody-svarochnye-zubr-uoni-13-55-s-osnovnym-pokrytiem-3h350-mm-5-kg-40025-3-0-1866143/",
    "https://www.vseinstrumenti.ru/product/elektrody-svarochnye-zubr-uoni-13-55-s-osnovnym-pokrytiem-4h450-mm-5-kg-40025-4-0-1866147/",
    "https://www.vseinstrumenti.ru/product/elektrody-svarochnye-zubr-professional-zok-46-s-rutil-tsellyuloznym-pokrytiem-2-5h350-mm-1-5-kg-40031-2-5-1610122/",
    "https://www.vseinstrumenti.ru/product/elektrody-svarochnye-zubr-professional-zok-46-s-rutil-tsellyuloznym-pokrytiem-3h350-mm-5-kg-40035-3-0-1866144/",
    "https://www.vseinstrumenti.ru/product/ploskaya-kist-zubr-lazur-master-4-01009-063-216613/",
    "https://www.vseinstrumenti.ru/product/zaklepki-alyuminij-stal-50-sht-4-8x16-mm-matrix-40665-1059852/",
    "https://www.vseinstrumenti.ru/product/teflonovyj-pistolet-dlya-montazhnoj-peny-zubr-montazhnik-4-06875-z02-1457805/",
    "https://www.vseinstrumenti.ru/product/nasadka-uglovaya-d36-mm-seraya-makita-410306-2-8267523/",
    "https://www.vseinstrumenti.ru/product/nabor-schupov-chiz-n2-100mm-0-02-0-5-54567-1280421/",

    ]

OUTPUT_FILE = "prices.csv"
CURRENT_PRICE = '[data-qa="price-now"]'
PERSONAL_PRICE = '[data-qa="personal-price"] a span:has-text("₽")'
CITY_SELECTION_BUTTON = "button span:has-text('Указать другой')"
MOSCOW_BUTTON = '[data-qa="location"] p:has-text("Москва")'
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"


def load_random_urls(file_path, count=100):
    """
    Загружает случайную выборку URL из файла

    Args:
        file_path (str): Путь к файлу с URL (каждый URL на новой строке)
        count (int): Количество случайных URL для выбора

    Returns:
        list: Список случайно выбранных URL
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            all_urls = [line.strip() for line in f if line.strip()]

        if len(all_urls) < count:
            print(f"Внимание: в файле только {len(all_urls)} URL, а запрошено {count}")
            return all_urls

        random_urls = random.sample(all_urls, count)
        print(f"Выбрано {len(random_urls)} случайных URL из {len(all_urls)} доступных")
        return random_urls

    except FileNotFoundError:
        print(f"Файл {file_path} не найден!")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        return []


def load_random_urls_from_csv(csv_file_path, url_column=0, count=100):
    """Загружает случайные URL из CSV файла"""
    try:
        all_urls = []
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > url_column and row[url_column].strip():
                    all_urls.append(row[url_column].strip())

        if len(all_urls) < count:
            print(f"Внимание: в CSV файле только {len(all_urls)} URL, а запрошено {count}")
            return all_urls

        random_urls = random.sample(all_urls, count)
        print(f"Выбрано {len(random_urls)} случайных URL из {len(all_urls)} доступных (CSV)")
        return random_urls

    except FileNotFoundError:
        print(f"CSV файл {csv_file_path} не найден!")
        return []
    except Exception as e:
        print(f"Ошибка при чтении CSV файла {csv_file_path}: {e}")
        return []


def human_delay(min_sec=0.5, max_sec=1.5):
    """Создает случайную задержку, имитирующую поведение человека"""
    time.sleep(random.uniform(min_sec, max_sec))


def save_to_csv(url: str, price: str):
    """Сохраняет результат в CSV файл"""
    today = datetime.date.today().isoformat()
    file_exists = os.path.isfile(OUTPUT_FILE)
    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Дата", "URL", "Цена"])
        writer.writerow([today, url, price])


# Конфигурация
URLS_FILE_PATH = "all_product_urls.txt"  # Путь к файлу со всеми URL
RANDOM_URLS_COUNT = 100  # Количество случайных URL для обработки
OUTPUT_FILE = "prices.csv"


@allure.title("Сбор цен по всем товарам одним тестом")
def test_get_all_prices_human_like_2(page_fixture):
    page = page_fixture()
    solver = SyncCaptchaSlider(page)
    price_results = []

    # Загружаем случайные URL из файла
    with allure.step(f"Загрузка {RANDOM_URLS_COUNT} случайных URL из файла"):
        if URLS_FILE_PATH.endswith('.txt'):
            product_urls = load_random_urls(URLS_FILE_PATH, RANDOM_URLS_COUNT)
        elif URLS_FILE_PATH.endswith('.csv'):
            product_urls = load_random_urls_from_csv(URLS_FILE_PATH, url_column=0, count=RANDOM_URLS_COUNT)
        else:
            product_urls = load_random_urls(URLS_FILE_PATH, RANDOM_URLS_COUNT)

        if not product_urls:
            pytest.fail(f"Не удалось загрузить URL из файла {URLS_FILE_PATH}")

        allure.attach(
            f"Загружено {len(product_urls)} URL из файла {URLS_FILE_PATH}",
            name="Информация о загрузке",
            attachment_type=allure.attachment_type.TEXT
        )

    # Паттерн антибан настроек
    # page.context.set_extra_http_headers({"User-Agent": USER_AGENT})
    # page.set_viewport_size({"width": 1920, "height": 1080})
    # page.add_init_script("""
    #     Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
    #     Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru', 'en-US', 'en']});
    #     Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5, 6]});
    #     window.chrome = { runtime: {} };
    #     const getFakeData = () => new Uint8ClampedArray([128,128,128,255,128,128,128,255]);
    #     HTMLCanvasElement.prototype.toDataURL = function(){ return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Zw8AAjMBi/MaaWkAAAAASUVORK5CYII="; }
    #     window.OffscreenCanvas = HTMLCanvasElement;
    #     const _orig_ua = navigator.userAgent;
    #     Object.defineProperty(navigator, 'userAgent', { get: () => _orig_ua });
    #     Intl.DateTimeFormat = function() { return { resolvedOptions: () => ({ timeZone: 'Europe/Moscow' }) } }
    # """)

    with allure.step("Переход на главную и прогрев страницы"):
        page.goto("https://abrahamjuliot.github.io/creepjs/")
        # Даем сайту полностью загрузиться и просчитать проценты
        page.wait_for_timeout(4000)
        # Парсим проценты из DOM
        like_headless = page.locator("text=like headless").locator("xpath=../following-sibling::div").first.inner_text()
        headless = page.locator("text=headless").locator("xpath=../following-sibling::div").first.inner_text()
        print(f"like headless: {like_headless}")
        print(f"headless: {headless}")    page.goto("https://abrahamjuliot.github.io/creepjs/")
        # Даем сайту полностью загрузиться и просчитать проценты
        page.wait_for_timeout(4000)
        # Парсим проценты из DOM
        like_headless = page.locator("text=like headless").locator("xpath=../following-sibling::div").first.inner_text()
        headless = page.locator("text=headless").locator("xpath=../following-sibling::div").first.inner_text()
        print(f"like headless: {like_headless}")
        print(f"headless: {headless}")
        # page.goto("https://api.ipify.org")
        # ip = page.text_content("body").strip()
        # print("Мой реальный внешний IP:", ip)
        page.mouse.move(200, 250)
        page.mouse.down()
        page.mouse.up()
        page.wait_for_timeout(random.randint(800, 2500))
        page.keyboard.type('hello')
        page.mouse.move(400, 600)
        page.goto("https://www.vseinstrumenti.ru/", wait_until="domcontentloaded")
        page.mouse.move(200, 250)
        page.mouse.down()
        page.mouse.up()
        page.wait_for_timeout(random.randint(800, 2500))
        page.keyboard.type('hello')
        page.mouse.move(400, 600)
        human_delay(1.2, 2.5)

        curr_url = page.url
        if re.search(r"/xpvnsulc|forbidden", curr_url) or page_contains_forbidden(page):
            solver.capcha_solver()

        if page_contains_forbidden(page):
            assert False, "Тест остановлен: найден forbidden после перехода на главную"
        solver.capcha_solver()
        human_delay(1.2, 2.5)

        # # 50% шанс применить проверку с ошибкой
        # if random.random() < 0.5:
        #     print("🎲 Применяем намеренную проверку с ошибкой...")
        #     # Ваша проверка с ошибкой
        #     page.locator('//span[contains(translate(text(), "МОСКВАЧ", "москвач"), "москвач")]').wait_for(timeout=10000)
        # else:
        #     print("🎲 Пропускаем проверку с ошибкой...")

        page.locator('//span[contains(translate(text(), "МОСКВА", "москва"), "москва")]').wait_for(timeout=10000)
        # page.locator(CITY_SELECTION_BUTTON).click()
        # human_delay(1.2, 2.5)
        # page.locator(MOSCOW_BUTTON).wait_for(timeout=60000)
        # page.locator(MOSCOW_BUTTON).click()
        # human_delay(1.2, 2.5)

    for index, url in enumerate(product_urls, 1):
        with allure.step(f"Обработка товара {index}/{len(product_urls)}: {url}"):
            page.goto(url, wait_until="load", timeout=60000)
            with allure.step("Go to товар, обработка антибота"):
                print("Ура, мы на товаре:", page.url)
            curr_url = page.url
            if re.search(r"/xpvnsulc|forbidden", curr_url) or page_contains_forbidden(page):
                solver.capcha_solver()

            if page_contains_forbidden(page):
                assert False, f"Тест остановлен: найден forbidden после перехода на url товара: {url}"


            solver.capcha_solver()
            human_delay(2, 3)

        with allure.step("Имитируем поведение пользователя: скролл и мышь"):
            for i in range(0, random.randint(400, 1000), 150):
                page.mouse.wheel(0, i)
                human_delay(0.2, 0.5)
            page.mouse.move(random.randint(100, 600), random.randint(200, 400), steps=10)
            human_delay(0.5, 1.0)

        with allure.step("Наводим курсор на цену и считываем"):
            try:
                if page.locator(PERSONAL_PRICE).is_visible():
                    price_element = page.locator(PERSONAL_PRICE)
                else:
                    price_element = page.locator(CURRENT_PRICE)
                price_element.wait_for(timeout=10000)
                box = price_element.bounding_box()
                if not box:
                    raise Exception("No bounding box for price")
                page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=20)
                human_delay(0.5, 1.2)
                price = price_element.inner_text().strip()
            except Exception:
                price = "-"
                print(f"Цена не найдена на {url}")
            price_results.append((url, price))

        with allure.step("Сохраняем результат в CSV"):
            save_to_csv(url, price)

        with allure.step("Вывод результата"):
            print(f"✔ {url} — {price}")
            allure.attach(price, name="Цена", attachment_type=allure.attachment_type.TEXT)

        assert "₽" in price or price == "-", f"Нет корректной цены на {url}: {price}"

    # Можно добавить общую проверку по результатам
    print("Результаты парсинга:")
    for url, price in price_results:
        print(f"{url} — {price}")

def human_delay(min_sec=0.5, max_sec=1.5):
    time.sleep(random.uniform(min_sec, max_sec))

def save_to_csv(url: str, price: str):
    today = datetime.date.today().isoformat()
    file_exists = os.path.isfile(OUTPUT_FILE)
    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Дата", "URL", "Цена"])
        writer.writerow([today ,url, price])

"""Конец рабочего тест"""


"""Тест законсервирован до лучших времен куки с автоматизации не подходят"""

# import csv
# import os
# import random
# import time
# import pytest
# import allure
# from playwright.sync_api import Page
# from widgets.capcha_solver import SyncCaptchaSlider, page_contains_forbidden
#
#
# PRODUCT_URLS = [
#     "https://www.vseinstrumenti.ru/product/topor-800-g-fiberglasovoe-toporische-matrix-21647-534021/",
#     "https://www.vseinstrumenti.ru/product/drel-shurupovert-aeg-bs18g4-202c-4935478630-1760653/",
#     "https://www.vseinstrumenti.ru/product/zakrytye-ochki-soyuzspetsodezhda-rosomz-3h11-panorama-prozrachnye-2000000168654-3576162/",
#     "https://www.vseinstrumenti.ru/product/dlinnogubtsy-jonnesway-p118/"
# ]
#
# OUTPUT_FILE = "prices.csv"
# PRICE_LOCATOR = '[data-qa="price-now"]'
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
#              "AppleWebKit/537.36 (KHTML, like Gecko) " \
#              "Chrome/122.0.0.0 Safari/537.36"
#
#
# # тест работает с куками в headless
# @pytest.mark.parametrize("url", PRODUCT_URLS)
# @allure.title("Сбор цены с имитацией поведения пользователя")
# def test_get_price_human_like_2(page_fixture, url):
#     page = page_fixture()
#     solver = SyncCaptchaSlider(page)
#
#     # Паттерн антибан настроек
#     page.context.set_extra_http_headers({"User-Agent": USER_AGENT})
#     page.set_viewport_size({"width": 1366, "height": 768})
#     page.add_init_script("""
#     // Отключаем webdriver и подсовываем более "живой" fingerprint
#     Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
#     Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru', 'en-US', 'en']});
#     Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5, 6]});
#     window.chrome = { runtime: {} };
#
#     // Fingerprint: canvas spoof, audio spoof
#     const getFakeData = () => new Uint8ClampedArray([128,128,128,255,128,128,128,255]);
#     HTMLCanvasElement.prototype.toDataURL = function(){ return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Zw8AAjMBi/MaaWkAAAAASUVORK5CYII="; }
#     window.OffscreenCanvas = HTMLCanvasElement;
#
#     // UserAgent spoof внутри navigator (для некоторых js-антиботов)
#     const _orig_ua = navigator.userAgent;
#     Object.defineProperty(navigator, 'userAgent', { get: () => _orig_ua });
#
#     // Timezone spoof
#     Intl.DateTimeFormat = function() { return { resolvedOptions: () => ({ timeZone: 'Europe/Moscow' }) } }
# """)
#
#     with allure.step("Переход на главную и прогрев страницы"):
#         # Заходим на яндекс и ищем "Все инструменты"
#         page.goto("https://mail.ru/", timeout=60000)
#         human_delay(1, 2)
#         search_box = page.locator('input[name="search_source"]')
#         search_box.type("Все инструменты",200)
#         page.keyboard.press("Enter")
#         # Ждём появления результатов и ссылки на vseinstrumenti.ru, кликаем на первую (или где вхождение)
#         page.wait_for_selector('a[href*="vseinstrumenti.ru"]', timeout=60000)
#         first_link = page.locator('a[href*="vseinstrumenti.ru"]').first
#         first_link.click()
#         # Ждём загрузки целевого сайтаhref="https://www.vseinstrumenti.ru/"
#         page.wait_for_url("https://www.vseinstrumenti.ru/*", timeout=15000)
#
#         # Проверяем принудительно — вдруг редирект на /xpvnsulc (или другая капча)
#         curr_url = page.url
#         if re.search(r"/xpvnsulc|forbidden", curr_url) or page_contains_forbidden(page):
#             # Сразу решаем капчу!
#             solver.capcha_solver()
#
#     with allure.step("Проверка 'forbidden' на главной"):
#         if page_contains_forbidden(page):
#             assert False, "Тест остановлен: найден forbidden после перехода на главную"
#
#     with allure.step("Проверка наличия капчи на главной"):
#         solver.capcha_solver()
#
#     human_delay(1.2, 2.5)
#
#     # # Имитируем поведение настоящего браузера
#     # page.context.set_extra_http_headers({"User-Agent": USER_AGENT})
#     #
#     # with allure.step("Переход на главную и прогрев страницы"):
#     #     page.goto("https://www.vseinstrumenti.ru/", wait_until="domcontentloaded")
#     #     human_delay(1.2, 2.5)
#
#
#
#     # with allure.step(f"Переход на товар: {url}"):
#     #     page.goto(url, wait_until="load", timeout=60000)
#     #     human_delay(2, 3)
#
#     with allure.step(f"Переход на товар: {url}"):
#         page.goto(url, wait_until="load", timeout=60000)
#         with allure.step("Go to товар, обработка антибота"):
#             print("Ура, мы на товаре:", page.url)
#         # Проверяем принудительно — вдруг редирект на /xpvnsulc (или другая капча)
#         curr_url = page.url
#         if re.search(r"/xpvnsulc|forbidden", curr_url) or page_contains_forbidden(page):
#             # Сразу решаем капчу!
#             solver.capcha_solver()
#
#     with allure.step(f"Проверка 'forbidden' на: {url}"):
#         if page_contains_forbidden(page):
#             assert False, "Тест остановлен: найден forbidden после перехода на url товара"
#
#     with allure.step(f"Проверка капчи на: {url}"):
#         solver.capcha_solver()
#
#     human_delay(2, 3)
#
#     with allure.step("Имитируем поведение пользователя: скролл и мышь"):
#         for i in range(0, random.randint(400, 1000), 150):
#             page.mouse.wheel(0, i)
#             human_delay(0.2, 0.5)
#         page.mouse.move(random.randint(100, 600), random.randint(200, 400), steps=10)
#         human_delay(0.5, 1.0)
#
#     with allure.step("Наводим курсор на цену и считываем"):
#         try:
#             price_element = page.locator(PRICE_LOCATOR)
#             price_element.wait_for(timeout=10000)
#             box = price_element.bounding_box()
#             if not box:
#                 raise Exception("No bounding box for price")
#             page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=20)
#             human_delay(0.5, 1.2)
#             price = price_element.inner_text().strip()
#         except Exception:
#             price = "-"
#             print(f"Цена не найдена на {url}")
#
#     with allure.step("Сохраняем результат в CSV"):
#         save_to_csv(url, price)
#
#     with allure.step("Вывод результата"):
#         print(f"✔ {url} — {price}")
#         allure.attach(price, name="Цена", attachment_type=allure.attachment_type.TEXT)
#
#     assert "₽" in price or "не найдена" not in price.lower()
#
#
# # ---------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ----------
#
# def human_delay(min_sec=0.5, max_sec=1.5):
#     """Пауза как у человека"""
#     time.sleep(random.uniform(min_sec, max_sec))
#
#
# def save_to_csv(url: str, price: str):
#     file_exists = os.path.isfile(OUTPUT_FILE)
#     with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
#         writer = csv.writer(f)
#         if not file_exists:
#             writer.writerow(["URL", "Цена"])
#         writer.writerow([url, price])


# import base64
# import time
# import requests
# from io import BytesIO
# from PIL import Image
# from playwright.sync_api import Page
#
#
# def capture_captcha(page: Page, selector: str) -> Image.Image:
#     """Сохраняем изображение капчи из элемента"""
#     element = page.locator(selector)
#     box = element.bounding_box()
#     screenshot = page.screenshot()
#     full_img = Image.open(BytesIO(screenshot))
#     cropped = full_img.crop((box['x'], box['y'], box['x'] + box['width'], box['y'] + box['height']))
#     return cropped
#
#
# def solve_captcha_deepseek(image: Image.Image, deepseek_api_key: str) -> float:
#     """Решение капчи через DeepSeek (предполагаем кастомную модель/промпт)"""
#     base64_img = base64.b64encode(image_to_bytes(image)).decode('utf-8')
#     headers = {"Authorization": f"Bearer {deepseek_api_key}"}
#     data = {
#         "model": "deepseek-coder",
#         "messages": [
#             {"role": "user", "content": "What angle (in degrees) should this image be rotated to be upright?"},
#             {"role": "user", "content": {"image": base64_img}}
#         ]
#     }
#     response = requests.post("https://api.deepseek.com/v1/chat/completions", json=data, headers=headers)
#     return float(extract_angle_from_response(response.json()))
#
#
# def solve_captcha_gemini(image: Image.Image, gemini_api_key: str) -> float:
#     """Решение капчи через Gemini"""
#     base64_img = base64.b64encode(image_to_bytes(image)).decode('utf-8')
#     headers = {"Content-Type": "application/json"}
#     data = {
#         "contents": [{
#             "parts": [
#                 {"text": "Determine by how many degrees this image should be rotated clockwise to be upright."},
#                 {"inlineData": {"mimeType": "image/png", "data": base64_img}}
#             ]
#         }]
#     }
#     url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro-vision:generateContent?key={gemini_api_key}"
#     response = requests.post(url, json=data, headers=headers)
#     return float(extract_angle_from_response(response.json()))
#
#
# def image_to_bytes(image: Image.Image) -> bytes:
#     buf = BytesIO()
#     image.save(buf, format='PNG')
#     return buf.getvalue()
#
#
# def extract_angle_from_response(response_json: dict) -> float:
#     """Простая логика извлечения числа из ответа"""
#     import re
#     text = str(response_json)
#     matches = re.findall(r'\d{1,3}', text)
#     for num in matches:
#         angle = int(num)
#         if 0 <= angle <= 360:
#             return angle
#     raise ValueError("Angle not found in response")
#
#
# def drag_slider(page: Page, slider_selector: str, angle: float):
#     """Имитация перетаскивания ползунка"""
#     slider = page.locator(slider_selector)
#     box = slider.bounding_box()
#     start_x = box["x"] + box["width"] / 2
#     start_y = box["y"] + box["height"] / 2
#
#     # Предположим, 360 градусов соответствует 200px движения вправо
#     pixels_per_degree = 200 / 360
#     move_x = angle * pixels_per_degree
#
#     page.mouse.move(start_x, start_y)
#     page.mouse.down()
#     page.mouse.move(start_x + move_x, start_y, steps=15)
#     page.mouse.up()
#     time.sleep(1)  # Ждем реакции капчи
#
#
#
# def test_captcha_solver(page_fixture):
#     page = page_fixture()
#     page.goto("https://www.vseinstrumenti.ru/")  # или нужная страница с капчей
#
#     image = capture_captcha(page, selector="css=.captcha-image")  # адаптировать под селектор
#     angle = solve_captcha_gemini(image, gemini_api_key="")  # или solve_captcha_deepseek
#
#     drag_slider(page, slider_selector="div.captcha-control-button", angle=angle)
#
#     # Проверка, что капча пройдена и мы попали на нужную страницу
#     assert "some expected content" in page.content()
#
#
#
# import os
# import time
# import random
# import pytest
# import allure
# from playwright.sync_api import Page, expect, sync_playwright
# from page_objects.product_page import ProductPage
#
#
# @allure.title("Проход капчи вручную имитацией человека")
# def test_captcha_human_behavior(page_fixture):
#     page = page_fixture()
#
#     # Переход к продукту
#     page.goto("https://www.vseinstrumenti.ru/product/dlinnogubtsy-jonnesway-p118", wait_until="load")
#     time.sleep(2)  # Позволяем странице полностью прогрузиться
#
#     # Проверка, есть ли капча
#     if page.locator("div.captcha-control").is_visible(timeout=5000):
#         print("Капча найдена. Пробуем решить...")
#
#         slider = page.locator("div.captcha-slider-button")
#         container = page.locator("div.captcha-control-wrap")
#
#         box = container.bounding_box()
#         slider_box = slider.bounding_box()
#
#         if not box or not slider_box:
#             raise Exception("Не удалось определить координаты элементов капчи")
#
#         # Начальные координаты
#         start_x = slider_box["x"] + slider_box["width"] / 2
#         start_y = slider_box["y"] + slider_box["height"] / 2
#
#         # Конечная точка — почти край контейнера (с отступом)
#         end_x = box["x"] + box["width"] - 10
#
#         # Движение мышки
#         page.mouse.move(start_x, start_y)
#         page.mouse.down()
#
#         steps = 30
#         total_distance = end_x - start_x
#         step_size = total_distance / steps
#
#         for i in range(steps):
#             page.mouse.move(start_x + step_size * i, start_y, steps=1)
#             time.sleep(random.uniform(0.01, 0.03))  # Микрозадержки
#
#         page.mouse.up()
#         time.sleep(3)  # Подождать реакции капчи
#
#     # Проверим, успешно ли обошли капчу и попали на продукт
#     expect(page.locator('[data-qa="price-now"]')).to_be_visible(timeout=10000)
#     price = page.locator('[data-qa="price-now"]').inner_text()
#     print(f"Цена: {price}")
#
#
#
#
#
#
#
#
#
# import base64
# import time
# import requests
# from io import BytesIO
# from PIL import Image
# from playwright.sync_api import Page
#
#
# def capture_captcha(page: Page, selector: str) -> Image.Image:
#     """Сохраняем изображение капчи из элемента"""
#     element = page.locator(selector)
#     box = element.bounding_box()
#     screenshot = page.screenshot()
#     full_img = Image.open(BytesIO(screenshot))
#     cropped = full_img.crop((box['x'], box['y'], box['x'] + box['width'], box['y'] + box['height']))
#     return cropped
#
#
# def solve_captcha_deepseek(image: Image.Image, deepseek_api_key: str) -> float:
#     """Решение капчи через DeepSeek (предполагаем кастомную модель/промпт)"""
#     base64_img = base64.b64encode(image_to_bytes(image)).decode('utf-8')
#     headers = {"Authorization": f"Bearer {deepseek_api_key}"}
#     data = {
#         "model": "deepseek-coder",
#         "messages": [
#             {"role": "user", "content": "What angle (in degrees) should this image be rotated to be upright?"},
#             {"role": "user", "content": {"image": base64_img}}
#         ]
#     }
#     response = requests.post("https://api.deepseek.com/v1/chat/completions", json=data, headers=headers)
#     return float(extract_angle_from_response(response.json()))
#
#
# def solve_captcha_gemini(image: Image.Image, gemini_api_key: str) -> float:
#     """Решение капчи через Gemini"""
#     base64_img = base64.b64encode(image_to_bytes(image)).decode('utf-8')
#     headers = {"Content-Type": "application/json"}
#     data = {
#         "contents": [{
#             "parts": [
#                 {"text": "Determine by how many degrees this image should be rotated clockwise to be upright."},
#                 {"inlineData": {"mimeType": "image/png", "data": base64_img}}
#             ]
#         }]
#     }
#     url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro-vision:generateContent?key={gemini_api_key}"
#     response = requests.post(url, json=data, headers=headers)
#     return float(extract_angle_from_response(response.json()))
#
#
# def image_to_bytes(image: Image.Image) -> bytes:
#     buf = BytesIO()
#     image.save(buf, format='PNG')
#     return buf.getvalue()
#
#
# def extract_angle_from_response(response_json: dict) -> float:
#     """Простая логика извлечения числа из ответа"""
#     import re
#     text = str(response_json)
#     matches = re.findall(r'\d{1,3}', text)
#     for num in matches:
#         angle = int(num)
#         if 0 <= angle <= 360:
#             return angle
#     raise ValueError("Angle not found in response")
#
#
# def drag_slider(page: Page, slider_selector: str, angle: float):
#     """Имитация перетаскивания ползунка"""
#     slider = page.locator(slider_selector)
#     box = slider.bounding_box()
#     start_x = box["x"] + box["width"] / 2
#     start_y = box["y"] + box["height"] / 2
#
#     # Предположим, 360 градусов = 200 пикселей вправо
#     pixels_per_degree = 200 / 360
#     move_x = angle * pixels_per_degree
#
#     page.mouse.move(start_x, start_y)
#     page.mouse.down()
#     page.mouse.move(start_x + move_x, start_y, steps=15)
#     page.mouse.up()
#     time.sleep(1)  # Ждем реакции капчи
#
#
# def solve_slider_captcha(page: Page, deepseek_api_key: str = None, gemini_api_key: str = None):
#     """Основная логика: найти капчу, распознать угол и сдвинуть ползунок"""
#     captcha_selector = 'div.captcha-control'
#     slider_selector = 'div.captcha-control-wrap'
#
#     if not page.locator(captcha_selector).is_visible():
#         print("Капча не обнаружена.")
#         return
#
#     image = capture_captcha(page, captcha_selector)
#
#     if deepseek_api_key:
#         angle = solve_captcha_deepseek(image, deepseek_api_key)
#     elif gemini_api_key:
#         angle = solve_captcha_gemini(image, gemini_api_key)
#     else:
#         raise ValueError("Нужен ключ API DeepSeek или Gemini.")
#
#     print(f"Распознан угол: {angle}")
#     drag_slider(page, slider_selector, angle)
#
#
# import asyncio
# import random
# import time
# from playwright.async_api import Page, Locator
# import json
# from typing import Optional, Tuple, List
#
#
# class AdvancedCaptchaSolver:
#     def __init__(self, page: Page):
#         self.page = page
#
#     async def wait_for_captcha_load(self, timeout: int = 10000) -> bool:
#         """Ожидание загрузки капчи"""
#         try:
#             # Ждем появления основных элементов капчи
#             await self.page.wait_for_selector('.captcha-container, .slide-verify, .geetest-wrap', timeout=timeout)
#             await asyncio.sleep(1)  # Дополнительное время для полной загрузки
#             return True
#         except:
#             return False
#
#     async def find_captcha_elements(self) -> Optional[Tuple[Locator, Locator, Locator]]:
#         """Поиск элементов капчи с различными селекторами"""
#         selectors_map = [
#             {
#                 'container': '.geetest-wrap',
#                 'slider': '.geetest_slider_button',
#                 'track': '.geetest_slider'
#             },
#             {
#                 'container': '.slide-verify',
#                 'slider': '.slide-verify-slider-mask-item',
#                 'track': '.slide-verify-slider'
#             },
#             {
#                 'container': '.captcha-container',
#                 'slider': '.captcha-control-button',
#                 'track': '.captcha-track'
#             }
#         ]
#
#         for selectors in selectors_map:
#             try:
#                 container = self.page.locator(selectors['container'])
#                 slider = self.page.locator(selectors['slider'])
#                 track = self.page.locator(selectors['track'])
#
#                 if await container.count() > 0 and await slider.count() > 0:
#                     return container, slider, track
#             except:
#                 continue
#
#         return None
#
#     async def human_like_drag(self, slider: Locator, target_distance: int) -> bool:
#         """Человекоподобное перетаскивание ползунка"""
#         try:
#             # Получаем координаты ползунка
#             box = await slider.bounding_box()
#             if not box:
#                 return False
#
#             start_x = box['x'] + box['width'] / 2
#             start_y = box['y'] + box['height'] / 2
#
#             # Добавляем случайные вариации для имитации человеческого поведения
#             start_x += random.randint(-2, 2)
#             start_y += random.randint(-2, 2)
#
#             # Наводимся на ползунок
#             await self.page.mouse.move(start_x - 10, start_y)
#             await asyncio.sleep(random.uniform(0.1, 0.3))
#
#             # Перемещаемся точно на ползунок
#             await self.page.mouse.move(start_x, start_y)
#             await asyncio.sleep(random.uniform(0.1, 0.2))
#
#             # Начинаем перетаскивание
#             await self.page.mouse.down()
#             await asyncio.sleep(random.uniform(0.05, 0.1))
#
#             # Создаем реалистичный путь движения
#             steps = random.randint(15, 25)
#             for i in range(steps):
#                 progress = (i + 1) / steps
#
#                 # Используем кубическую функцию для более естественного движения
#                 eased_progress = self._ease_out_cubic(progress)
#                 current_distance = target_distance * eased_progress
#
#                 # Добавляем небольшие случайные отклонения
#                 jitter_x = random.uniform(-1, 1)
#                 jitter_y = random.uniform(-0.5, 0.5)
#
#                 new_x = start_x + current_distance + jitter_x
#                 new_y = start_y + jitter_y
#
#                 await self.page.mouse.move(new_x, new_y)
#                 await asyncio.sleep(random.uniform(0.01, 0.03))
#
#             # Финальная позиция
#             await self.page.mouse.move(start_x + target_distance, start_y)
#             await asyncio.sleep(random.uniform(0.1, 0.2))
#
#             # Отпускаем кнопку мыши
#             await self.page.mouse.up()
#
#             return True
#
#         except Exception as e:
#             print(f"Ошибка при перетаскивании: {e}")
#             return False
#
#     def _ease_out_cubic(self, t: float) -> float:
#         """Функция плавности для естественного движения"""
#         return 1 - (1 - t) ** 3
#
#     async def solve_puzzle_captcha(self, container: Locator, slider: Locator) -> bool:
#         """Решение пазл-капчи методом постепенного приближения"""
#         max_attempts = 10
#
#         for attempt in range(max_attempts):
#             # Начинаем с небольшого движения и увеличиваем
#             base_distance = 50 + (attempt * 20)  # От 50 до 230 пикселей
#             distance = base_distance + random.randint(-10, 10)
#
#             success = await self.human_like_drag(slider, distance)
#             if not success:
#                 continue
#
#             # Ждем реакции системы
#             await asyncio.sleep(random.uniform(1, 2))
#
#             # Проверяем результат
#             if await self._check_success(container):
#                 return True
#
#             # Если не удалось, ждем немного перед следующей попыткой
#             await asyncio.sleep(random.uniform(0.5, 1))
#
#         return False
#
#     async def _check_success(self, container: Locator) -> bool:
#         """Проверка успешного прохождения капчи"""
#         success_indicators = [
#             '.geetest_success',
#             '.slide-verify-success',
#             '.captcha-success',
#             '[class*="success"]',
#             '[class*="complete"]'
#         ]
#
#         for indicator in success_indicators:
#             try:
#                 element = container.locator(indicator)
#                 if await element.count() > 0:
#                     return True
#             except:
#                 continue
#
#         return False






















# import random
# import time
# from playwright.sync_api import Page, Locator, sync_playwright
# from typing import Optional, Tuple
#
#
# class SyncCaptchaSolver:
#     def __init__(self, page: Page):
#         self.page = page
#
#     def wait_for_captcha_load(self, timeout: int = 10000) -> bool:
#         """Ожидание загрузки капчи"""
#         try:
#             # Ждем появления контейнера капчи
#             self.page.wait_for_selector('div.captcha-control', timeout=timeout)
#             time.sleep(1)  # Дополнительное время для полной загрузки
#             return True
#         except Exception as e:
#             print(f"Капча не загрузилась: {e}")
#             return False
#
#     def find_captcha_elements(self) -> Optional[Tuple[Locator, Locator, Locator]]:
#         """Поиск элементов капчи с точными селекторами"""
#         try:
#             container = self.page.locator('div.captcha-control')
#             slider_wrap = self.page.locator('div.captcha-control-wrap')
#             slider_button = self.page.locator('div.captcha-control-button')
#
#
#             if (container.count() > 0 and
#                     slider_wrap.count() > 0 and
#                     slider_button.count() > 0):
#                 return container, slider_wrap, slider_button
#         except Exception as e:
#             print(f"Ошибка при поиске элементов: {e}")
#
#         return None
#
#     def human_like_drag(self, slider: Locator, target_distance: int) -> bool:
#         """Человекоподобное перетаскивание ползунка"""
#         try:
#             # Получаем координаты ползунка
#             box = slider.bounding_box()
#             if not box:
#                 print("Не удалось получить координаты ползунка")
#                 return False
#
#             start_x = box['x'] + box['width'] / 2
#             start_y = box['y'] + box['height'] / 2
#
#             # Добавляем случайные вариации для имитации человеческого поведения
#             start_x += random.randint(-2, 2)
#             start_y += random.randint(-2, 2)
#
#             print(f"Начальная позиция: ({start_x}, {start_y})")
#             print(f"Цель: переместить на {target_distance} пикселей")
#
#             # Наводимся на ползунок
#             self.page.mouse.move(start_x - 10, start_y)
#             time.sleep(random.uniform(0.1, 0.3))
#
#             # Перемещаемся точно на ползунок
#             self.page.mouse.move(start_x, start_y)
#             time.sleep(random.uniform(0.1, 0.2))
#
#             # Начинаем перетаскивание
#             self.page.mouse.down()
#             time.sleep(random.uniform(0.05, 0.1))
#
#             # Создаем реалистичный путь движения
#             steps = random.randint(15, 25)
#             for i in range(steps):
#                 progress = (i + 1) / steps
#
#                 # Используем кубическую функцию для более естественного движения
#                 eased_progress = self._ease_out_cubic(progress)
#                 current_distance = target_distance * eased_progress
#
#                 # Добавляем небольшие случайные отклонения
#                 jitter_x = random.uniform(-1, 1)
#                 jitter_y = random.uniform(-0.5, 0.5)
#
#                 new_x = start_x + current_distance + jitter_x
#                 new_y = start_y + jitter_y
#
#                 self.page.mouse.move(new_x, new_y)
#                 time.sleep(random.uniform(0.01, 0.03))
#
#             # Финальная позиция
#             final_x = start_x + target_distance
#             self.page.mouse.move(final_x, start_y)
#             time.sleep(random.uniform(0.1, 0.2))
#
#             print(f"Финальная позиция: ({final_x}, {start_y})")
#
#             # Отпускаем кнопку мыши
#             self.page.mouse.up()
#
#             return True
#
#         except Exception as e:
#             print(f"Ошибка при перетаскивании: {e}")
#             return False
#
#     def _ease_out_cubic(self, t: float) -> float:
#         """Функция плавности для естественного движения"""
#         return 1 - (1 - t) ** 3
#
#     def solve_slider_captcha(self, container: Locator, slider_button: Locator) -> bool:
#         """Решение слайдер-капчи методом постепенного приближения"""
#         max_attempts = 8
#
#         # Получаем ширину контейнера для расчета расстояния
#         container_box = container.bounding_box()
#         if not container_box:
#             print("Не удалось получить размеры контейнера")
#             return False
#
#         max_distance = int(container_box['width'] * 0.8)  # Максимум 80% от ширины
#         print(f"Максимальное расстояние для движения: {max_distance}px")
#
#         for attempt in range(max_attempts):
#             # Варьируем расстояние от 30% до 90% от максимума
#             min_distance = int(max_distance * 0.3)
#             distance_range = max_distance - min_distance
#             distance = min_distance + int((distance_range / max_attempts) * (attempt + 1))
#             distance += random.randint(-15, 15)  # Случайная вариация
#
#             print(f"\n--- Попытка {attempt + 1}/{max_attempts} ---")
#             print(f"Расстояние: {distance}px")
#
#             success = self.human_like_drag(slider_button, distance)
#             if not success:
#                 continue
#
#             # Ждем реакции системы
#             time.sleep(random.uniform(1.5, 2.5))
#
#             # Проверяем результат
#             if self._check_success(container):
#                 print("✅ Капча решена успешно!")
#                 return True
#
#             print(f"❌ Попытка {attempt + 1} неуспешна")
#
#             # Ждем перед следующей попыткой
#             if attempt < max_attempts - 1:
#                 time.sleep(random.uniform(1, 2))
#
#         print("❌ Все попытки исчерпаны")
#         return False
#
#     def _check_success(self, container: Locator) -> bool:
#         """Проверка успешного прохождения капчи"""
#         success_indicators = [
#             'div.captcha-success',
#             'div.captcha-complete',
#             '.success',
#             '.complete',
#             '[class*="success"]',
#             '[class*="complete"]',
#             '[class*="solved"]'
#         ]
#
#         try:
#             # Проверяем изменение классов контейнера
#             container_classes = container.get_attribute('class')
#             if container_classes and (
#                     'success' in container_classes.lower() or 'complete' in container_classes.lower()):
#                 return True
#
#             # Проверяем появление индикаторов успеха
#             for indicator in success_indicators:
#                 element = container.locator(indicator)
#                 if element.count() > 0:
#                     return True
#
#             # Проверяем, исчез ли ползунок (иногда признак успеха)
#             slider_button = container.locator('div.captcha-slider-button')
#             if slider_button.count() == 0:
#                 return True
#
#         except Exception as e:
#             print(f"Ошибка при проверке успеха: {e}")
#
#         return False
#
#
# def test_advanced_captcha_solver():
#     """Синхронный тест для решения капчи"""
#     with sync_playwright() as p:
#         # Запускаем браузер с настройками для обхода детекции
#         browser = p.chromium.launch(
#             headless=False,  # Визуальный режим для отладки
#             args=[
#                 '--no-blink-features=AutomationControlled',
#                 '--disable-blink-features=AutomationControlled',
#                 '--disable-dev-shm-usage',
#                 '--no-first-run',
#                 '--disable-default-apps',
#                 '--disable-features=TranslateUI',
#                 '--disable-web-security'
#             ]
#         )
#
#         context = browser.new_context(
#             user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#             viewport={'width': 1366, 'height': 768},
#             extra_http_headers={
#                 'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8'
#             }
#         )
#
#         page = context.new_page()
#
#         # Убираем признаки автоматизации
#         page.add_init_script("""
#             Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
#             window.chrome = {runtime: {}};
#             Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
#         """)
#
#         try:
#             print("🚀 Переходим на страницу...")
#             page.goto("https://www.vseinstrumenti.ru/", wait_until='networkidle')
#
#             solver = SyncCaptchaSolver(page)
#
#             # Ждем появления капчи (может потребоваться действие пользователя)
#             print("⏳ Ожидание появления капчи...")
#             print("   (Возможно, потребуется ручное действие для активации капчи)")
#
#             # Увеличиваем время ожидания
#             if not solver.wait_for_captcha_load(60000):  # 60 секунд
#                 print("❌ Капча не найдена в течение 60 секунд")
#                 input("Нажмите Enter, если капча появилась...")
#
#                 # Повторная проверка
#                 if not solver.wait_for_captcha_load(5000):
#                     print("❌ Капча все еще не найдена")
#                     return False
#
#             # Находим элементы капчи
#             print("🔍 Поиск элементов капчи...")
#             captcha_elements = solver.find_captcha_elements()
#             if not captcha_elements:
#                 print("❌ Элементы капчи не найдены")
#
#                 # Показываем доступные элементы для отладки
#                 print("\n🔧 Доступные элементы на странице:")
#                 all_divs = page.locator('div').all()
#                 for i, div in enumerate(all_divs[:20]):  # Первые 20 div'ов
#                     try:
#                         class_attr = div.get_attribute('class')
#                         if class_attr and 'captcha' in class_attr.lower():
#                             print(f"  - div с классом: {class_attr}")
#                     except:
#                         continue
#
#                 return False
#
#             container, slider_wrap, slider_button = captcha_elements
#             print("✅ Элементы капчи найдены!")
#             print(f"   - Контейнер: {container.count()} элемент(ов)")
#             print(f"   - Обертка: {slider_wrap.count()} элемент(ов)")
#             print(f"   - Кнопка: {slider_button.count()} элемент(ов)")
#
#             # Решаем капчу
#             print("\n🎯 Начинаем решение капчи...")
#             success = solver.solve_slider_captcha(container, slider_button)
#
#             if success:
#                 print("\n🎉 Капча успешно решена!")
#                 time.sleep(3)  # Ждем возможного перенаправления
#                 return True
#             else:
#                 print("\n😞 Не удалось решить капчу автоматически")
#                 return False
#
#         except Exception as e:
#             print(f"💥 Критическая ошибка: {e}")
#             import traceback
#             traceback.print_exc()
#             return False
#         finally:
#             print("\n🔚 Закрытие браузера...")
#             time.sleep(2)  # Время на просмотр результата
#             browser.close()
#
#
# # Упрощенная версия для быстрого тестирования
# def test_simple_captcha_solver():
#     """Упрощенный тест с базовой логикой"""
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#
#         try:
#             page.goto("https://www.vseinstrumenti.ru/")
#
#             # Ждем появления капчи
#             print("Ожидание капчи...")
#             page.wait_for_selector('div.captcha-control', timeout=30000)
#
#             # Находим кнопку слайдера
#             slider = page.locator('div.captcha-control-button')
#
#             if slider.count() > 0:
#                 print("Кнопка слайдера найдена, начинаем движение...")
#
#                 # Получаем координаты
#                 box = slider.bounding_box()
#                 start_x = box['x'] + box['width'] / 2
#                 start_y = box['y'] + box['height'] / 2
#
#                 # Простое перетаскивание на разные расстояния
#                 distances = [60, 120, 180, 240]
#
#                 for distance in distances:
#                     print(f"Пробуем расстояние: {distance}px")
#
#                     page.mouse.move(start_x, start_y)
#                     page.mouse.down()
#                     page.mouse.move(start_x + distance, start_y, steps=20)
#                     page.mouse.up()
#
#                     time.sleep(2)
#
#                     # Простая проверка - исчезла ли кнопка
#                     if page.locator('div.captcha-slider-button').count() == 0:
#                         print("✅ Кнопка исчезла - возможно, капча решена!")
#                         return True
#
#                 print("❌ Капча не решена")
#                 return False
#             else:
#                 print("❌ Кнопка слайдера не найдена")
#                 return False
#
#         except Exception as e:
#             print(f"Ошибка: {e}")
#             return False
#         finally:
#             time.sleep(5)
#             browser.close()
#
#
# if __name__ == "__main__":
#     # Можете выбрать любой из тестов
#     test_advanced_captcha_solver()
#     # test_simple_captcha_solver()
















# import base64
# import json
# import random
# import time
# import requests
# from io import BytesIO
# from playwright.sync_api import Page, sync_playwright, Locator
# from typing import Optional, Tuple
# from PIL import Image
# import re
#
#
# class SyncCaptchaSolverGemini:
#     def __init__(self, page: Page, gemini_api_key: str):
#         self.page = page
#         self.gemini_api_key = gemini_api_key
#
#     def wait_for_captcha_load(self, timeout: int = 10000) -> bool:
#         """Ожидание загрузки капчи"""
#         try:
#             self.page.wait_for_selector('div.captcha-control', timeout=timeout)
#             time.sleep(1)  # Дополнительное время для полной загрузки
#             return True
#         except Exception as e:
#             print(f"Капча не загрузилась: {e}")
#             return False
#
#     def find_captcha_elements(self) -> Optional[Tuple[Locator, Locator, Locator]]:
#         """Поиск элементов капчи с точными селекторами"""
#         try:
#             container = self.page.locator('div.captcha-control')
#             slider_wrap = self.page.locator('div.captcha-control-wrap')
#             slider_button = self.page.locator('div.captcha-control-button')
#
#             if (container.count() > 0 and
#                     slider_wrap.count() > 0 and
#                     slider_button.count() > 0):
#                 return container, slider_wrap, slider_button
#         except Exception as e:
#             print(f"Ошибка при поиске элементов: {e}")
#
#         return None
#
#     def capture_captcha_image(self, container: Locator) -> Optional[Image.Image]:
#         """Захват изображения капчи для анализа"""
#         try:
#             # Получаем координаты контейнера капчи
#             box = container.bounding_box()
#             if not box:
#                 print("Не удалось получить координаты контейнера")
#                 return None
#
#             # Делаем скриншот всей страницы
#             screenshot = self.page.screenshot()
#             full_img = Image.open(BytesIO(screenshot))
#
#             # Обрезаем изображение до области капчи
#             cropped = full_img.crop((
#                 box['x'],
#                 box['y'],
#                 box['x'] + box['width'],
#                 box['y'] + box['height']
#             ))
#
#             print(f"📷 Захвачено изображение капчи размером: {cropped.size}")
#             return cropped
#
#         except Exception as e:
#             print(f"Ошибка при захвате изображения: {e}")
#             return None
#
#     def solve_captcha_gemini(self, image: Image.Image) -> Optional[float]:
#         """Решение капчи через Gemini API"""
#         try:
#             # Конвертируем изображение в base64
#             buf = BytesIO()
#             image.save(buf, format='PNG')
#             base64_img = base64.b64encode(buf.getvalue()).decode('utf-8')
#
#             # Подготавливаем запрос к Gemini API
#             headers = {"Content-Type": "application/json"}
#             data = {
#                 "contents": [{
#                     "parts": [
#                         {
#                             "text": """Analyze this slider captcha image. I need to determine how many pixels to move the slider to complete the puzzle.
#                             Look for the missing piece or gap in the puzzle and estimate the horizontal distance in pixels from the slider's current position to where it should be placed.
#                             Return only a number representing pixels (for example: 120, 200, 85). If you can't determine the exact position, estimate based on the typical captcha layout."""
#                         },
#                         {
#                             "inlineData": {
#                                 "mimeType": "image/png",
#                                 "data": base64_img
#                             }
#                         }
#                     ]
#                 }]
#             }
#
#             # Отправляем запрос к Gemini API
#             url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
#
#             print("🔍 Отправляем запрос к Gemini API...")
#             response = requests.post(url, json=data, headers=headers, timeout=30)
#
#             if response.status_code != 200:
#                 print(f"❌ Ошибка API: {response.status_code} - {response.text}")
#                 return None
#
#             response_json = response.json()
#             print(f"📄 Ответ Gemini API: {response_json}")
#
#             # Извлекаем расстояние из ответа
#             return self.extract_distance_from_response(response_json)
#
#         except Exception as e:
#             print(f"❌ Ошибка при обращении к Gemini API: {e}")
#             return None
#
#     def extract_distance_from_response(self, response_json: dict) -> Optional[float]:
#         """Извлечение числа пикселей из ответа Gemini"""
#         try:
#             # Получаем текст ответа
#             if 'candidates' in response_json and response_json['candidates']:
#                 content = response_json['candidates'][0].get('content', {})
#                 parts = content.get('parts', [])
#                 if parts:
#                     text = parts[0].get('text', '')
#                     print(f"📝 Текст ответа: {text}")
#
#                     # Ищем числа в тексте
#                     numbers = re.findall(r'\b\d{2,4}\b', text)  # Числа от 10 до 9999
#
#                     if numbers:
#                         distance = int(numbers[0])
#                         # Проверяем разумность значения (10-500 пикселей)
#                         if 10 <= distance <= 500:
#                             print(f"✅ Извлечено расстояние: {distance} пикселей")
#                             return float(distance)
#                         else:
#                             print(f"⚠️ Расстояние {distance} выходит за разумные пределы")
#
#             print("❌ Не удалось извлечь расстояние из ответа")
#             return None
#
#         except Exception as e:
#             print(f"❌ Ошибка при извлечении расстояния: {e}")
#             return None
#
#     def human_like_drag(self, slider: Locator, target_distance: float) -> bool:
#         """Человекоподобное перетаскивание ползунка"""
#         try:
#             box = slider.bounding_box()
#             if not box:
#                 print("❌ Не удалось получить координаты ползунка")
#                 return False
#
#             start_x = box['x'] + box['width'] / 2
#             start_y = box['y'] + box['height'] / 2
#
#             # Добавляем случайные вариации
#             start_x += random.randint(-2, 2)
#             start_y += random.randint(-2, 2)
#
#             print(f"🎯 Начальная позиция: ({start_x:.1f}, {start_y:.1f})")
#             print(f"🎯 Перемещение на: {target_distance} пикселей")
#
#             # Наводимся на ползунок
#             self.page.mouse.move(start_x - 10, start_y)
#             time.sleep(random.uniform(0.1, 0.3))
#
#             # Перемещаемся на ползунок
#             self.page.mouse.move(start_x, start_y)
#             time.sleep(random.uniform(0.1, 0.2))
#
#             # Нажимаем и удерживаем
#             self.page.mouse.down()
#             time.sleep(random.uniform(0.05, 0.1))
#
#             # Плавное перемещение
#             steps = random.randint(15, 25)
#             for i in range(steps):
#                 progress = (i + 1) / steps
#                 eased_progress = 1 - (1 - progress) ** 3  # Cubic ease-out
#                 current_distance = target_distance * eased_progress
#
#                 # Добавляем микро-дрожание
#                 jitter_x = random.uniform(-0.8, 0.8)
#                 jitter_y = random.uniform(-0.4, 0.4)
#
#                 new_x = start_x + current_distance + jitter_x
#                 new_y = start_y + jitter_y
#
#                 self.page.mouse.move(new_x, new_y)
#                 time.sleep(random.uniform(0.01, 0.03))
#
#             # Финальная позиция
#             final_x = start_x + target_distance
#             self.page.mouse.move(final_x, start_y)
#             time.sleep(random.uniform(0.1, 0.2))
#
#             # Отпускаем
#             self.page.mouse.up()
#
#             print(f"✅ Перемещение завершено в позицию: ({final_x:.1f}, {start_y:.1f})")
#             return True
#
#         except Exception as e:
#             print(f"❌ Ошибка при перетаскивании: {e}")
#             return False
#
#     def _check_success(self, container: Locator) -> bool:
#         """Проверка успешного прохождения капчи"""
#         try:
#             # Проверяем классы контейнера
#             container_classes = container.get_attribute('class')
#             if container_classes:
#                 success_keywords = ['success', 'complete', 'solved', 'valid', 'passed']
#                 for keyword in success_keywords:
#                     if keyword in container_classes.lower():
#                         print(f"✅ Найден класс успеха: {keyword}")
#                         return True
#
#             # Проверяем исчезновение кнопки слайдера
#             slider_button = container.locator('div.captcha-control-button')
#             if slider_button.count() == 0:
#                 print("✅ Кнопка слайдера исчезла - капча решена")
#                 return True
#
#             # Проверяем сообщения об успехе
#             success_texts = ['успешно', 'success', 'complete', 'solved']
#             for text in success_texts:
#                 if container.locator(f'text=/{text}/i').count() > 0:
#                     print(f"✅ Найден текст успеха: {text}")
#                     return True
#
#             return False
#
#         except Exception as e:
#             print(f"❌ Ошибка при проверке успеха: {e}")
#             return False
#
#     def solve_slider_captcha(self) -> bool:
#         """Главная функция решения капчи"""
#         print("🚀 Начинаем решение капчи...")
#
#         # Ждем загрузки капчи
#         if not self.wait_for_captcha_load(60000):
#             print("❌ Капча не найдена в течение 60 секунд")
#             return False
#
#         # Находим элементы
#         captcha_elements = self.find_captcha_elements()
#         if not captcha_elements:
#             print("❌ Элементы капчи не найдены")
#             return False
#
#         container, slider_wrap, slider_button = captcha_elements
#         print("✅ Элементы капчи найдены")
#
#         # Захватываем изображение
#         image = self.capture_captcha_image(container)
#         if image is None:
#             print("⚠️ Не удалось захватить изображение, используем расстояние по умолчанию")
#             distance = 150.0  # Значение по умолчанию
#         else:
#             # Анализируем через Gemini
#             distance = self.solve_captcha_gemini(image)
#             if distance is None or distance < 10:
#                 print("⚠️ Gemini не определил расстояние, используем значение по умолчанию")
#                 distance = 150.0
#
#         print(f"🎯 Итоговое расстояние для перемещения: {distance} пикселей")
#
#         # Выполняем перемещение
#         success = self.human_like_drag(slider_button, distance)
#         if not success:
#             return False
#
#         # Ждем реакции системы
#         print("⏳ Ожидание реакции системы...")
#         time.sleep(random.uniform(3.0, 4.0))
#
#         # Проверяем результат
#         if self._check_success(container):
#             print("🎉 Капча успешно решена!")
#             return True
#         else:
#             print("😞 Капча не решена")
#             return False
#
#
# def test_final_captcha_solver():
#     """Финальный тест решения капчи с Gemini API"""
#
#     # ============================================================
#     # ВАЖНО: Введите ваш Gemini API ключ здесь!
#     # ============================================================
#     GEMINI_API_KEY = ""  # <-- ЗАМЕНИТЕ НА ВАШ КЛЮЧ
#
#     if GEMINI_API_KEY == "ВАШ_GEMINI_API_КЛЮЧ_ЗДЕСЬ":
#         print("❌ ОШИБКА: Не указан API ключ Gemini!")
#         print("   Замените 'ВАШ_GEMINI_API_КЛЮЧ_ЗДЕСЬ' на ваш реальный ключ")
#         return False
#
#     with sync_playwright() as p:
#         # Настройки браузера для обхода детекции
#         browser = p.chromium.launch(
#             headless=False,
#             args=[
#                 '--no-blink-features=AutomationControlled',
#                 '--disable-blink-features=AutomationControlled',
#                 '--disable-dev-shm-usage'
#             ]
#         )
#
#         context = browser.new_context(
#             user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#             viewport={'width': 1366, 'height': 768}
#         )
#
#         page = context.new_page()
#
#         # Убираем признаки автоматизации
#         page.add_init_script("""
#             Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
#             window.chrome = {runtime: {}};
#         """)
#
#         try:
#             print("🌐 Переходим на сайт...")
#             page.goto("https://www.vseinstrumenti.ru/", wait_until='networkidle')
#
#             # Создаем решатель капчи
#             solver = SyncCaptchaSolverGemini(page, GEMINI_API_KEY)
#
#             # Решаем капчу
#             success = solver.solve_slider_captcha()
#
#             if success:
#                 print("\n🎊 УСПЕХ! Капча решена!")
#                 time.sleep(5)  # Время на просмотр результата
#             else:
#                 print("\n😔 Не удалось решить капчу")
#
#             return success
#
#         except Exception as e:
#             print(f"💥 Критическая ошибка: {e}")
#             import traceback
#             traceback.print_exc()
#             return False
#         finally:
#             print("\n🔚 Закрытие браузера...")
#             time.sleep(2)
#             browser.close()
#
#
# if __name__ == "__main__":
#     test_final_captcha_solver()





















# # Нормальный рабочий вариант, gemini угадывает каждый 5 раз, нет повторных попыток
# import base64
# import json
# import random
# import re
# import time
# import requests
# from io import BytesIO
# from typing import Optional, Tuple, List
# from PIL import Image
# from playwright.sync_api import Page, sync_playwright, Locator
# # import torch
# # from transformers import AutoModelForCausalLM
# # from deepseek_vl.models import VLChatProcessor, MultiModalityCausalLM
# # from deepseek_vl.utils.io import load_pil_images
#
#
# class SyncCaptchaSolverAdvanced:
#     def __init__(self, page: Page, gemini_api_key: Optional[str]=None, deepseek_api_key: Optional[str]=None, twocaptcha_key: Optional[str]=None):
#         self.page = page
#         self.gemini_api_key = gemini_api_key
#         self.deepseek_api_key = deepseek_api_key
#         self.twocaptcha_key = twocaptcha_key
#
#     def wait_for_captcha_load(self, timeout: int = 10000) -> bool:
#         try:
#             self.page.wait_for_selector('div.captcha-control', timeout=timeout)
#             time.sleep(1)
#             return True
#         except Exception as e:
#             print(f"Капча не загрузилась: {e}")
#             return False
#
#     def find_captcha_elements(self) -> Optional[Tuple[Locator, Locator, Locator]]:
#         try:
#             container = self.page.locator('div.captcha-control')
#             slider_wrap = self.page.locator('div.captcha-control-wrap')
#             slider_button = self.page.locator('div.captcha-control-button')
#             if container.count() > 0 and slider_wrap.count() > 0 and slider_button.count() > 0:
#                 return container, slider_wrap, slider_button
#         except Exception as e:
#             print(f"Ошибка при поиске элементов: {e}")
#         return None
#
#     def capture_captcha_image(self, container: Locator) -> Optional[Image.Image]:
#         try:
#             box = container.bounding_box()
#             screenshot = self.page.screenshot()
#             full_img = Image.open(BytesIO(screenshot))
#             cropped = full_img.crop((box['x'], box['y'], box['x'] + box['width'], box['y'] + box['height']))
#             return cropped
#         except Exception as e:
#             print(f"Ошибка при захвате изображения: {e}")
#             return None
#
#     # ---------- GEMINI, с улучшениями -----------
#     def solve_captcha_gemini(self, image: Image.Image) -> Optional[float]:
#         prompts = [
#             "How many pixels should I move this slider to solve the puzzle? Give a number only.",
#             # "Measure the distance from the slider to the missing piece, in pixels. Reply only with an integer.",
#             "What is the pixel offset required to solve this slider captcha?",
#             # "Анализируй приложенное изображение с капчей-слайдером. Определи точное количество пикселей по горизонтали, которое нужно переместить слайдер вправо, чтобы картинка была выравнена по горизонтали, не находилось вверх-ногами и не была завалена по горизонтали. Верни только число в формате целого числа, например: 82.",
#             # "Give only the amount (in pixels) to move the slider to complete the captcha.",
#         ]
#
#         def extract_num_from_response(response_json: dict) -> Optional[float]:
#             try:
#                 content = None
#                 if 'candidates' in response_json and response_json['candidates']:
#                     parts = response_json['candidates'][0].get('content', {}).get('parts', [])
#                     if parts:
#                         content = parts[0].get('text', '')
#                 if not content:
#                     return None
#                 numbers = re.findall(r'\d{2,4}', content)
#                 if numbers:
#                     val = int(numbers[0])
#                     if 10 <= val <= 400:
#                         return float(val)
#             except Exception as e:
#                 print(f"Ошибка извлечения числа: {e}")
#             return None
#
#         buf = BytesIO()
#         image.save(buf, format='PNG')
#         base64_img = base64.b64encode(buf.getvalue()).decode('utf-8')
#
#         best_guess = None
#         numbers = []
#         for prompt in prompts:
#             data = {
#                 "contents": [{
#                     "parts": [
#                         {"text": prompt},
#                         {"inlineData": {"mimeType": "image/png", "data": base64_img}}
#                     ]
#                 }]
#             }
#             url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
#             headers = {"Content-Type": "application/json"}
#             try:
#                 resp = requests.post(url, json=data, headers=headers, timeout=30)
#                 resp_json = resp.json()
#                 print(f"GEMINI: {resp_json}")
#                 n = extract_num_from_response(resp_json)
#                 if n and 10 <= n <= 400:
#                     numbers.append(n)
#             except Exception as e:
#                 print(f"GEMINI error: {e}")
#
#         if numbers:
#             best_guess = sum(numbers) / len(numbers)
#         if not best_guess:
#             print("Gemini дал шаблонный или пустой ответ, fallback.")
#             best_guess = 90.0
#         print(f"Gemini итоговое значение: {best_guess}")
#         return best_guess
#
#     # ---------- DEEPSEEK -----------
#     def solve_captcha_deepseek(self, image: Image.Image) -> Optional[float]:
#         import requests, base64, re
#         buf = BytesIO()
#         image.save(buf, format='PNG')
#         base64_img = base64.b64encode(buf.getvalue()).decode('utf-8')
#
#         headers = {
#             "Authorization": f"Bearer {self.deepseek_api_key}",
#             "Content-Type": "application/json",
#             "Accept": "application/json",
#         }
#
#         data = {
#             "model": "deepseek-vl-chat",  # Используем именно визуальную модель
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": [
#                         {
#                             "type": "text",
#                             "text": "How many pixels should the slider move to perfectly solve the CAPTCHA in the image? Respond only with an integer."
#                         },
#                         {
#                             "type": "image_url",
#                             "image_url": {
#                                 "url": f"data:image/png;base64,{base64_img}"
#                             }
#                         }
#                     ]
#                 }
#             ],
#             "max_tokens": 8,
#             "temperature": 0
#         }
#
#         try:
#             response = requests.post(
#                 "https://api.deepseek.com/v1/vl/chat/completions",
#                 json=data,
#                 headers=headers,
#                 timeout=60
#             )
#             response.raise_for_status()
#             j = response.json()
#             print(f"DeepSeek-VL ответ: {j}")
#
#             # Разбор ответа
#             if 'choices' in j and len(j['choices']) > 0:
#                 content = j['choices'][0]['message']['content']
#                 # Оставляем только первое число 10-400
#                 numbers = re.findall(r'\d{2,4}', content)
#                 if numbers:
#                     val = int(numbers[0])
#                     if 10 <= val <= 400:
#                         return float(val)
#             return 90.0
#
#         except requests.exceptions.HTTPError as http_err:
#             print(f"HTTP error: {http_err}\nResponse: {getattr(http_err.response, 'text', '')}")
#         except Exception as e:
#             print(f"DeepSeek-VL error: {e}")
#         return 90.0
#
#     # ---------- 2CAPTCHA -----------
#     def solve_captcha_2captcha(self, page_url: str, site_key: str) -> Optional[str]:
#         # Для классического рекаптча/keycaptcha/geetest укажите нужный метод!
#         # На слайдер-капчы часто используют custom метод или клон GeeTest:
#         try:
#             capt_id = requests.post(
#                 "http://2captcha.com/in.php",
#                 data={
#                     "key": self.twocaptcha_key,
#                     "method": "userrecaptcha",  # или geetest, если нужный тип
#                     "googlekey": site_key,
#                     "pageurl": page_url,
#                     "json": 1,
#                 }).json()["request"]
#             print(f"2captcha submitted, id={capt_id}")
#             # Polling for solution
#             for _ in range(30):
#                 time.sleep(6)
#                 r = requests.get("http://2captcha.com/res.php", params={
#                     "key": self.twocaptcha_key,
#                     "action": "get",
#                     "id": capt_id,
#                     "json": 1,
#                 }).json()
#                 if r["status"] == 1:
#                     print(f"2captcha SOLUTION: {r['request']}")
#                     return r["request"]
#                 elif r["request"] == "CAPCHA_NOT_READY":
#                     continue
#                 else:
#                     print(f"2captcha: {r['request']}")
#                     break
#             print("2captcha: No solution in time")
#             return None
#         except Exception as e:
#             print(f"2captcha error: {e}")
#             return None
#
#     # ----------- ХЕЛПЕРЫ / ДРАГ ----------------
#     def human_like_drag(self, slider: Locator, target_distance: float) -> bool:
#         try:
#             box = slider.bounding_box()
#             if not box:
#                 print("Не удалось получить координаты ползунка")
#                 return False
#             start_x = box['x'] + box['width'] / 2
#             start_y = box['y'] + box['height'] / 2
#             start_x += random.randint(-2, 2)
#             start_y += random.randint(-2, 2)
#             self.page.mouse.move(start_x - 10, start_y)
#             time.sleep(random.uniform(0.1, 0.3))
#             self.page.mouse.move(start_x, start_y)
#             time.sleep(random.uniform(0.1, 0.2))
#             self.page.mouse.down()
#             time.sleep(random.uniform(0.05, 0.1))
#             steps = random.randint(15, 25)
#             for i in range(steps):
#                 progress = (i + 1) / steps
#                 eased_progress = 1 - (1 - progress) ** 3
#                 current = target_distance * eased_progress
#                 jitter_x = random.uniform(-1, 1)
#                 jitter_y = random.uniform(-0.5, 0.5)
#                 self.page.mouse.move(start_x + current + jitter_x, start_y + jitter_y)
#                 time.sleep(random.uniform(0.01, 0.03))
#             self.page.mouse.move(start_x + target_distance, start_y)
#             time.sleep(random.uniform(0.1, 0.2))
#             self.page.mouse.up()
#             return True
#         except Exception as e:
#             print(f"Ошибка drag: {e}")
#             return False
#
#     def _check_success(self, container: Locator) -> bool:
#         try:
#             cc = container.get_attribute('class')
#             if cc and any(x in cc.lower() for x in ('success', 'complete', 'solved', 'valid', 'passed')):
#                 return True
#             slider_button = container.locator('div.captcha-control-button')
#             if slider_button.count() == 0:
#                 return True
#         except Exception as e:
#             print(f"Ошибка проверки успеха: {e}")
#         return False
#
#     # ----------- ОСНОВНЫЕ СЦЕНАРИИ -------------
#
#     def run_gemini(self):
#         if not self.wait_for_captcha_load(60000):
#             print("Капча не найдена")
#             return False
#         captcha_elements = self.find_captcha_elements()
#         if not captcha_elements:
#             print("Элементы капчи не найдены")
#             return False
#         container, _, slider_button = captcha_elements
#         image = self.capture_captcha_image(container)
#         if image:
#             distance = self.solve_captcha_gemini(image)
#         else:
#             distance = 90
#         print(f"Перемещаем слайдер на {distance} пикселей (gemini)")
#         self.human_like_drag(slider_button, distance)
#         time.sleep(3)
#         return self._check_success(container)
#
#     def run_deepseek(self):
#         if not self.wait_for_captcha_load(60000):
#             print("Капча не найдена")
#             return False
#         captcha_elements = self.find_captcha_elements()
#         if not captcha_elements:
#             print("Элементы капчи не найдены")
#             return False
#         container, _, slider_button = captcha_elements
#         image = self.capture_captcha_image(container)
#         if image:
#             distance = self.solve_captcha_deepseek(image)
#         else:
#             distance = 90
#         print(f"Перемещаем слайдер на {distance} пикселей (deepseek)")
#         self.human_like_drag(slider_button, distance)
#         time.sleep(3)
#         return self._check_success(container)
#
# @pytest.mark.parametrize("run", range(100)) # добавить run в параметры функции
# def test_captcha_solver_gemini(run):
#     GEMINI_API_KEY = ""
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#         page.goto("https://www.vseinstrumenti.ru/", wait_until='networkidle')
#         solver = SyncCaptchaSolverAdvanced(page, gemini_api_key=GEMINI_API_KEY)
#         ok = solver.run_gemini()
#         print("Результат Gemini:", ok)
#         time.sleep(4)
#         slider_button = page.locator('div.captcha-control-button')
#         assert slider_button is None
#         browser.close()
#
# def test_captcha_solver_deepseek():
#     DEEPSEEK_API_KEY = ""
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#         page.goto("https://www.vseinstrumenti.ru/", wait_until='networkidle')
#         solver = SyncCaptchaSolverAdvanced(page, deepseek_api_key=DEEPSEEK_API_KEY)
#         ok = solver.run_deepseek()
#         print("Результат Deepseek:", ok)
#         time.sleep(4)
#
#         browser.close()
#
# def test_captcha_solver_2captcha():
#     TWO_CAPTCHA_KEY = "ВАШ_2CAPTCHA_KEY"
#     # Для 2captcha нужно знать тип капчи и/или sitekey, pageurl!
#     PAGE_URL = "https://www.vseinstrumenti.ru/"
#     SITE_KEY = ""  # найдите в html если это рекапча/geetest
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#         page.goto(PAGE_URL, wait_until='networkidle')
#         solver = SyncCaptchaSolverAdvanced(page, twocaptcha_key=TWO_CAPTCHA_KEY)
#         token = solver.solve_captcha_2captcha(PAGE_URL, SITE_KEY)
#         if token:
#             # Как применять токен - зависит от типа капчи (recaptcha: вставить в g-recaptcha-response, geetest — через JS cf. 2captcha docs)
#             print("Токен 2captcha получен:", token)
#         else:
#             print("2captcha не решила")
#         browser.close()


# import base64
# import json
# import random
# import re
# import time
# import requests
# from io import BytesIO
# from typing import Optional, Tuple
# from PIL import Image
# from playwright.sync_api import Page, sync_playwright, Locator
#
# class UniversalCaptchaSolver:
#     def __init__(self, page: Page, *,
#                  gemini_api_key: Optional[str]=None,
#                  gpt_api_key: Optional[str]=None,
#                  deepseek_api_key: Optional[str]=None):
#         self.page = page
#         self.gemini_api_key = gemini_api_key
#         self.gpt_api_key = gpt_api_key
#         self.deepseek_api_key = deepseek_api_key
#
#     def wait_for_captcha_load(self, timeout: int = 10000) -> bool:
#         try:
#             self.page.wait_for_selector('div.captcha-control', timeout=timeout)
#             time.sleep(1)
#             return True
#         except Exception as e:
#             print(f"Капча не загрузилась: {e}")
#             return False
#
#     def find_captcha_elements(self) -> Optional[Tuple[Locator, Locator, Locator]]:
#         try:
#             container = self.page.locator('div.captcha-control')
#             slider_wrap = self.page.locator('div.captcha-control-wrap')
#             slider_button = self.page.locator('div.captcha-control-button')
#             if container.count() > 0 and slider_wrap.count() > 0 and slider_button.count() > 0:
#                 return container, slider_wrap, slider_button
#         except Exception as e:
#             print(f"Ошибка при поиске элементов: {e}")
#         return None
#
#     def capture_captcha_image(self, container: Locator) -> Optional[Image.Image]:
#         try:
#             box = container.bounding_box()
#             screenshot = self.page.screenshot()
#             full_img = Image.open(BytesIO(screenshot))
#             cropped = full_img.crop((box['x'], box['y'], box['x'] + box['width'], box['y'] + box['height']))
#             return cropped
#         except Exception as e:
#             print(f"Ошибка при захвате изображения: {e}")
#             return None
#
#     # ------- GPT-Vision --------
#     def solve_captcha_gpt(self, image: Image.Image) -> Optional[float]:
#         try:
#             buf = BytesIO()
#             image.save(buf, format='PNG')
#             base64_img = base64.b64encode(buf.getvalue()).decode('utf-8')
#             headers = {
#                 "Content-Type": "application/json",
#                 "Authorization": f"Bearer {self.gpt_api_key}"
#             }
#             data = {
#                 "model": "gpt-4o",
#                 "messages": [
#                     {"role": "system", "content": "You are a helpful assistant for pixel-precise slider captcha solving. Respond only with the number of horizontal pixels to move."},
#                     {"role": "user", "content": [
#                         {
#                             "type": "text",
#                             "text": "Проанализируй полученую картинку, она перевернута. На сколько пикселей требуется передвинуть слайдер, чтобы картинка выравнялись по горизонтали, 1 гразус поворота картинки равен 2 пикселя. В ответ передай только целое число. Если ты не получил изображение напиши 99",
#                         },
#                         {
#                             "type": "image_url",
#                             "image_url": {"url": f"data:image/png;base64,{base64_img}"}
#                         }
#                     ]}
#                 ],
#                 "max_tokens": 8
#             }
#             url = "https://api.openai.com/v1/chat/completions"
#             resp = requests.post(url, json=data, headers=headers, timeout=40)
#             result = resp.json()
#             print("GPT-4o Vision ответ:", result)
#             answer = str(result.get("choices", [{}])[0].get("message", {}).get("content", ""))
#             nums = re.findall(r"\d{2,4}", answer)
#             if nums and 10 <= int(nums[0]) <= 500:
#                 return float(nums[0])
#             return None
#         except Exception as e:
#             print(f"GPT-Vision error: {e}")
#             return None
#
#     # ------- Gemini --------
#     def solve_captcha_gemini(self, image: Image.Image) -> Optional[float]:
#         buf = BytesIO()
#         image.save(buf, format='PNG')
#         base64_img = base64.b64encode(buf.getvalue()).decode('utf-8')
#         headers = {"Content-Type": "application/json"}
#         data = {
#             "contents": [{
#                 "parts": [
#                     {"text": "How many pixels should I move this slider to solve the puzzle? Respond with a single integer."},
#                     {"inlineData": {"mimeType": "image/png", "data": base64_img}}
#                 ]
#             }]
#         }
#         url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
#         try:
#             resp = requests.post(url, json=data, headers=headers, timeout=40)
#             rj = resp.json()
#             print("Gemini ответ:", rj)
#             answer = ""
#             if 'candidates' in rj and rj['candidates']:
#                 parts = rj['candidates'][0].get('content', {}).get('parts', [])
#                 if parts:
#                     answer = parts[0].get('text', '')
#             nums = re.findall(r"\d{2,4}", answer)
#             if nums and 10 <= int(nums[0]) <= 500:
#                 return float(nums[0])
#             return None
#         except Exception as e:
#             print(f"Gemini error: {e}")
#             return None
#
#     # ------- DeepSeek --------
#     def solve_captcha_deepseek(self, image: Image.Image) -> Optional[float]:
#         buf = BytesIO()
#         image.save(buf, format='PNG')
#         base64_img = base64.b64encode(buf.getvalue()).decode('utf-8')
#         headers = {"Authorization": f"Bearer {self.deepseek_api_key}"}
#         data = {
#             "model": "deepseek-coder",
#             "messages": [
#                 {"role": "user", "content": "Give the horizontal slider distance (in pixels as integer only) to solve this slider captcha."},
#                 {"role": "user", "content": {"image": base64_img}}
#             ]
#         }
#         try:
#             resp = requests.post("https://api.deepseek.com/v1/chat/completions", json=data, headers=headers, timeout=40)
#             rj = resp.json()
#             print("DeepSeek ответ:", rj)
#             answer = str(rj)
#             nums = re.findall(r"\d{2,4}", answer)
#             if nums and 10 <= int(nums[0]) <= 500:
#                 return float(nums[0])
#             return None
#         except Exception as e:
#             print(f"DeepSeek error: {e}")
#             return None
#
#     def human_like_drag(self, slider: Locator, target_distance: float) -> bool:
#         try:
#             box = slider.bounding_box()
#             if not box:
#                 print("Не удалось получить координаты ползунка")
#                 return False
#             # Плавное движение с микродрожанием
#             start_x = box['x'] + box['width'] / 2
#             start_y = box['y'] + box['height'] / 2
#             self.page.mouse.move(start_x, start_y)
#             self.page.mouse.down()
#             steps = random.randint(17, 27)
#             for i in range(steps):
#                 progress = (i + 1) / steps
#                 eased = 1 - (1 - progress) ** 3
#                 cur = target_distance * eased
#                 jitter_x = random.uniform(-1, 1)
#                 jitter_y = random.uniform(-0.7, 0.7)
#                 self.page.mouse.move(start_x + cur + jitter_x, start_y + jitter_y)
#                 time.sleep(random.uniform(0.01, 0.03))
#             self.page.mouse.move(start_x + target_distance, start_y)
#             time.sleep(random.uniform(0.07, 0.12))
#             self.page.mouse.up()
#             return True
#         except Exception as e:
#             print(f"Ошибка drag: {e}")
#             return False
#
#     def _check_success(self, container: Locator) -> bool:
#         try:
#             cc = container.get_attribute('class')
#             if cc and any(x in cc.lower() for x in ('success', 'complete', 'solved', 'valid', 'passed')):
#                 return True
#             slider_button = container.locator('div.captcha-slider-button')
#             if slider_button.count() == 0:
#                 return True
#         except Exception as e:
#             print(f"Ошибка проверки успеха: {e}")
#         return False
#
#     def solve_slider_captcha_with_retries(self, provider_priority=None, max_attempts=8) -> bool:
#         if provider_priority is None:
#             provider_priority = [
#                 'gpt', 'gemini', 'deepseek'
#             ]
#         if not self.wait_for_captcha_load(60000):
#             print("Капча не найдена")
#             return False
#         captcha_elements = self.find_captcha_elements()
#         if not captcha_elements:
#             print("Элементы капчи не найдены")
#             return False
#         container, _, slider_button = captcha_elements
#
#         for attempt in range(1, max_attempts + 1):
#             print(f"\n===== Попытка решения №{attempt} =====")
#             image = self.capture_captcha_image(container)
#             pixels = None
#             for prov in provider_priority:
#                 if prov == "gpt" and self.gpt_api_key and image:
#                     pixels = self.solve_captcha_gpt(image)
#                 elif prov == "gemini" and self.gemini_api_key and image and not pixels:
#                     pixels = self.solve_captcha_gemini(image)
#                 elif prov == "deepseek" and self.deepseek_api_key and image and not pixels:
#                     pixels = self.solve_captcha_deepseek(image)
#                 if pixels:
#                     print(f"Рассчитанное расстояние ({prov}): {pixels}")
#                     break
#             if not pixels:
#                 print("Не удалось вычислить точное расстояние, fallback 100")
#                 pixels = 100
#             self.human_like_drag(slider_button, pixels)
#             time.sleep(random.uniform(2.2, 3.5))
#             if self._check_success(container):
#                 print(f"✅ Капча успешно решена на {attempt} попытке!")
#                 return True
#             else:
#                 print(f"❌ Капча НЕ решена (попытка {attempt})")
#         print("😞 Все попытки исчерпаны, не удалось решить капчу")
#         return False
#
# # --------------- Пример теста ------------------
#
# def test_captcha_solver_all():
#     GEMINI_API_KEY = "ВАШ_GEMINI_API_KEY"
#     GPT_API_KEY = ""
#     DEEPSEEK_API_KEY = ""
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#         page.goto("https://www.vseinstrumenti.ru/", wait_until='networkidle')
#         solver = UniversalCaptchaSolver(
#             page,
#             gemini_api_key=GEMINI_API_KEY,
#             gpt_api_key=GPT_API_KEY,
#             deepseek_api_key=DEEPSEEK_API_KEY,
#         )
#         solved = solver.solve_slider_captcha_with_retries()
#         print("Финальный результат:", solved)
#         time.sleep(4)
#         browser.close()



# import base64
# import json
# import random
# import re
# import time
# import requests
# from io import BytesIO
# from typing import Optional, Tuple, List
# from PIL import Image
# from playwright.sync_api import Page, sync_playwright, Locator
# import pytest
#
# class SyncCaptchaSolverAdvanced:
#     def __init__(self, page: Page, gemini_api_key: Optional[str]=None, deepseek_api_key: Optional[str]=None, twocaptcha_key: Optional[str]=None):
#         self.page = page
#         self.gemini_api_key = gemini_api_key
#         self.deepseek_api_key = deepseek_api_key
#         self.twocaptcha_key = twocaptcha_key
#
#     # --- УЛУЧШЕНИЯ ДЛЯ "ЧЕЛОВЕЧНОСТИ" ПОВЕДЕНИЯ В HEADLESS ---
#     def prepare_human_like_environment(self):
#         # Устанавливаем user-agent, viewport, и маскируем webdriver
#         self.page.context.set_default_timeout(60000)
#         self.page.add_init_script("""
#             Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
#             Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru', 'en-US', 'en']});
#             Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
#             window.chrome = { runtime: {} };
#             // Mock permissions API (e.g. GeoLocation)
#             const originalQuery = window.navigator.permissions.query;
#             window.navigator.permissions.query = (parameters) => (
#                 parameters.name === 'notifications' ?
#                     Promise.resolve({ state: Notification.permission }) :
#                     originalQuery(parameters)
#             );
#         """)
#
#     # --- Ожидание капчи ---
#     def wait_for_captcha_load(self, timeout: int = 10000) -> bool:
#         try:
#             self.page.wait_for_selector('div.captcha-control', timeout=timeout)
#             time.sleep(1)
#             return True
#         except Exception as e:
#             print(f"Капча не загрузилась: {e}")
#             return False
#
#     def find_captcha_elements(self) -> Optional[Tuple[Locator, Locator, Locator]]:
#         try:
#             container = self.page.locator('div.captcha-control')
#             slider_wrap = self.page.locator('div.captcha-control-wrap')
#             slider_button = self.page.locator('div.captcha-control-button')
#             if container.count() > 0 and slider_wrap.count() > 0 and slider_button.count() > 0:
#                 return container, slider_wrap, slider_button
#         except Exception as e:
#             print(f"Ошибка при поиске элементов: {e}")
#         return None
#
#     def capture_captcha_image(self, container: Locator) -> Optional[Image.Image]:
#         try:
#             box = container.bounding_box()
#             screenshot = self.page.screenshot()
#             full_img = Image.open(BytesIO(screenshot))
#             cropped = full_img.crop((box['x'], box['y'], box['x'] + box['width'], box['y'] + box['height']))
#             return cropped
#         except Exception as e:
#             print(f"Ошибка при захвате изображения: {e}")
#             return None
#
#     # Здесь должна быть реализация solve_captcha_gemini и других (взяты из вашего кода, не повторяю для компактности)
#
#     def solve_captcha_gemini(self, image: Image.Image) -> Optional[float]:
#         buf = BytesIO()
#         image.save(buf, format='PNG')
#         base64_img = base64.b64encode(buf.getvalue()).decode('utf-8')
#         headers = {"Content-Type": "application/json"}
#         data = {
#             "contents": [{
#                 "parts": [
#                     {"text": "How many pixels should I move this slider to solve the puzzle? Respond with a single integer."},
#                     {"inlineData": {"mimeType": "image/png", "data": base64_img}}
#                 ]
#             }]
#         }
#         url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
#         try:
#             resp = requests.post(url, json=data, headers=headers, timeout=40)
#             rj = resp.json()
#             print("Gemini ответ:", rj)
#             answer = ""
#             if 'candidates' in rj and rj['candidates']:
#                 parts = rj['candidates'][0].get('content', {}).get('parts', [])
#                 if parts:
#                     answer = parts[0].get('text', '')
#             nums = re.findall(r"\d{2,4}", answer)
#             if nums and 10 <= int(nums[0]) <= 500:
#                 return float(nums[0])
#             return None
#         except Exception as e:
#             print(f"Gemini error: {e}")
#             return None
#
#
#     def human_like_drag(self, slider: Locator, target_distance: float) -> bool:
#         try:
#             box = slider.bounding_box()
#             if not box:
#                 print("Не удалось получить координаты ползунка")
#                 return False
#             start_x = box['x'] + box['width'] / 2
#             start_y = box['y'] + box['height'] / 2
#             start_x += random.randint(-2, 2)
#             start_y += random.randint(-2, 2)
#             self.page.mouse.move(start_x - 10, start_y)
#             time.sleep(random.uniform(0.1, 0.3))
#             self.page.mouse.move(start_x, start_y)
#             time.sleep(random.uniform(0.1, 0.2))
#             self.page.mouse.down()
#             time.sleep(random.uniform(0.05, 0.1))
#             steps = random.randint(15, 25)
#             for i in range(steps):
#                 progress = (i + 1) / steps
#                 eased_progress = 1 - (1 - progress) ** 3
#                 current = target_distance * eased_progress
#                 jitter_x = random.uniform(-1, 1)
#                 jitter_y = random.uniform(-0.5, 0.5)
#                 self.page.mouse.move(start_x + current + jitter_x, start_y + jitter_y)
#                 time.sleep(random.uniform(0.01, 0.03))
#             self.page.mouse.move(start_x + target_distance, start_y)
#             time.sleep(random.uniform(0.1, 0.2))
#             self.page.mouse.up()
#             return True
#         except Exception as e:
#             print(f"Ошибка drag: {e}")
#             return False
#
#     def _check_success(self, container: Locator) -> bool:
#         try:
#             cc = container.get_attribute('class')
#             if cc and any(x in cc.lower() for x in ('success', 'complete', 'solved', 'valid', 'passed')):
#                 return True
#             slider_button = container.locator('div.captcha-control-button')
#             if slider_button.count() == 0:
#                 return True
#             return False
#         except Exception as e:
#             print(f"Ошибка проверки успеха: {e}")
#             return False
#
#     # Главный цикл с повторными попытками (до 10, проверка кнопки после 5 сек)
#     def solve_with_retries(self, max_attempts=10):
#         for attempt in range(1, max_attempts + 1):
#             print(f"\nПопытка решения №{attempt}")
#             if not self.wait_for_captcha_load(60000):
#                 print("Капча не найдена")
#                 return False
#             captcha_elements = self.find_captcha_elements()
#             if not captcha_elements:
#                 print("Элементы капчи не найдены")
#                 return False
#             container, _, slider_button = captcha_elements
#
#             image = self.capture_captcha_image(container)
#             if image and self.gemini_api_key:
#                 distance = self.solve_captcha_gemini(image)
#             else:
#                 print("Нет ответа от нейронки, двигаем на 90 пикселей")
#                 distance = 90.0
#
#             self.human_like_drag(slider_button, distance)
#
#             # Ждем 5 секунд после движения, чтобы увидеть результат
#             time.sleep(5)
#             slider_button = self.page.locator('div.captcha-control-button')
#
#             if slider_button.count() == 0:
#                 print("Капча пройдена!")
#                 return True
#             else:
#                 print(f"Капча не пройдена, повторяем попытку {attempt}/{max_attempts}")
#
#                 # Перезагрузить страницу и повторить
#                 self.page.reload(wait_until='networkidle')
#                 # Восстановить человеческие маски
#                 self.prepare_human_like_environment()
#
#         print("Не удалось пройти капчу за 10 попыток")
#         return False
#
#
# # Отдельный тест только с движением на 90 пикселей (без нейронки)
# def test_move_slider_fixed_90_pixels():
#     max_attempts = 10
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, args=[
#             '--disable-blink-features=AutomationControlled',
#             '--disable-web-security',
#             '--disable-features=IsolateOrigins,site-per-process',
#             '--window-size=1366,768',
#         ])
#         context = browser.new_context(
#             user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#             viewport={'width': 1366, 'height': 768}
#         )
#         page = context.new_page()
#         page.add_init_script("""
#             Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
#             Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru', 'en-US', 'en']});
#             Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
#             window.chrome = { runtime: {} };
#         """)
#
#         page.goto("https://www.vseinstrumenti.ru/", wait_until='networkidle')
#         for attempt in range(1, max_attempts + 1):
#             print(f"\nПопытка #{attempt}")
#             container = page.locator('div.captcha-control')
#             slider_wrap = page.locator('div.captcha-control-wrap')
#             slider_button = page.locator('div.captcha-control-button')
#             if container.count() == 0 or slider_wrap.count() == 0 or slider_button.count() == 0:
#                 print("Капча не найдена, пропуск попытки")
#                 continue
#             box = slider_button.bounding_box()
#             if not box:
#                 print("Bounding box не найден")
#                 continue
#             start_x = box['x'] + box['width'] / 2 + random.randint(-2, 2)
#             start_y = box['y'] + box['height'] / 2 + random.randint(-2, 2)
#             try:
#                 page.mouse.move(start_x, start_y)
#                 page.mouse.down()
#                 steps = random.randint(15, 25)
#                 for i in range(steps):
#                     progress = (i + 1) / steps
#                     eased = 1 - (1 - progress) ** 3
#                     cur = 90 * eased
#                     jitter_x = random.uniform(-1, 1)
#                     jitter_y = random.uniform(-0.5, 0.5)
#                     page.mouse.move(start_x + cur + jitter_x, start_y + jitter_y)
#                     time.sleep(random.uniform(0.01, 0.03))
#                 page.mouse.move(start_x + 90, start_y)
#                 time.sleep(random.uniform(0.1, 0.2))
#                 page.mouse.up()
#             except Exception as e:
#                 print(f"Ошибка drag: {e}")
#                 continue
#
#             print("Двигаем ползунок на 90 пикселей...")
#             time.sleep(15)
#
#             # После действия проверяем именно на свежем локаторе
#             if page.locator('div.captcha-control-button').count() == 0:
#                 print("Капча пройдена на попытке", attempt)
#                 browser.close()
#                 return
#             else:
#                 print("Капча не пройдена, пробуем еще раз")
#
#         print("Не удалось пройти капчу за 10 попыток")
#         browser.close()
#         assert False, "Не удалось пройти капчу за 10 попыток"
#
#
# # Пример использования основного решения с повторами и человеческой маскировкой:
# @pytest.mark.parametrize("run", range(1))  # по желанию расширить количество повторов
# def test_captcha_solver_gemini_with_retries(run):
#     GEMINI_API_KEY = ""
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, args=[
#             '--disable-blink-features=AutomationControlled',
#             '--disable-web-security',
#             '--disable-features=IsolateOrigins,site-per-process',
#             '--window-size=1366,768',
#         ])
#         context = browser.new_context(
#             user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#             viewport={'width': 1366, 'height': 768}
#         )
#         page = context.new_page()
#         page.add_init_script("""
#             Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
#             Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru', 'en-US', 'en']});
#             Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
#             window.chrome = { runtime: {} };
#         """)
#
#         page.goto("https://www.vseinstrumenti.ru/", wait_until='networkidle')
#
#         solver = SyncCaptchaSolverAdvanced(page, gemini_api_key=GEMINI_API_KEY)
#         result = solver.solve_with_retries(max_attempts=10)
#         assert result, "Не удалось пройти капчу за 10 попыток"
#         time.sleep(4)
#         browser.close()









# нормальный вариант, но гемини не делает несколько попыток + все через тайм слипы
# import base64
# import json
# import random
# import re
# import time
# import requests
# from io import BytesIO
# from typing import Optional, Tuple
# from PIL import Image
# from playwright.sync_api import Page, sync_playwright, Locator
# import pytest
#
#
# def wait_slider_button_absent(page, selector, timeout=12):
#     """Ждать исчезновения движка капчи, устойчиво к обновлениям контекста"""
#     for t in range(timeout):
#         try:
#             loc = page.locator(selector)
#             if loc.count() == 0:
#                 return True
#         except Exception as e:
#             print(f"Ошибка проверки локатора (попытка {t + 1}): {e}")
#         time.sleep(1)
#     return False
#
# class SyncCaptchaSolverAdvanced:
#     def __init__(self, page: Page, gemini_api_key: Optional[str]=None):
#         self.page = page
#         self.gemini_api_key = gemini_api_key
#
#
#
#     def prepare_human_like_environment(self):
#         self.page.context.set_default_timeout(60000)
#         self.page.add_init_script("""
#             Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
#             Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru', 'en-US', 'en']});
#             Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
#             window.chrome = { runtime: {} };
#         """)
#
#     def wait_for_captcha_load(self, timeout: int = 15000) -> bool:
#         try:
#             self.page.wait_for_selector('div.captcha-control', timeout=timeout)
#             time.sleep(1)
#             return True
#         except Exception as e:
#             print(f"Капча не загрузилась: {e}")
#             return False
#
#     def find_captcha_elements(self) -> Optional[Tuple[Locator, Locator, Locator]]:
#         try:
#             container = self.page.locator('div.captcha-control')
#             slider_wrap = self.page.locator('div.captcha-control-wrap')
#             slider_button = self.page.locator('div.captcha-control-button')
#             if container.count() > 0 and slider_wrap.count() > 0 and slider_button.count() > 0:
#                 return container, slider_wrap, slider_button
#         except Exception as e:
#             print(f"Ошибка при поиске элементов: {e}")
#         return None
#
#     def capture_captcha_image(self, container: Locator) -> Optional[Image.Image]:
#         try:
#             box = container.bounding_box()
#             screenshot = self.page.screenshot()
#             full_img = Image.open(BytesIO(screenshot))
#             cropped = full_img.crop((box['x'], box['y'], box['x'] + box['width'], box['y'] + box['height']))
#             return cropped
#         except Exception as e:
#             print(f"Ошибка при захвате изображения: {e}")
#             return None
#
#     def solve_captcha_gemini(self, image: Image.Image) -> Optional[float]:
#         buf = BytesIO()
#         image.save(buf, format='PNG')
#         base64_img = base64.b64encode(buf.getvalue()).decode('utf-8')
#         headers = {"Content-Type": "application/json"}
#         data = {
#             "contents": [{
#                 "parts": [
#                     {"text": "What is the pixel offset required to solve this slider captcha?"},
#                     {"inlineData": {"mimeType": "image/png", "data": base64_img}}
#                 ]
#             }]
#         }
#         url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
#         try:
#             resp = requests.post(url, json=data, headers=headers, timeout=40)
#             rj = resp.json()
#             print("Gemini ответ:", rj)
#             answer = ""
#             if 'candidates' in rj and rj['candidates']:
#                 parts = rj['candidates'][0].get('content', {}).get('parts', [])
#                 if parts:
#                     answer = parts[0].get('text', '')
#             nums = re.findall(r"\d{2,4}", answer)
#             if nums and 10 <= int(nums[0]) <= 500:
#                 return float(nums[0])
#         except Exception as e:
#             print(f"Gemini error: {e}")
#         return None
#
#     def human_like_drag(self, slider: Locator, target_distance: float) -> bool:
#         try:
#             box = slider.bounding_box()
#             if not box:
#                 print("Не удалось получить координаты ползунка")
#                 return False
#             start_x = box['x'] + box['width'] / 2
#             start_y = box['y'] + box['height'] / 2
#             start_x += random.randint(-2, 2)
#             start_y += random.randint(-2, 2)
#             self.page.mouse.move(start_x - 10, start_y)
#             time.sleep(random.uniform(0.1, 0.3))
#             self.page.mouse.move(start_x, start_y)
#             time.sleep(random.uniform(0.1, 0.2))
#             self.page.mouse.down()
#             time.sleep(random.uniform(0.05, 0.1))
#             steps = random.randint(15, 25)
#             for i in range(steps):
#                 progress = (i + 1) / steps
#                 eased_progress = 1 - (1 - progress) ** 3
#                 current = target_distance * eased_progress
#                 jitter_x = random.uniform(-1, 1)
#                 jitter_y = random.uniform(-0.5, 0.5)
#                 self.page.mouse.move(start_x + current + jitter_x, start_y + jitter_y)
#                 time.sleep(random.uniform(0.01, 0.03))
#             self.page.mouse.move(start_x + target_distance, start_y)
#             time.sleep(random.uniform(0.1, 0.2))
#             self.page.mouse.up()
#             return True
#         except Exception as e:
#             print(f"Ошибка drag: {e}")
#             return False
#
#     def solve_with_retries(self, max_attempts=10):
#         for attempt in range(1, max_attempts + 1):
#             print(f"\nПопытка решения №{attempt}")
#             if not self.wait_for_captcha_load(15000):
#                 print("Капча не найдена")
#                 continue
#             captcha_elements = self.find_captcha_elements()
#             if not captcha_elements:
#                 print("Элементы капчи не найдены")
#                 continue
#             container, _, slider_button = captcha_elements
#
#             image = self.capture_captcha_image(container)
#             distance = None
#             if image and self.gemini_api_key:
#                 distance = self.solve_captcha_gemini(image)
#             if distance is None:
#                 print("Нет ответа от нейронки, двигаем на 90 пикселей")
#                 distance = 90.0
#             self.human_like_drag(slider_button, distance)
#
#             # Ждем появления новой капчи (до 12 сек), ловим ошибки пересоздания контекста
#             print("Ждем появления новой или исчезновения старой кнопки...")
#             for t in range(12):
#                 try:
#                     # Создаем новый локатор на каждый шаг
#                     slider_btn = self.page.locator('div.captcha-control-button')
#                     # Если кнопка исчезла — успех!
#                     if slider_btn.count() == 0:
#                         print("Капча пройдена!")
#                         return True
#                     # Если есть — возможно уже обновился контекст, кнопка другая. Ждем!
#                 except Exception as e:
#                     print(f"Ошибка проверки локатора (попытка {t + 1}): {e}")
#                     # Вероятно, navigation изнутри капчи, даем странице обновиться
#                 time.sleep(1)
#
#             print(f"Капча не пройдена, повторяем попытку {attempt}/{max_attempts}")
#
#         print("Не удалось пройти капчу за 10 попыток")
#         return False
#
#
#
# def test_move_slider_fixed_90_pixels():
#     max_attempts = 10
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, args=[
#             '--disable-blink-features=AutomationControlled',
#             '--disable-web-security',
#             '--disable-features=IsolateOrigins,site-per-process',
#             '--window-size=1366,768',
#         ])
#         context = browser.new_context(
#             user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#             viewport={'width': 1366, 'height': 768}
#         )
#         page = context.new_page()
#         page.add_init_script("""
#             Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
#             Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru', 'en-US', 'en']});
#             Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
#             window.chrome = { runtime: {} };
#         """)
#
#         page.goto("https://www.vseinstrumenti.ru/", wait_until='networkidle')
#         for attempt in range(1, max_attempts + 1):
#             print(f"\nПопытка #{attempt}")
#             slider_button = page.locator('div.captcha-control-button')
#             if slider_button.count() == 0:
#                 print("Капча не найдена, пропуск попытки")
#                 continue
#             box = slider_button.bounding_box()
#             if not box:
#                 print("Bounding box не найден")
#                 continue
#             start_x = box['x'] + box['width'] / 2 + random.randint(-2, 2)
#             start_y = box['y'] + box['height'] / 2 + random.randint(-2, 2)
#             try:
#                 page.mouse.move(start_x, start_y)
#                 page.mouse.down()
#                 steps = random.randint(15, 25)
#                 for i in range(steps):
#                     progress = (i + 1) / steps
#                     eased = 1 - (1 - progress) ** 3
#                     cur = 90 * eased
#                     jitter_x = random.uniform(-1, 1)
#                     jitter_y = random.uniform(-0.5, 0.5)
#                     page.mouse.move(start_x + cur + jitter_x, start_y + jitter_y)
#                     time.sleep(random.uniform(0.01, 0.03))
#                 page.mouse.move(start_x + 90, start_y)
#                 time.sleep(random.uniform(0.1, 0.2))
#                 page.mouse.up()
#             except Exception as e:
#                 print(f"Ошибка drag: {e}")
#                 time.sleep(2)
#                 continue
#
#             print("Двигаем ползунок на 90 пикселей...")
#             slider_btn = page.wait_for_selector('div.captcha-control-button')
#             page.wait_for_selector('div.captcha-control-button', timeout=10000)
#
#             # ...движение мышкой...
#             # Ждем обновления капчи (до 12 секунд), не валимся по ошибке навигации!
#             if wait_slider_button_absent(page, 'div.captcha-control-button', timeout=12):
#                 print(f"Капча пройдена на попытке {attempt}")
#                 browser.close()
#                 return
#             else:
#                 print(f"Капча не пройдена, пробуем еще раз")
#
#         print("Не удалось пройти капчу за 10 попыток")
#         browser.close()
#         assert False, "Не удалось пройти капчу за 10 попыток"
#
#
# @pytest.mark.parametrize("run", range(1))
# def test_captcha_solver_gemini_with_retries(run):
#     GEMINI_API_KEY = ""
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, args=[
#             '--disable-blink-features=AutomationControlled',
#             '--disable-web-security',
#             '--disable-features=IsolateOrigins,site-per-process',
#             '--window-size=1366,768',
#         ])
#         context = browser.new_context(
#             user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#             viewport={'width': 1366, 'height': 768}
#         )
#         page = context.new_page()
#         page.add_init_script("""
#             Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
#             Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru', 'en-US', 'en']});
#             Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
#             window.chrome = { runtime: {} };
#         """)
#
#         page.goto("https://www.vseinstrumenti.ru/", wait_until='networkidle')
#         solver = SyncCaptchaSolverAdvanced(page, gemini_api_key=GEMINI_API_KEY)
#         result = solver.solve_with_retries(max_attempts=10)
#         assert result, "Не удалось пройти капчу за 10 попыток"
#         time.sleep(7)
#         browser.close()









"""Рабочи метод с быстрым брутфорсом капчи"""


# import base64
# import json
# import random
# import re
# import requests
# from io import BytesIO
# from typing import Optional, Tuple
# from PIL import Image
# from playwright.sync_api import Page, sync_playwright, TimeoutError as PwTimeout
# import pytest
#
# def page_contains_forbidden(page):
#     try:
#         body_text = page.content().lower()
#         if "forbidden" in body_text:
#             print("На странице найден forbidden — бан или антибот.")
#             return True
#     except Exception as e:
#         print(f"Ошибка при попытке получить текст страницы: {e}")
#     return False
#
# class SyncCaptchaSolverAdvanced:
#
#
#     def __init__(self, page: Page, gemini_api_key: Optional[str]=None):
#         self.page = page
#         self.gemini_api_key = gemini_api_key
#
#     def prepare_human_like_environment(self):
#         self.page.context.set_default_timeout(60000)
#         self.page.add_init_script("""
#             Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
#             Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru', 'en-US', 'en']});
#             Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
#             window.chrome = { runtime: {} };
#         """)
#
#     def wait_for_captcha_load(self, timeout: int = 15000) -> bool:
#         try:
#             self.page.wait_for_selector('div.captcha-control', timeout=timeout)
#             return True
#         except Exception as e:
#             print(f"Капча не загрузилась: {e}")
#             return False
#
#     def find_captcha_elements(self) -> tuple[Locator, Locator, Locator] | None:
#         try:
#             container = self.page.locator('div.captcha-control')
#             slider_wrap = self.page.locator('div.captcha-control-wrap')
#             slider_button = self.page.locator('div.captcha-control-button')
#             if container.count() > 0 and slider_wrap.count() > 0 and slider_button.count() > 0:
#                 return container, slider_wrap, slider_button
#         except Exception as e:
#             print(f"Ошибка при поиске элементов: {e}")
#         return None
#
#     def capture_captcha_image(self, container: Page) -> Optional[Image.Image]:
#         try:
#             box = container.bounding_box()
#             screenshot = self.page.screenshot()
#             full_img = Image.open(BytesIO(screenshot))
#             cropped = full_img.crop((box['x'], box['y'], box['x'] + box['width'], box['y'] + box['height']))
#             return cropped
#         except Exception as e:
#             print(f"Ошибка при захвате изображения: {e}")
#             return None
#
#     def solve_captcha_gemini(self, image: Image.Image) -> Optional[float]:
#         buf = BytesIO()
#         image.save(buf, format='PNG')
#         base64_img = base64.b64encode(buf.getvalue()).decode('utf-8')
#         headers = {"Content-Type": "application/json"}
#         data = {
#             "contents": [{
#                 "parts": [
#                     {"text": "How many pixels should I move this slider to solve the puzzle? Give a number only."},
#                     {"inlineData": {"mimeType": "image/png", "data": base64_img}}
#                 ]
#             }]
#         }
#         url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
#         try:
#             resp = requests.post(url, json=data, headers=headers, timeout=40)
#             rj = resp.json()
#             print("Gemini ответ:", rj)
#             answer = ""
#             if 'candidates' in rj and rj['candidates']:
#                 parts = rj['candidates'][0].get('content', {}).get('parts', [])
#                 if parts:
#                     answer = parts[0].get('text', '')
#             nums = re.findall(r"\d{2,4}", answer)
#             if nums and 10 <= int(nums[0]) <= 500:
#                 return float(nums[0])
#         except Exception as e:
#             print(f"Gemini error: {e}")
#         return None
#
#     def human_like_drag(self, slider, target_distance: float) -> bool:
#         try:
#             box = slider.bounding_box()
#             if not box:
#                 print("Не удалось получить координаты ползунка")
#                 return False
#
#             # [1] Задержка перед началом - имитация реакции человека (например, 0.7-2.3 сек)
#             think_delay = random.uniform(0.7, 2.3)
#             print(f"Жду перед действием (имитируем раздумье): {think_delay:.2f} сек")
#             time.sleep(think_delay)
#
#             start_x = box['x'] + box['width'] / 2
#             start_y = box['y'] + box['height'] / 2
#
#             # [2] Наводим мышь к слайдеру с паузами (движение поступательно, не в одну линию)
#             approach_steps = random.randint(5, 8)
#             approach_path = []
#             for i in range(approach_steps):
#                 progress = (i + 1) / approach_steps
#                 inter_x = start_x * progress + (start_x - 150) * (1 - progress) + random.uniform(-8, 8)
#                 inter_y = start_y + random.uniform(-3, 3)
#                 approach_path.append((inter_x, inter_y))
#             # старт вне зоны, к кнопке с задержками
#             self.page.mouse.move(start_x - 150, start_y + random.randint(-10, 10))
#             for (x, y) in approach_path:
#                 self.page.mouse.move(x, y)
#                 time.sleep(random.uniform(0.06, 0.14))
#             # финальное наведение точно на кнопку
#             self.page.mouse.move(start_x, start_y)
#             time.sleep(random.uniform(0.09, 0.20))
#
#             # [3] Держим кнопку вниз
#             self.page.mouse.down()
#             time.sleep(random.uniform(0.03, 0.09))
#
#             # [4] Движение с рывками, мини-ступеньками, неравномерно, иногда полностью останавливаемся или дергаем мышку назад или вниз
#             path_steps = random.randint(18, 29)
#             for i in range(path_steps):
#                 progress = (i + 1) / path_steps
#                 # "нервность" — иногда слегка уходим в минус/назад или чуть вниз
#                 jitter_back = -3 if (random.random() < 0.08 and i > 0) else 0
#                 jitter_x = random.uniform(-1.5, 1.5) + jitter_back
#                 jitter_y = random.uniform(-2.3, 2.3)
#                 if random.random() < 0.12 and i > 4:
#                     # Иногда неожиданно делаем паузу прям секундную на середине!
#                     print("Пауза внутри движения!")
#                     time.sleep(random.uniform(0.12, 0.30))
#                 # делаем рывок более "ступенчатым"
#                 step_base = target_distance * progress
#                 extra_jerk = random.uniform(-2, 3) if (i % 7 == 0) else 0
#                 cur = step_base + jitter_x + extra_jerk
#                 self.page.mouse.move(start_x + cur, start_y + jitter_y)
#                 time.sleep(random.uniform(0.018, 0.057))
#             # финальная точка (имитация недодвига и потом быстрого дохвата)
#             self.page.mouse.move(start_x + target_distance - random.randint(1, 6), start_y + random.randint(-2, 2))
#             time.sleep(random.uniform(0.07, 0.145))
#             self.page.mouse.move(start_x + target_distance, start_y)
#             time.sleep(random.uniform(0.06, 0.12))
#             self.page.mouse.up()
#             print("Человеческое движение завершено")
#             return True
#         except Exception as e:
#             print(f"Ошибка drag: {e}")
#             return False
#
#     def solve_with_retries(self, gemini_mode=False, max_attempts=10):
#         for attempt in range(1, max_attempts + 1):
#             print(f"\nПопытка #{attempt}")
#             if page_contains_forbidden(self.page):
#                 assert False, f"Тест остановлен: найден forbidden на попытке {attempt}"
#             if not self.wait_for_captcha_load(15000):
#                 print("Капча не найдена")
#                 continue
#             captcha_elements = self.find_captcha_elements()
#             if not captcha_elements:
#                 print("Элементы капчи не найдены")
#                 continue
#             container, _, slider_button = captcha_elements
#
#             if gemini_mode and self.gemini_api_key:
#                 image = self.capture_captcha_image(container)
#                 distance = self.solve_captcha_gemini(image) if image else None
#                 if distance is None:
#                     print("Нет ответа от нейронки, двигаем на 90 пикселей")
#                     distance = 90.0
#             else:
#                 distance = 90.0
#
#             self.human_like_drag(slider_button, distance)
#
#             # Ждем пропадания кнопки ― динамически, без sleep!
#             try:
#                 self.page.wait_for_selector('div.captcha-control-button', timeout=7000, state='detached')
#             except PwTimeout:
#                 print("Кнопка не исчезла после drag (7 сек), пробуем еще раз!")
#                 continue
#
#             # Теперь ждем (до 10 сек) появления новой кнопки ― если не появилась, значит, все решено!
#             try:
#                 self.page.wait_for_selector('div.captcha-control-button', timeout=10000)
#                 print("Капча не пройдена, пробуем еще раз")
#             except PwTimeout:
#                 print("Капча пройдена!")
#                 return True
#
#         print("Не удалось пройти капчу за 10 попыток")
#         return False
#
#
# def test_move_slider_fixed_90_pixels():
#     max_attempts = 10
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, args=[
#             '--disable-blink-features=AutomationControlled',
#             '--disable-web-security',
#             '--disable-features=IsolateOrigins,site-per-process',
#             '--window-size=1366,768',
#         ])
#         context = browser.new_context(
#             user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#             viewport={'width': 1366, 'height': 768}
#         )
#         page = context.new_page()
#         page.add_init_script("""
#             Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
#             Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru', 'en-US', 'en']});
#             Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
#             window.chrome = { runtime: {} };
#         """)
#
#         page.goto("https://www.vseinstrumenti.ru/", wait_until='networkidle')
#         if page_contains_forbidden(page):
#             assert False, "Тест остановлен: найден forbidden после открытия страницы"
#
#         solver = SyncCaptchaSolverAdvanced(page)
#         result = solver.solve_with_retries(max_attempts=max_attempts)
#         assert result, "Не удалось пройти капчу за 10 попыток"
#         browser.close()
#
#
# @pytest.mark.parametrize("run", range(1))
# def test_captcha_solver_gemini_with_retries(run):
#     GEMINI_API_KEY = ""
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, args=[
#             '--disable-blink-features=AutomationControlled',
#             '--disable-web-security',
#             '--disable-features=IsolateOrigins,site-per-process',
#             '--window-size=1366,768',
#         ])
#         context = browser.new_context(
#             user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#             viewport={'width': 1366, 'height': 768}
#         )
#         page = context.new_page()
#         page.add_init_script("""
#             Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
#             Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru', 'en-US', 'en']});
#             Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
#             window.chrome = { runtime: {} };
#         """)
#
#         page.goto("https://www.vseinstrumenti.ru/", wait_until='networkidle')
#         solver = SyncCaptchaSolverAdvanced(page, gemini_api_key=GEMINI_API_KEY)
#         result = solver.solve_with_retries(gemini_mode=True, max_attempts=10)
#         assert result, "Не удалось пройти капчу за 10 попыток"
#         browser.close()
