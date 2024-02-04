import allure
from config.links_of_pages import local
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType

MCPAY_BUTTON = ('xpath', "//div[@class ='pt-auth-header__logo']")

GOOGLE_STORE_BUTTON = ('xpath', "//img[@alt = 'GooglePlay']")
APPSTORE_BUTTON = ('xpath', "//img[@alt = 'AppStore']")

LANGUAGE_SELECT = ('xpath', '//div[@tabindex="0"]//span[@class="mc-button__append"]')
LANGUAGE_DROPDOWN = ('xpath', "//section[@class = 'mc-dropdown-panel']")

RESET_PASSWORD_FIELD = ('xpath', '//main[@class="reset-page"]')

EMAIL_FIELD = ('xpath', '//input[@id = "email"]')
ERROR_EMAIL_FIELD = ('xpath',
                     '//label[@for = "email"]/following-sibling::div[@class ="mc-field-text__footer"]//div[@ class="mc-title__text"]')

SUBMIT_BUTTON_FROM_RECOVER_PAGE = (
'xpath', '(//div[@class="mc-grid-row mc-grid-row--justify-between mc-grid-row--align-middle"]//button)[1]')
REMEMBER_PASSWORD_BUTTON = (
'xpath', '(//div[@class="mc-grid-row mc-grid-row--justify-between mc-grid-row--align-middle"]//button)[2]')

SUCCESSFUL_AREA = ('xpath', '//main[@class = "reset-page"]')
WHICH_EMAIL_GET_LETTER = ('xpath', '//b')
SUPPORT_EMAIL = ('xpath', '//div[contains(@class, "reset-page__info")]//a')


class ResetPasswordPage(BasePage):
    page_url = f'{local}/auth/reset'

    def successful_sent_email(self, email):
        self.wait.until(EC.invisibility_of_element(EMAIL_FIELD))
        with allure.step('Сверка email в тексте страницы успеха с email, на который было отправлено письмо'):
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.successful_sent_email.__name__}_screenshot",
                          attachment_type=AttachmentType.PNG)
            email_in_success_text = self.find(WHICH_EMAIL_GET_LETTER).text
            assert email == email_in_success_text, 'Letter was not sent'
