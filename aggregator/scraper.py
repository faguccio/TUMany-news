from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PAGE_LOAD_TIMEOUT = 8
COOKIE_TIMEOUT = 1.5
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

            # Wait a few second for the cookie banner to appear
            time.sleep(COOKIE_TIMEOUT)

            try:
                # List of possible keywords for cookie acceptance
                accept_keywords = [
                    "Accept", "Consent", "Allow", "Agree", "Proceed", "Continue", "Confirm", "Enable", "Grant", "Got It", "Understood",  # English
                    "Akzeptieren", "Einwilligen", "Zustimmen", "Erlauben"  # German
                ]

                for keyword in accept_keywords:
                    # Find all elements containing the keyword (case-insensitive)
                    cookie_buttons = driver.find_elements(
                        By.XPATH, f"//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{keyword.lower()}')]")

                    if cookie_buttons:
                        print(
                            f"\tFound {len(cookie_buttons)} cookie element(s) for keyword: '{keyword}'")
                        for button in cookie_buttons:
                            try:
                                print(f"\t\tClicking button: {button.text}")
                                ActionChains(driver).move_to_element(
                                    button).click().perform()
                            except Exception as e:
                                print(f"\t\tCould not click button")

            except Exception as e:
                print(f"\tNo cookie popup found on {url}. Proceeding...", e)

            # Wait briefly to ensure any JavaScript changes are applied
            time.sleep(JS_TIMEOUT)

            # Get the HTML of the page
            article["html"] = driver.page_source
            print(f"\tRetrieved HTML for {url}")

    finally:
        driver.quit()

    return feed_list
