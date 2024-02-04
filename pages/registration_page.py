import allure
from allure_commons.types import AttachmentType
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC

from config.links_of_pages import local, Links
from error_messages import error_text_ru, error_text_th, error_text_vi, error_text_en, error_text_pt, error_text_es
from pages.base_page import BasePage
from pages.home_page import WELCOME_MODAL

GOOGLE_BUTTON = ('xpath', '//span[contains(text(),"Google")]')
FACEBOOK_BUTTON = ('xpath', '//span[contains(text(),"Facebook")]')
APPLE_BUTTON = ('xpath', '//span[contains(text(),"Apple")]')

MCPAY_BUTTON = ('xpath', "//div[@class ='pt-auth-header__logo']")

SIGN_UP_AREA_REGISTRATION_PAGE = ('xpath', '//div[@class="sign-up-page"]')

GOOGLE_STORE_BUTTON = ('xpath', "//img[@alt = 'GooglePlay']")
APPSTORE_BUTTON = ('xpath', "//img[@alt = 'AppStore']")

LANGUAGE_SELECT = ('xpath', '//div[@tabindex="0"]//span[@class="mc-button__append"]')
LANGUAGE_DROPDOWN = ('xpath', "//section[@class = 'mc-dropdown-panel']")
CHECK_ATTRIBUTE_LANGUAGE_DROPDOWN = ('xpath', '//div[contains(@class," tm-wg-locales-dropdown")]')

NAME_FIELD = ('xpath', '//input[@id="first_name"]')
LAST_NAME_FIELD = ('xpath', '//input[@id="last_name"]')
EMAIL_FIELD = ('xpath', '//input[@id = "email"]')

COUNTRY_SELECT = ('xpath', '//div[@aria-owns="listbox-country"]')
COUNTRY_SELECT_CLOSED = ('xpath', "//span[@class = 'multiselect__single']")
CHOSEN_COUNTRY_AREA = ('xpath', '//div[@class="mc-field-select__label-text"]')
COUNTRIES = ('xpath', "//ul[@id = 'listbox-country']/li")

PHONE_FIELD = ('xpath', '//input[@id ="phone"]')

PASSWORD_FIELD = ('xpath', '//input[@id = "password"]')
SHOW_PASSWORD_BUTTON = ('xpath', '//button[@tabindex ="-1"]')
TOOLTIP_BY_PASSWORD = ('xpath', '//div[@class = "tooltip-inner__content"]')
CHECK_VISIBILITY_OF_TOOLTIP = ('xpath', '//div[contains(@class, "mc-tooltip-target has-tooltip")]')

CHECKBOX_PRIVACY = ('css selector', 'label[class = "mc-field-checkbox__name"] svg')
CHECKBOX_PRIVACY_STATUS = ('xpath', '//input[@type = "checkbox"]')

PRIVACY_POLICY_REGISTRATION_PAGE = ('xpath', "//a[contains(@href, '/api/privacy')]")
TERMS_OF_SERVISE_REGISTRATION_PAGE = ('xpath', "//a[contains(@href, '/api/agreement')]")

SIGN_IN_BUTTON = ('xpath', '//button[@tabindex = "9"]')
LOGIN_FROM_SIGNIN_PAGE = ('xpath',
                          '//button[@tabindex = "9"]/ancestor::div[@class = "mc-grid-row mc-grid-row--justify-between mc-grid-row--align-middle"]//button[not(@tabindex = "9")]')

ERROR_BLOCK = ('xpath', '//div[@class="mc-field-text__footer"]')

ERROR_EMAIL_FIELD = ('xpath',
                     '//label[@for = "email"]/following-sibling::div[@class ="mc-field-text__footer"]//div[@ class="mc-title__text"]')
ERROR_PASSWORD_FIELD = ('xpath',
                        '//label[@for = "password"]/following-sibling::div[@class ="mc-field-text__footer"]//div[@ class="mc-title__text"]')
ERROR_FIRST_NAME_FIELD = ('xpath',
                          '//label[@for = "first_name"]/following-sibling::div[@class ="mc-field-text__footer"]//div[@ class="mc-title__text"]')
ERROR_LAST_NAME_FIELD = ('xpath',
                         '//label[@for = "last_name"]/following-sibling::div[@class ="mc-field-text__footer"]//div[@ class="mc-title__text"]')
ERROR_PHONE_FIELD = ('xpath',
                     '//label[@for = "phone"]/following-sibling::div[@class ="mc-field-text__footer"]//div[@ class="mc-title__text"]')

ERROR_CHECKBOX_FIELD = ('xpath', '//div[@class ="mc-field-checkbox__footer"]//div[@ class="mc-title__text"]')


class RegistrationPage(BasePage):
    page_url = f'{local}/auth/sign-up'

    def clean_and_fill_phone_field(self, locator, phone_data):
        with allure.step('Выделяем весь контент в поле ввода номера телефона'):
            self.find(locator).send_keys(Keys.CONTROL + 'a')
        with allure.step('Очищаем поле ввода номера телефона'):
            self.find(locator).send_keys(Keys.BACKSPACE)
        with allure.step('Ввод данных в поле номера телефона'):
            self.find(locator).send_keys(phone_data)
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.clean_and_fill_phone_field.__name__}_phone_number field is filled",
                          attachment_type=AttachmentType.PNG)
        with allure.step('Сохранение в переменную данных из поля номера телефона'):
            entered_number = self.find(locator).get_attribute('value')
        number = ''.join(c for c in entered_number if c.isdigit())
        with allure.step('Проверка, что введенный номер совпадает с номером, отображающимся в поле'):
            assert phone_data == number, 'numbers did not match'

    def check_validation_error_text_field(self):
        self.wait.until(EC.visibility_of_all_elements_located(ERROR_BLOCK))

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

        with allure.step('Проверка корректности ошибки под полем на выбранной локали'):
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.check_validation_error_text_field.__name__}_error texts are shown under particular field",
                          attachment_type=AttachmentType.PNG)
            assert text.invalid_first_and_last_name in self.find(
                ERROR_FIRST_NAME_FIELD).text, 'error text did not match'
            assert text.invalid_first_and_last_name in self.find(ERROR_LAST_NAME_FIELD).text, 'error text did not match'
            assert text.invalid_email in self.find(ERROR_EMAIL_FIELD).text, 'error text did not match'
            assert text.invalid_phone in self.find(ERROR_PHONE_FIELD).text, 'error text did not match'

    def check_validation_error_checkbox(self):
        self.wait.until(EC.visibility_of_element_located(ERROR_CHECKBOX_FIELD))
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
        with allure.step('Проверка корректности ошибки под полем на выбранной локали'):
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.check_validation_error_checkbox.__name__}_checkbox was not selected",
                          attachment_type=AttachmentType.PNG)
            assert self.find(ERROR_CHECKBOX_FIELD).text == text.checkbox_did_not_selected, 'error text did not match'

    def check_error_email_already_exists(self):
        self.wait.until(EC.visibility_of_all_elements_located(ERROR_BLOCK))

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
        with allure.step('Проверка корректности ошибки под полем на выбранной локали'):
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.check_error_email_already_exists.__name__}_email has already existed",
                          attachment_type=AttachmentType.PNG)
            assert self.find(ERROR_EMAIL_FIELD).text == text.email_already_exists, 'error text did not match'

    def click_checkbox(self, checkbox_locator, checkbox_status):
        self.find_and_click_element(checkbox_locator)
        allure.attach(self.driver.get_screenshot_as_png(),
                      name=f"{self.click_checkbox.__name__}_checkbox is selected",
                      attachment_type=AttachmentType.PNG)
        with allure.step(f'Получение статуса поля {checkbox_status}'):
            status = self.find(checkbox_status)
        with allure.step('Проверка, что элемент выбран'):
            self.wait.until(EC.element_to_be_selected(status))

    def change_country(self, country):
        self.wait.until(EC.presence_of_element_located(COUNTRY_SELECT_CLOSED))
        self.find_and_click_element(COUNTRY_SELECT)
        with allure.step('Проверка, что в DOM изменился статус мультиселекта страны'):
            self.wait.until(EC.none_of(EC.presence_of_element_located(COUNTRY_SELECT_CLOSED)))
        with allure.step('Проверка, что в DOM изменился статус мультиселекта страны и дропдаун открыт'):
            self.wait.until(EC.text_to_be_present_in_element_attribute(COUNTRY_SELECT, 'class', 'multiselect--active'))
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.change_country.__name__}_country dropdown is opened",
                          attachment_type=AttachmentType.PNG)
        self.find(COUNTRY_SELECT).send_keys(Keys.ARROW_DOWN)
        self.find(COUNTRY_SELECT).send_keys(country, Keys.ENTER)
        with allure.step('Проверка, что в поле "страна" отображается выбранное значение'):
            self.wait.until(EC.text_to_be_present_in_element(CHOSEN_COUNTRY_AREA, country))
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.change_country.__name__}_chosen country is presented in a field",
                          attachment_type=AttachmentType.PNG)

    def check_welcome_modal_home_page(self):
        self.wait.until(EC.url_to_be(Links.home_url))
        with allure.step('Дожидаемся появления welcome modal'):
            self.wait.until(EC.visibility_of_element_located(WELCOME_MODAL))
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.check_welcome_modal_home_page.__name__}_screenshot",
                          attachment_type=AttachmentType.PNG)
