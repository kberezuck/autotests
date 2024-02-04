
import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from allure_commons.types import AttachmentType
from pages.base_page import BasePage
from config.links_of_pages import local, Links
from error_messages import error_text_ru, error_text_th, error_text_vi, error_text_en, error_text_pt, error_text_es

LOGIN_BUTTON_AUTORISATION_PAGE = ('xpath', '//button[@tabindex = "3"]')
SIGN_IN_BUTTON_AUTORISATION_PAGE = ('xpath',
                                    '//button[@tabindex = "3"]/ancestor::div[@class = "mc-grid-row mc-grid-row--justify-between mc-grid-row--align-middle"]//button[not(@tabindex = "3")]')
FORGOT_PASSWORD_BUTTON = ('xpath', '//div[contains(@class,"sign-in-page__forgot_password")]/button')

LOADER = ('xpath', "//span[@class = 'mc-button__loader']")
SIGN_IN_AREA_AUTHORISATION_PAGE = ('xpath', '//div[@class="sign-in-page"]')

PRIVACY_POLICY_AUTORISARION_PAGE = ('xpath', "//a[contains(@href, '/api/privacy')]")

EMAIL_FIELD = ('xpath', '//input[@id = "email"]')
PASSWORD_FIELD = ('xpath', '//input[@id = "password"]')

SHOW_PASSWORD_BUTTON = ('xpath', '//button[@tabindex ="-1"]')
TOOLTIP_BY_PASSWORD = ('xpath', '//div[@class = "tooltip-inner__content"]')
CHECK_VISIBILITY_OF_TOOLTIP = ('xpath', '//div[contains(@class, "mc-tooltip-target has-tooltip")]')

GOOGLE_BUTTON = ('xpath', '//span[contains(text(),"Google")]')
FACEBOOK_BUTTON = ('xpath', '//span[contains(text(),"Facebook")]')
APPLE_BUTTON = ('xpath', '//span[contains(text(),"Apple")]')

MCPAY_BUTTON = ('xpath', "//div[@class ='pt-auth-header__logo']")

GOOGLE_STORE_BUTTON = ('xpath', "//img[@alt = 'GooglePlay']")
APPSTORE_BUTTON = ('xpath', "//img[@alt = 'AppStore']")

LANGUAGE_SELECT = ('xpath', '//div[@tabindex="0"]//span[@class="mc-button__append"]')
LANGUAGE_DROPDOWN = ('xpath', "//section[@class = 'mc-dropdown-panel']")
CHECK_ATTRIBUTE_LANGUAGE_DROPDOWN = ('xpath', '//div[contains(@class," tm-wg-locales-dropdown")]')

ERROR_EMAIL_FIELD = ('xpath',
                     '//label[@for = "email"]/following-sibling::div[@class ="mc-field-text__footer"]//div[@ class="mc-title__text"]')
ERROR_PASSWORD_FIELD = ('xpath',
                        '//label[@for = "password"]/following-sibling::div[@class ="mc-field-text__footer"]//div[@ class="mc-title__text"]')

ERROR_BLOCK = ('xpath', '//div[@class="mc-field-text__footer"]')


class AuthorisationPage(BasePage):
    page_url = f'{local}/auth/sign-in'

    def __init__(self, driver, actions):
        super().__init__(driver, actions)
        self.wait = WebDriverWait(self.driver, 15, poll_frequency=1)



    def check_no_exist_on_DB_email_error(self):
        self.wait.until(EC.visibility_of_all_elements_located(ERROR_EMAIL_FIELD))

        current_url = self.get_current_url()
        if '/ru' in current_url:
            text = error_text_ru
        elif '/es' in current_url:
            text = error_text_es
        elif '/pt' in current_url:
            text = error_text_pt
        elif '/th' in current_url:
            text = error_text_th
        elif '/vi' in current_url:
            text = error_text_vi
        else:
            text = error_text_en

        with allure.step('Проверка корректности ошибки под полем email на выбранной локали'):
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.check_no_exist_on_DB_email_error.__name__}_email does not exist in DB",
                          attachment_type=AttachmentType.PNG)
            assert self.find(
                ERROR_EMAIL_FIELD).text == text.email_does_not_exist_in_db, 'error text did not match'

    def check_redirect_to_2fa_after_login(self):
        with allure.step(('Наблюдаем за лоадером')):
            self.wait.until(EC.visibility_of_element_located(LOADER))
            self.wait.until(EC.invisibility_of_element(LOADER))
        with allure.step('Проверка, что произошел редирект на ввод кода 2fa'):
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.check_redirect_to_2fa_after_login.__name__}_2fa page is shown",
                          attachment_type=AttachmentType.PNG)
            current_page = self.get_current_url()
            assert current_page == Links.twofa_url, 'Redirect to 2fa does not happened'

    def check_redirect_to_home_account(self):
        self.wait.until(EC.invisibility_of_element(LOADER))
        with allure.step('Проверка, что произошел редирект на аккаунт юзера'):
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.check_redirect_to_home_account.__name__}_home_page is shown",
                          attachment_type=AttachmentType.PNG)
            current_page = self.get_current_url()
            assert current_page == Links.home_url, 'Redirect to home page does not happened'
