"Browsing utilities for the GPT-3 and GPT-4 models."

class GPTModels():
    gpt3 = "text-davinci-002-render-sha"
    gpt4 = "gpt-4"
    gpt4_browsing = "gpt-4-browsing"

class BASEURL():
    base = "https://chat.openai.com/"
    model = "?model="
    login = "auth/login"

class XPaths():
    login_button = '//*[@id="__next"]/div[1]/div[1]/div[4]/button[1]'
    continue_button = "//button[contains(text(), 'Continue')]"
    plus_text = '//h1/span[contains(text(), "Plus")]'
    username_id = "username"
    password_id = "password"
