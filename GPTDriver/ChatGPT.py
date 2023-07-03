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

from utilities.utils import BASEURL, XPaths, GPTModels

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

    def __init__(self, email: str, pwd: str) -> None:
        self.email = email
        self.pwd = pwd
        self.is_closed = False
        self.model = GPTModels.gpt3
        options = uc.ChromeOptions()
        self.driver = uc.Chrome(use_subprocess=True, options=options)
        self.login()
        self.is_plus = self.__check_is_plus()

    def login(self) -> None:
        """Login to the OpenAI Chat website.
        """
        # Check if the instance is closed.
        self.__check_is_closed()

        # Open the login page.
        self.driver.get(BASEURL.base + BASEURL.login)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, XPaths.login_button))).click()
        time.sleep(5)

        # Send the email
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, XPaths.continue_button)))
        self.driver.find_element(By.ID, XPaths.username_id).send_keys(self.email)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, XPaths.continue_button))).click()
        time.sleep(3)

        # Send the password
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, XPaths.continue_button)))
        self.driver.find_element(By.ID, XPaths.password_id).send_keys(self.pwd)
        self.driver.find_element(By.ID, XPaths.password_id).send_keys(Keys.RETURN)
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

        WebDriverWait(self.driver, 10)
        self.is_plus = self.driver.find_element(By.ID, XPaths.plus_text)
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
