"""Converts runescape accounts to Jagex accounts via selenium."""
import re
import sys
import time

# from selenium import webdriver
import undetected_chromedriver as uc

from multiprocessing.pool import ThreadPool

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from loguru import logger


def get_driver():
    """Returns chrome driver."""
    options = uc.ChromeOptions()
    options.headless = False
    driver = uc.Chrome(options=options, version_main=116)
    return driver


def accept_cookies(driver) -> bool:
    """Clicks the 'Use necessary cookies only' button on the cookies pop-up."""
    logger.debug("Looking for 'Use necessary cookies only' button to click.")
    try:
        # Use the id attribute to find the button
        cookies_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyButtonDecline"))
        )
        # Click the button to accept necessary cookies
        logger.debug("Clicking 'Use necessary cookies only' button.")
        cookies_button.click()
    except Exception as e:
        logger.error(f"An error occurred while trying to accept cookies: {e}")
        return False
    else:
        logger.debug("Successfully clicked 'Use necessary cookies only' button.")
        return True


def navigate_to_login_page(driver) -> bool:
    """Clicks the 'account' header button on the home page to get to the login page."""
    logger.debug("Looking for 'account' button to click.")
    try:
        # Use the data-test attribute to find the button
        account_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-test="header-sub-account"]'))
        )
        # Click "account" button
        logger.debug("Clicking 'account' button.")
        account_button.click()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return False
    else:
        logger.debug("Successfully clicked 'account' button.")
        return True


def enter_username(driver, email) -> bool:
    """Enters the username into the login form."""
    logger.debug("Looking for username input field element to enter username.")
    try:
        # Wait up to 10 seconds for the element to become available
        username_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        # Enter the email into the element
        logger.debug("Entering username into username input field.")
        driver.switch_to.active_element.send_keys(email)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return False
    else:
        logger.debug("Successfully entered username into username input field.")
        return True


def click_submit_button(driver) -> bool:
    """Clicks the submit button to continue after entering username."""
    logger.debug("Looking for submit button to click.")
    try:
        # Wait for the submit button to become clickable and then click it
        submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="continue-with-assisted-via-email-flow"]'))
        )
        logger.debug("Clicking submit button.")
        submit_button.click()
    except Exception as e:
        logger.error(f"An error occurred while trying to click the submit button: {e}")
        return False
    else:
        logger.debug("Successfully clicked the submit button.")
        return True


def enter_password(driver, password) -> bool:
    """Enters the password into the currently active password field."""
    logger.debug("Entering password into the active password field.")
    try:
        # Send password to the currently active input box
        driver.switch_to.active_element.send_keys(password)
    except Exception as e:
        logger.error(f"An error occurred while trying to enter the password: {e}")
        return False
    else:
        logger.debug("Successfully entered the password into the password field.")
        return True


def click_login_button(driver) -> bool:
    """Clicks the login button to continue after entering password."""
    logger.debug("Looking for login button to click.")
    try:
        # Wait for the login button to become clickable and then click it
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="login"]'))
        )
        logger.debug("Clicking login button.")
        login_button.click()
    except Exception as e:
        logger.error(f"An error occurred while trying to click the login button: {e}")
        return False
    else:
        logger.debug("Successfully clicked the login button.")
        return True


def click_upgrade_image(driver) -> bool:
    """Clicks the upgrade image to proceed."""
    logger.debug("Looking for upgrade image to click.")
    try:
        # Wait for the image to become clickable and then click it
        upgrade_image = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'img[alt="Jagex Accounts - Enhance your security. Upgrade."]'))
        )
        logger.debug("Clicking upgrade image.")
        upgrade_image.click()
    except Exception as e:
        logger.error(f"An error occurred while trying to click the upgrade image: {e}")
        return False
    else:
        logger.debug("Successfully clicked the upgrade image.")
        return True


def click_start_button(driver) -> bool:
    """Clicks the 'Start' button to proceed."""
    logger.debug("Looking for 'Start' button to click.")
    try:
        # Wait for the 'Start' button to become clickable and then click it
        start_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="account-migration--button-start"]'))
        )
        logger.debug("Clicking 'Start' button.")
        start_button.click()
    except Exception as e:
        logger.error(f"An error occurred while trying to click the 'Start' button: {e}")
        return False
    else:
        logger.debug("Successfully clicked the 'Start' button.")
        return True


def input_email(driver, email) -> bool:
    logger.debug(f"Entering email address ({email}) into the email input field.")
    time.sleep(5)
    active_el = driver.switch_to.active_element
    logger.debug(f"Active element: {active_el.get_attribute('outerHTML')}")
    try:
        email_field = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div/div/form/div[1]/label/input')))
        email_field.send_keys(email)
    except Exception as e:
        logger.error(f"An error occurred while trying to enter the email: {e}")
        return False
    else:
        logger.debug("Successfully entered the email address.")
        return True


def input_dob(driver, day, month, year) -> bool:
    logger.debug("Entering date of birth into the respective fields.")
    try:
        day_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div/form/div[4]/div[1]/div/label/input"))
        )
        day_field.send_keys(day)

        month_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div/form/div[4]/div[2]/div/label/input"))
        )
        month_field.send_keys(month)

        year_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div/form/div[4]/div[3]/div/label/input"))
        )
        year_field.send_keys(year)
    except Exception as e:
        logger.error(f"An error occurred while trying to enter the date of birth: {e}")
        return False
    else:
        logger.debug("Successfully entered the date of birth.")
        return True


def click_agree_checkbox(driver) -> bool:
    logger.debug("Looking for 'I agree' checkbox to click.")
    try:
        agree_checkbox = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[data-testid="registration-start-accept-agreements"]'))
        )
        agree_checkbox.click()
    except Exception as e:
        logger.error(f"An error occurred while trying to click the 'I agree' checkbox: {e}")
        return False
    else:
        logger.debug("Successfully clicked the 'I agree' checkbox.")
        return True


def access_email_on_website(driver, email_address) -> bool:
    # Open a new tab
    driver.execute_script("window.open('', '_blank');")
    
    # Switch to the new tab (the new tab becomes the last window handle)
    driver.switch_to.window(driver.window_handles[-1])

    # Navigate directly to the email's inbox using the provided email address
    inbox_url = f"https://tuamaeaquelaursa.com/{email_address}"
    driver.get(inbox_url)

    try:
        # Just as a sample check: Wait for a message div to be present (indicating the inbox loaded)
        # Adjust the selector as needed if you want to check for a different element
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-v-bbba6544].the-message-subject'))
        )
    except Exception as e:
        logger.error(f"Error opening email website in new tab: {e}")
        return False
    else:
        logger.debug(f"Successfully accessed the inbox for email: {email_address} in the new tab.")
        return True


def get_verification_code(driver) -> str:
    """Extract the verification code from the most recent email message on the website."""
    try:
        # Wait for the message divs to be present and get all of them
        message_divs = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-v-bbba6544].the-message-subject'))
        )

        if not message_divs:
            logger.warning("No email messages found on the page.")
            return ""

        # Using first div to get the most recent email
        message_text = message_divs[0].text

        # Extract the code from the message text using regex
        match = re.search(r'([A-Z0-9]+) is your Jagex verification code', message_text)
        if match:
            verification_code = match.group(1)
            logger.debug(f"Extracted verification code: {verification_code}")
            return verification_code
        else:
            logger.warning("Couldn't extract the verification code from the most recent message.")
            return ""
    except Exception as e:
        logger.error(f"An error occurred while trying to extract the verification code: {e}")
        return ""


def click_continue_button(driver) -> bool:
    """Clicks the 'Continue' button."""
    try:
        # Wait for the "Continue" button to be clickable and then click it
        continue_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="BoxFlowqi"]'))
        )
        continue_button.click()
    except Exception as e:
        logger.error(f"An error occurred while trying to click the 'Continue' button: {e}")
        return False
    else:
        logger.debug("Successfully clicked the 'Continue' button.")
        return True


def input_verification_code(driver, code) -> bool:
    """Inputs the extracted code and clicks the 'Continue' button."""
    try:
        # Switch back to the original tab
        driver.switch_to.window(driver.window_handles[0])

        # Input the code into the active field
        active_field = driver.switch_to.active_element
        active_field.send_keys(code)
    except Exception as e:
        logger.error(f"An error occurred while inputting the verification code: {e}")
        return False
    else:
        logger.debug("Successfully input verification code and clicked the 'Continue' button.")
        return True


def enter_jagex_name(driver, email_address) -> bool:
    """Inputs the email into the currently active field and clicks the 'Continue' button."""
    # Sometimes field seems to not be ready
    time.sleep(5)
    try:
        # Input the email address into the active field
        active_field = driver.switch_to.active_element
        active_field.send_keys(email_address)
    except Exception as e:
        logger.error(f"An error occurred while inputting the jagex username: {e}")
        return False
    else:
        logger.debug("Successfully input jagex username.")
        return True


def input_password_and_create_account(driver, password) -> bool:
    """Inputs the password into the two fields and clicks the 'Create account' button."""
    # Sometimes field seems to not be ready
    time.sleep(5)
    try:
        # Input the password into the first field using its full XPath
        password_field_1 = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/form/div[1]/label/input'))
        )
        password_field_1.send_keys(password)

        # Input the password into the second field using its full XPath
        password_field_2 = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/form/div[3]/label/input'))
        )
        password_field_2.send_keys(password)

        # Wait for the "Create account" button to be clickable and then click it
        create_account_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="BoxFlowqi"]'))
        )
        create_account_button.click()
    except Exception as e:
        logger.error(f"An error occurred while inputting the password and clicking 'Create account': {e}")
        return False
    else:
        logger.info("Successfully input password and clicked the 'Create account' button.")
        return True


def check_invalid_password(driver) -> bool:
    """Checks if we got an invalid password error."""
    try:
        # Wait for the error message to appear with the specific text
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//p[contains(., "Your login or password was incorrect")]'))
        )
    except Exception as e:
        logger.error(f"An error occurred while checking for the invalid password error: {e}")
        return False
    else:
        logger.warning("Received invalid password error. Skipping account.")
        return True


def check_for_authenticator(driver) -> bool:
    """Checks if we hit the authenticator page."""
    try:
        # Wait for the authenticator page to load
        authenticator_page = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="l-vista__container"]/h1'))
        )
    except Exception as e:
        logger.error(f"An error occurred while checking for the authenticator page: {e}")
        return False
    else:
        logger.warning("Hit the authenticator page. Skipping account.")
        return True


def convert_to_jagex_account(
        driver,
        runescape_email, runescape_password,
        jagex_username, jagex_password, jagex_email,
        base_username
        ) -> bool:
    """Wrapper function to convert a runescape account to a jagex account."""
    HOME_URL = "https://www.runescape.com/community"

    # Load the home page
    driver.get(HOME_URL) 

    # Accept cookies
    accept_cookies(driver)

    # Navigate to login page
    navigate_to_login_page(driver)

    # Accept cookies again
    accept_cookies(driver)

    # Attempt to enter the username
    enter_username(driver, runescape_email)

    # Click the submit button
    click_submit_button(driver)

    # Accept cookies again
    accept_cookies(driver)

    # Enter password
    enter_password(driver, runescape_password)

    # Click login button
    click_login_button(driver)

    # Check for invalid password
    if check_invalid_password(driver):
        return False

    # Check for authenticator page
    if check_for_authenticator(driver):
        return False

    # Click upgrade image
    click_upgrade_image(driver)

    # Click cookies again
    accept_cookies(driver)

    # Click start button
    click_start_button(driver)

    # Input email
    input_email(driver, jagex_email)

    # Input date of birth
    input_dob(driver, "02", "02", "1994")

    # Click agree checkbox
    click_agree_checkbox(driver)

    # Click continue button
    click_continue_button(driver)

    # Access email on website
    access_email_on_website(driver, base_username)

    # wait a bit to get the email
    time.sleep(5)

    # Get verification code
    code = get_verification_code(driver)
    logger.debug(f"Verification code: {code}")

    if code:
        # Input code and continue
        input_verification_code(driver, code)
        click_continue_button(driver)

        # Enter jagex name
        enter_jagex_name(driver, jagex_username)
        click_continue_button(driver)

        # Input password and click "create account"
        input_password_and_create_account(driver, jagex_password)

        logger.success("Successfully created account with info:")
        logger.info(f"Runescape username: {runescape_email}")
        logger.info(f"Runescape password: {runescape_password}")
        logger.info(f"Jagex username: {jagex_username}")
        logger.info(f"Jagex password: {jagex_password}")
        logger.info(f"Jagex email: {jagex_email}")

        # New line for cleaner output
        print("\n")

        return True


def process_account(account, jagex_password):
    """Process an account."""
    USERNAME, PASSWORD = account.split(":")
    BASE_USERNAME = USERNAME.split("@")[0]
    JAGEX_ACCOUNT_EMAIL = BASE_USERNAME + "@tuamaeaquelaursa.com"
    JAGEX_ACCOUNT_USERNAME = BASE_USERNAME if BASE_USERNAME.isalpha() else re.sub(r"[^a-z]", "", BASE_USERNAME)  # Username to use for the jagex account. Taken usernames aren't error handled.

    # Get the driver
    driver = get_driver()

    try:
        convert_to_jagex_account(
            driver=driver,
            runescape_email=USERNAME, runescape_password=PASSWORD,
            jagex_username=JAGEX_ACCOUNT_USERNAME, jagex_password=jagex_password, jagex_email=JAGEX_ACCOUNT_EMAIL,
            base_username=BASE_USERNAME
        )
    except Exception as e:
        logger.error(f"An error occurred while processing account: {e}")
    finally:
        # Close driver for next account
        driver.close()


def error_callback(task_name, e):
    logger.error(f'{task_name} completed with exception {e}')


def main():
    DEBUG = False
    MAX_CONCURRENT_SESSIONS = 2

    ACCOUNT_LIST = [
        "account1@gmail.com:password1",
        "account2@gmail.com:password2",
    ]

    JAGEX_ACCOUNT_PASSWORD = "Secure!0123"  # Password to use for the jagex account. Jagex password must not be considered "weak"

    if DEBUG:
        logger.add("logs_{time}.log", level="DEBUG")
    else:
        logger.add("logs_{time}.log", level="INFO")

    pool_size = min(MAX_CONCURRENT_SESSIONS, len(ACCOUNT_LIST))

    with ThreadPool(pool_size) as pool:
        for account in ACCOUNT_LIST:
            pool.apply_async(process_account, args=(account, JAGEX_ACCOUNT_PASSWORD), error_callback=lambda e: error_callback(account, e))
            time.sleep(5)   # Chrome driver access error otherwise.
        pool.close()
        pool.join()

    logger.info("Finished converting accounts.")
    sys.exit(0)


if __name__ == "__main__":
    main()
