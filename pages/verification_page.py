import time

import allure

from config.links_of_pages import local
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from error_messages import error_text_vi, error_text_th, error_text_pt, error_text_es, error_text_en, error_text_ru

MCPAY_BUTTON = ('xpath', "//div[@class ='pt-auth-header__logo']")

GOOGLE_STORE_BUTTON = ('xpath', "//img[@alt = 'GooglePlay']")
APPSTORE_BUTTON = ('xpath', "//img[@alt = 'AppStore']")

LANGUAGE_SELECT = ('xpath', '//div[@tabindex="0"]//span[@class="mc-button__append"]')
LANGUAGE_DROPDOWN = ('xpath', "//section[@class = 'mc-dropdown-panel']")

BACK_BUTTON = ('xpath', '//button[contains(@class, "mc-button--variation-black-flat")]')
VERIFICATION_FIELD = ('xpath', '//div[@class="el-input-separated__main"]')
INPUT_FIELD = ('xpath', '//input[contains(@name, "input")]')
REQUEST_CODE_BUTTON = ('xpath', '//button[contains(@class, "two-fa-page__retry")]')
DISABLE_CONFIRM_BUTTON = ('xpath', '//div[contains(@class, "two-fa-page__footer")]/button[@disabled="disabled"]')
CONFIRM_BUTTON_VER_PAGE = ('xpath', '(//div[contains(@class, "two-fa-page__footer")]/button)[1]')
ENTER_BACKUP_CODE_BUTTON = ('xpath', '(//div[contains(@class, "two-fa-page__footer")]/button)[2]')
TIMER = ('xpath', '(//div[contains(@class, "tm-wg-timer")]/..//div)[1]')

ERROR_VERIFICATION_CODE = ('xpath', '//div[contains(@class, "el-input-separated__errors")]/div')

BACKUP_CODE_FIELD = ('xpath', '//input[@id = "reserve_code"]')
SUPPORT_EMAIL_LINK = ('xpath', '//a[contains(@href, "mailto")]')
ERROR_BACKUP_CODE = ('xpath', '//div[contains(@class, "mc-field-text__error-text")]/div')
LOADER_ON_CONFIRM_BUTTON = ('xpath', '//span[@class = "mc-button__loader"]')
CONFIRM_BACKUP_BUTTON = ('xpath', '//div[contains(@class, "two-fa-page__footer")]/button')


class VerificationPage(BasePage):
    page_url = f'{local}/auth/2fa?type=default'

    def check_button_is_disabled_timer_runs(self):
        with allure.step('Проверка наличия таймера на странице'):
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.check_button_is_disabled_timer_runs.__name__}_initial_state_of_verification_page",
                          attachment_type=AttachmentType.PNG)
            self.wait.until(EC.none_of(EC.element_to_be_clickable(CONFIRM_BUTTON_VER_PAGE)))
            self.wait.until(EC.invisibility_of_element_located(REQUEST_CODE_BUTTON))

    def check_backup_page_is_open_button_disabled(self):
        with allure.step('Проверка перехода на страницу ввода резервных кодов'):
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.check_backup_page_is_open_button_disabled.__name__}_initial_state_of_backup_page",
                          attachment_type=AttachmentType.PNG)
        self.wait.until(EC.invisibility_of_element_located(VERIFICATION_FIELD))
        self.wait.until(EC.visibility_of_element_located(BACKUP_CODE_FIELD))
        self.wait.until(EC.none_of((EC.element_to_be_clickable(CONFIRM_BACKUP_BUTTON))))

    def check_validation_of_backup_codes_by_lenght(self, data):
        with allure.step('Проверка активности кнопки в зависимости от длины введенного кода'):
            if len(data) == 12:
                self.wait.until(EC.element_to_be_clickable(CONFIRM_BACKUP_BUTTON))
                allure.attach(self.driver.get_screenshot_as_png(),
                              name=f"{self.check_validation_of_backup_codes_by_lenght.__name__}_entered_code_and_active_button",
                              attachment_type=AttachmentType.PNG)
            else:
                self.wait.until(EC.none_of((EC.element_to_be_clickable(CONFIRM_BACKUP_BUTTON))))
                allure.attach(self.driver.get_screenshot_as_png(),
                              name=f"{self.check_validation_of_backup_codes_by_lenght.__name__}_entered_code_and_disabled_button",
                              attachment_type=AttachmentType.PNG)

    def error_text_after_invalid_backup_code(self):
        self.wait.until(EC.visibility_of_all_elements_located(ERROR_BACKUP_CODE))

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
        with allure.step('Проверка отображения ошибки "невалидный код"'):
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.error_text_after_invalid_backup_code.__name__}_error_text_is_shown",
                          attachment_type=AttachmentType.PNG)
            assert self.find(
                ERROR_BACKUP_CODE).text == text.invalid_backup_code, 'error text did not match'

    def five_attempts(self, data, field_locator, button_locator, error_locator):
        for i in data:
            self.find_and_clean_field(field_locator)
            self.find_and_send_text_in_field(field_locator, i)
            self.find_and_click_element(button_locator)
            self.wait.until(EC.visibility_of_element_located(error_locator))

    def fill_out_2fa_once(self, locator, data):
        self.wait.until(EC.element_to_be_clickable(locator))
        text_area = self.find_all(locator)

        for i in text_area:
            i.click()
            with allure.step(f'Ввод данных {data} в поле ввода {locator}'):
                i.send_keys(data)
                allure.attach(self.driver.get_screenshot_as_png(),
                              name=f"{self.find_and_send_text_in_field.__name__}_there are entered data in a field",
                              attachment_type=AttachmentType.PNG)
                return
        self.wait.until(EC.visibility_of_element_located(LOADER_ON_CONFIRM_BUTTON))

    def fill_2fa_five_times(self, locator, data_list):
        self.wait.until(EC.element_to_be_clickable(locator))
        text_areas = self.find_all(locator)
        for set in data_list:
            for i in text_areas:
                i.click()
                with allure.step(f'Ввод данных {set} в поле'):
                    i.send_keys(str(set))
                    self.find_and_click_element(CONFIRM_BUTTON_VER_PAGE)
                    allure.attach(self.driver.get_screenshot_as_png(),
                                  name=f"{self.fill_2fa_five_times.__name__}_screenshot",
                                  attachment_type=AttachmentType.PNG)
                    self.wait.until(EC.visibility_of_element_located(ERROR_VERIFICATION_CODE))
                    error = self.find(ERROR_VERIFICATION_CODE)
                    if error:
                        for i in text_areas:
                            i.clear()
                        break


    def request_new_verification_code(self):
        self.wait.until(EC.element_to_be_clickable(REQUEST_CODE_BUTTON))
        with allure.step(f'Проверка появления кликабельной ссылки запроса нового кода 2фа'):
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.request_new_verification_code.__name__}_screenshot",
                          attachment_type=AttachmentType.PNG)
            self.find_and_click_element(REQUEST_CODE_BUTTON)
        with allure.step(f'Клик на кнопку запроса нового кода 2фа и отображение таймера'):
            self.wait.until(EC.visibility_of_element_located(TIMER))
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.request_new_verification_code.__name__}_screenshot",
                          attachment_type=AttachmentType.PNG)

    def error_invalid_2fa_code(self):
        self.wait.until(EC.visibility_of_all_elements_located(ERROR_VERIFICATION_CODE))

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
        with allure.step('Проверка отображения ошибки "неверный код 2fa"'):
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.error_invalid_2fa_code.__name__}_is_shown",
                          attachment_type=AttachmentType.PNG)
            assert self.find(
                ERROR_VERIFICATION_CODE).text == text.wrong_2fa_code, 'error text did not match'

    def error_request_new_verification_code(self):
        self.wait.until(EC.visibility_of_all_elements_located(ERROR_VERIFICATION_CODE))

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
        with allure.step('Проверка отображения ошибки "запроси новый код 2fa"'):
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.error_request_new_verification_code.__name__}_is_shown",
                          attachment_type=AttachmentType.PNG)
            assert self.find(
                ERROR_VERIFICATION_CODE).text == text.error_limit_2fa_codes, 'error text did not match'
