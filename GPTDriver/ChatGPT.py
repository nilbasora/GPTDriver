"ChatGPT class"

# Only for testing propuses
import os
from dotenv import load_dotenv
load_dotenv()
#######################

import time

import undetected_chromedriver as uc

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException

from utilities.utils import BASEURL, XPaths, GPTModels, AuthMethods

class NewChat():
    def __init__(self, driver: uc, tab_id: int) -> None:
        self.driver = driver
        self.tab_id = tab_id

    def prompt(self, send: str) -> str:
        """Send a prompt to the chat.

        Args:
            send (str): The prompt to send.

        Returns:
            str: The response from the chat.
        """
        # Go to the driver tab
        self.driver.switch_to.window(self.tab_id)

        #TODO: Create the prompt sender and getter

class ChatGPT():
    NEW_TAB_SCRIPT = "window.open('about:blank', '_blank');"

    def __init__(self, email: str, pwd: str, auth_method: str) -> None:
        self.email = email
        self.pwd = pwd
        self.auth_method = auth_method
        self.is_closed = False
        self.model = GPTModels.gpt3
        options = uc.ChromeOptions()
        self.driver = uc.Chrome(use_subprocess=True, options=options)
        self.wait = WebDriverWait(self.driver, 30)
        self.login()
        self.__close_dialog()
        self.is_plus = self.__check_is_plus()

    def login(self) -> None:
        """Login to the OpenAI Chat website.
        """
        # Check if the instance is closed.
        if self.auth_method == AuthMethods.email:
            self.__email_login()
        elif self.auth_method == AuthMethods.google:
            self.__google_login()
        else:
            raise Exception("Invalid auth method.")

    def __email_login(self) -> None:
        """Email Login to the OpenAI Chat website.
        """
        # Check if the instance is closed.
        self.__check_is_closed()

        # Open the login page.
        self.driver.get(BASEURL.base + BASEURL.login)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, XPaths.login_button))).click()
        time.sleep(5)

        # Send the email
        self.wait.until(EC.element_to_be_clickable((By.XPATH, XPaths.continue_button)))
        self.driver.find_element(By.ID, XPaths.username_id).send_keys(self.email)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, XPaths.continue_button))).click()
        time.sleep(3)

        # Send the password
        self.wait.until(EC.element_to_be_clickable((By.XPATH, XPaths.continue_button)))
        self.driver.find_element(By.ID, XPaths.password_id).send_keys(self.pwd)
        self.driver.find_element(By.ID, XPaths.password_id).send_keys(Keys.RETURN)
        time.sleep(5)

    def __google_login(self) -> None:
        """Google Login to the OpenAI Chat website.
        """
        # Check if the instance is closed.
        self.__check_is_closed()

        # Open the login page.
        self.driver.get(BASEURL.base + BASEURL.login)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, XPaths.login_button))).click()

        # Click the Google button where data-provider="google"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-provider='google']"))).click()
        time.sleep(5)

        # Wait the button id="identifierNext" and click it
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='identifierNext']/div/button")))

        # Send the email where is an input and type="email"
        self.driver.find_element(By.CSS_SELECTOR, "input[type='email']").send_keys(self.email)

        # Click the button id="identifierNext"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='identifierNext']/div/button"))).click()
        time.sleep(5)

        # Wait the password next button and click it
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='passwordNext']/div/button")))

        # Send the password where is an input and type="password"
        self.driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(self.pwd)

        # Click the button id="passwordNext"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='passwordNext']/div/button"))).click()
        time.sleep(10)

        # Wait until the page url is the base url and its fully load
        self.wait.until(EC.url_to_be(BASEURL.base))
        time.sleep(5)

    def close(self) -> None:
        """Close the instance of ChatGPT.
        """
        self.is_closed = True
        self.driver.close()

    def set_model(self, model: str) -> None:
        """Set the model to use.

        Args:
            model (str): The model to use.

        Raises:
            Exception: If the model is invalid.
        """
        if model == GPTModels.gpt3:
            self.model = GPTModels.gpt3
        elif model == GPTModels.gpt4:
            self.__plus_needed()
            self.model = GPTModels.gpt4
        elif model == GPTModels.gpt4_browsing:
            self.__plus_needed()
            self.model = GPTModels.gpt4_browsing
        else:
            raise Exception("Invalid model.")

    def new_chat(self) -> NewChat:
        """Create a new chat tab.

        Returns:
            NewChat: The new chat tab.
        """
        self.__check_is_closed()

        self.__check_is_logged()

        # Create a new tab
        self.driver.execute_script(self.NEW_TAB_SCRIPT)

        # Switch to the new tab
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[-1])

        # Open the chat with the model
        self.driver.get(BASEURL.base + BASEURL.model + self.model)

        # Get the current tab id
        current_tab_id = self.driver.current_window_handle

        # Return the new chat
        return NewChat(self.driver, current_tab_id)

    def __check_is_plus(self) -> bool:
        """Check if the user is a plus member.

        Returns:
            bool: True if the user is a plus member, False otherwise.
        """
        if self.driver.current_url != BASEURL.base:
            self.driver.get(BASEURL.base)

        # Wait unitl page is fully load
        self.wait.until(EC.url_to_be(BASEURL.base))

        # Check if the plus text is present
        try:
            self.is_plus = self.driver.find_element(By.ID, XPaths.plus_text)
            self.is_plus = True
        except InvalidSelectorException:
            self.is_plus = False

        return self.is_plus

    def __plus_needed(self) -> None:
        """Some functionality requires a plus membership.

        Raises:
            Exception: If the user is not a plus member.
        """
        if not self.is_plus:
            raise Exception("You must be a plus member to use this functionality.")

    def __check_is_closed(self) -> None:
        """Check if the instance is closed.

        Raises:
            Exception: If the instance is closed.
        """
        if self.is_closed:
            raise Exception('This instance of ChatGPT is closed.')

    def __check_is_logged(self):
        if self.driver.current_url.startswith(BASEURL.base + BASEURL.login):
            self.login()


if __name__ == "__main__":
    chat = ChatGPT(os.getenv("EMAIL"), os.getenv("PASSWORD"))
    chat.close()
