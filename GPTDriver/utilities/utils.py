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

    send_icon = "//*[local-name()='svg']/*[local-name()='path' and @d='M.5 1.163A1 1 0 0 1 1.97.28l12.868 6.837a1 1 0 0 1 0 1.766L1.969 15.72A1 1 0 0 1 .5 14.836V10.33a1 1 0 0 1 .816-.983L8.5 8 1.316 6.653A1 1 0 0 1 .5 5.67V1.163Z']"

class AuthMethods():
    email = "email"
    google = "google"
