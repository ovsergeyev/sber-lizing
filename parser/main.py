import asyncio

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from core.classes.pagination import Pagination
from core.db.auto_dao import AutoDAO
from core.schemas.avto_schema import AutoSchema
from core.classes.tg_bot import TgBot
from logger import get_logger, setup_logging
from settings import settings

BASE_URL = "https://www.sberleasing.ru/realizaciya-imushestva/?set_filter=y&arrFilter_434_2227190758=Y&arrFilter_434_2888745377=Y&arrFilter_434_794772980=Y"

setup_logging()
logger = get_logger("app")


def accept_cookies(driver: WebDriver):

    try:
        button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'cookie-warning__buttons')]/button")
            )
        )
        button.click()
        logger.info("Cookies приняты")
    except Exception as e:
        logger.error(f"Не удалось принять cookies: {e}")


def wait_page_loaded(driver: WebDriver, url: str, timeout=30):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    logger.info(f"Страница загружена {url}")


def save_pagination_links(driver: WebDriver, pagination: Pagination):
    link_tags = driver.find_elements(
        By.XPATH,
        "//a[contains(@class, 'sbl-pagenavigation__link') and not(contains(@class, 'sbl-pagenavigation__next'))]",
    )
    links = [
        f"{BASE_URL}&PAGEN_1={link.text}"
        for link in link_tags
        if link.text != "..." and link.text.isdigit()
    ]

    pagination.add_links(links)


def parse_card(card_tag: WebElement) -> AutoSchema:
    # проверка на Аукцион
    try:
        card_tag.find_element(
            By.XPATH,
            ".//div[contains(@class, 'realization__item-price-val') and contains(., 'Аукцион')]",
        )
        return None
    except NoSuchElementException:
        pass

    card_id = card_tag.find_element(
        By.XPATH, ".//div[@class='add-favourite']"
    ).get_attribute("data-offer-id")

    image_url = card_tag.find_element(
        By.XPATH, ".//img[contains(@class, 'tns-slide-active')]"
    ).get_attribute("src")

    title = card_tag.find_element(
        By.XPATH, ".//div[contains(@class, 'realization__item-name')]"
    ).text

    try:
        brand_tag = card_tag.find_element(
            By.XPATH,
            ".//div[contains(@class, 'realization__item-prop-name') and contains(., 'Марка')]/following-sibling::*[1]",
        )

        brand = brand_tag.get_attribute("innerText").strip()
    except NoSuchElementException:
        brand = None

    try:
        price = card_tag.find_element(
            By.XPATH,
            ".//div[contains(@class, 'realization__item-price')][1]/div[contains(@class, 'realization__item-price-val')]",
        ).text
    except NoSuchElementException:
        # Без цены пропускаем
        return None

    try:
        min_installment_element = card_tag.find_element(
            By.XPATH,
            ".//div[contains(@class, 'realization__item-price')][2]/div[contains(@class, 'realization__item-price-val')]",
        )
        min_installment = min_installment_element.text
    except NoSuchElementException:
        min_installment = None

    try:
        location = card_tag.find_element(
            By.XPATH, ".//div[contains(@class, 'realization__item-location-val')]"
        ).text.strip()
    except NoSuchElementException:
        location = ""

    try:
        year_of_release = (
            card_tag.find_element(
                By.XPATH,
                ".//div[contains(@class, 'realization__item-prop-name') and contains(., 'Год выпуска')]/following-sibling::*[1]",
            )
            .get_attribute("innerText")
            .strip()
        )
    except NoSuchElementException:
        year_of_release = None

    try:
        model_element = card_tag.find_element(
            By.XPATH,
            ".//div[contains(@class, 'realization__item-prop-name') and contains(., 'Модель')]/following-sibling::*[1]",
        )
        model = model_element.get_attribute("innerText").strip()
    except NoSuchElementException:
        model = None
        
    try:
        vin_element = card_tag.find_element(
            By.XPATH,
            ".//div[contains(@class, 'realization__item-prop-name') and contains(., 'VIN')]/following-sibling::*[1]",
        )
        vin = model_element.get_attribute("innerText").strip()
    except NoSuchElementException:
        vin = None

    try:
        mileage_element = card_tag.find_element(
            By.XPATH,
            ".//div[contains(@class, 'realization__item-prop-name') and contains(., 'Пробег, км')]/following-sibling::*[1]",
        )
        mileage = mileage_element.get_attribute("innerText").strip()
    except NoSuchElementException:
        mileage = None

    link = card_tag.find_element(
        By.XPATH, ".//a[contains(., 'Полная информация')]"
    ).get_attribute("href")

    auto = AutoSchema(
        auto_id=card_id,
        image_url=image_url,
        title=title,
        brand=brand,
        model=model,
        vin=vin,
        year_of_release=year_of_release,
        mileage=mileage,
        location=location,
        price=price,
        min_installment=min_installment,
        link=link,
    )

    return auto


async def parse_page(
    driver: WebDriver,
    url: str,
    pagination: Pagination,
    dao: AutoDAO,
    tg_bot: TgBot,
    is_accept_cookies=False,
):
    driver.get(url)
    logger.info(f"Переход на страницу {url}")

    wait_page_loaded(driver, url)
    driver.save_screenshot("screenshot.png")

    if is_accept_cookies:
        accept_cookies(driver)

    save_pagination_links(driver, pagination)

    card_tags = driver.find_elements(By.XPATH, "//div[@class='realization__item']")

    for card_tag in card_tags:
        try:
            auto: AutoSchema = parse_card(card_tag)

            if not auto:
                continue

            if dao.exists_by_auto_id(auto.auto_id):
                old_price = dao.get_price_by_auto_id(auto.auto_id)
                if old_price != auto.price:
                    auto.old_price = old_price
                    await tg_bot.send_message(auto)
                    dao.update(auto.model_dump(exclude={"link", "old_price"}))
            else:
                if settings.mode != "deployment":
                    await tg_bot.send_message(auto)
                dao.create(auto.model_dump(exclude={"link", "old_price"}))
        except Exception as e:
            logger.error(f"Ошибка при обработке элемента {e}")

        # send_message(auto)
        # dao.create_or_update(auto.dict())


async def main():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/90.0.4430.85 Safari/537.36')
    
    driver = webdriver.Chrome(service=service, options=options)
    pagination = Pagination()
    dao = AutoDAO()
    tg_bot = TgBot()

    await parse_page(driver, BASE_URL, pagination, dao, tg_bot, is_accept_cookies=True)

    while True:
        link = pagination.get_link()
        if link is None:
            break

        await parse_page(driver, link, pagination, dao, tg_bot, is_accept_cookies=False)

    # sleep(120)


if __name__ == "__main__":
    asyncio.run(main())
