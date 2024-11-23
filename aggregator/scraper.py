from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PAGE_LOAD_TIMEOUT = 8
COOKIE_TIMEOUT = 2
JS_TIMEOUT = 1.5


def automate_links(feed_list, headless=False):
    """
    feed_list is a dictionary which contains one field named `url`
    That is the website to scrape
    """
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    try:
        for article in feed_list:
            url = article.get('url')
            if url is None:
                print(f"ERROR: No url for {article['title']}")
                continue

            print(f"Opening {url}")
            driver.get(url)

            WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # try:
            #     # List of possible keywords for cookie acceptance
            #     accept_keywords = [
            #         "Accept", "I agree", "Consent",  # English
            #         "Akzeptieren", "Einwilligen", "Zustimmen", "Erlauben"  # German
            #     ]

            #     cookie_elements = [
            #         (By.XPATH, f"//*[contains(text(), '{keyword}')]") for keyword in accept_keywords
            #     ]

            #     for cookie_button in cookie_elements:
            #         try:
            #             button = WebDriverWait(driver, COOKIE_TIMEOUT).until(
            #                 EC.element_to_be_clickable(cookie_button)
            #             )
            #             print(
            #                 f"\tFound and clicked cookie button: {button.text}")
            #             ActionChains(driver).move_to_element(
            #                 button).click().perform()
            #             break
            #         except:
            #             pass

            # except Exception as e:
            #     print(f"\tNo cookie popup found on {url}. Proceeding...", e)

            # Wait briefly to ensure any JavaScript changes are applied
            time.sleep(JS_TIMEOUT)

            # Get the HTML of the page
            article["html"] = driver.page_source
            print(f"\tRetrieved HTML for {url}")

    finally:
        driver.quit()

    return feed_list
