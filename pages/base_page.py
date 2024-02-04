import allure
import time
from allure_commons.types import AttachmentType
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from config.links_of_pages import Links
from error_messages import error_text_vi, error_text_th, error_text_pt, error_text_es, error_text_en, error_text_ru
from helper.SM_and_store_links import *
from helper.locators_for_base_page import *

RU_LANGUAGE_BUTTON = ('xpath', "//section//a[contains(@class, 'mc-button')]/span[contains(text(), 'RU')]")
ES_LANGUAGE_BUTTON = ('xpath', "//section//a[contains(@class, 'mc-button')]/span[contains(text(), 'ES')]")
PT_LANGUAGE_BUTTON = ('xpath', "//section//a[contains(@class, 'mc-button')]/span[contains(text(), 'PT')]")
VI_LANGUAGE_BUTTON = ('xpath', "//section//a[contains(@class, 'mc-button')]/span[contains(text(), 'VI')]")
TH_LANGUAGE_BUTTON = ('xpath', "//section//a[contains(@class, 'mc-button')]/span[contains(text(), 'TH')]")
EN_LANGUAGE_BUTTON = ('xpath', "//section//a[contains(@class, 'mc-button')]/span[contains(text(), 'EN')]")


class BasePage:
    host_url = Links.HOST
    page_url = None

    def __init__(self, driver: WebDriver, actions: ActionChains):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5, poll_frequency=1)
        self.actions = actions

    def open_page(self):
        with allure.step('Открытие страницы'):
            if self.page_url:
                self.driver.get(f'{self.host_url}{self.page_url}')
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{self.open_page.__name__}_page is opened",
                              attachment_type=AttachmentType.PNG)
            else:
                allure.attach(self.driver.get_screenshot_as_png(),
                              name=f"{self.open_page.__name__}_page was not opened",
                              attachment_type=AttachmentType.PNG)
                raise NotImplementedError('Can not open page')

    def one_minute_pause(self):
        time.sleep(60)

    def find(self, locator):
        return self.driver.find_element(*locator)

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def find_and_click_element(self, locator):
        with allure.step(f'Клик на элемент {locator}'):
            self.wait.until(EC.element_to_be_clickable(locator))
            self.find(locator).click()

    def find_and_clean_field(self, locator):
        with allure.step(f'Очистка поля ввода {locator}'):
            self.wait.until(EC.element_to_be_clickable(locator))
            self.find(locator).clear()

    def check_that_field_is_empty(self, locator):
        self.wait.until((EC.presence_of_element_located(locator)))
        text_field = self.find(locator).text
        print(text_field)
        with allure.step(f'Проверка, что поле ввода пустое {locator}'):
            assert text_field == '', 'text area is not empty'

    def check_that_field_is_full(self, locator, data):
        with allure.step(f'Проверка, что в поле ввода {locator} введены данные {data}'):
            self.wait.until(EC.text_to_be_present_in_element(locator, data))

    def find_and_send_text_in_field(self, locator, data):
        self.wait.until(EC.element_to_be_clickable(locator))
        text_area = self.find(locator)
        text_area.click()
        with allure.step(f'Ввод данных {data} в поле ввода {locator}'):
            text_area.send_keys(data)
        with allure.step(f'Проверка, что в поле ввода {locator} содержатся введенные данные {data}'):
            self.wait.until(EC.text_to_be_present_in_element_value(locator, data))
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.find_and_send_text_in_field.__name__}_there are entered data in a field",
                          attachment_type=AttachmentType.PNG)

    def open_new_window(self, locator):
        current_url = self.get_current_url()
        windows_before = self.driver.window_handles
        self.find_and_click_element(locator=locator)
        with allure.step('Проверка, что открылось новое окно'):
            self.wait.until(EC.new_window_is_opened(windows_before))
        with allure.step('Переключение на новое окно'):
            self.driver.switch_to.window([x for x in self.driver.window_handles if x not in windows_before][0])
        opened_url = self.get_current_url()
        with allure.step('Проверка, что url исходного и открывшегося окна отличаются'):
            assert current_url != opened_url, 'new window was not opened'

    def get_current_url(self):
        return self.driver.current_url

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Общие методы для страниц входной группы!!!!!!!!!!!!!!!!!!!!!!!!!!

    # тут бы хотелось проверочку на тайтл открытого документа добавить
    def open_document(self, document):
        self.open_new_window(locator=document)
        allure.attach(self.driver.get_screenshot_as_png(), name=f"{self.open_document.__name__}_Screenshot",
                      attachment_type=AttachmentType.PNG)
        self.driver.quit()

    def open_store(self, store_button):
        self.open_new_window(locator=store_button)
        if store_button == APPSTORE_BUTTON:
            with allure.step('Проверка, что открылся APPSTORE'):
                self.wait.until(EC.url_to_be(APP_STORE))
                allure.attach(self.driver.get_screenshot_as_png(),
                              name=f"{self.open_store.__name__}_APP store is opened",
                              attachment_type=AttachmentType.PNG)
        elif store_button == GOOGLE_STORE_BUTTON:
            with allure.step('Проверка, что открылся GOOGLE STORE'):
                self.wait.until(EC.url_to_be(GOOGLE_STORE))
                allure.attach(self.driver.get_screenshot_as_png(),
                              name=f"{self.open_store.__name__}_Play Store is opened",
                              attachment_type=AttachmentType.PNG)
        self.driver.quit()

    def open_social_network_authorisation_form(self, social_network):
        self.open_new_window(locator=social_network)
        if social_network == GOOGLE_BUTTON:
            with allure.step('Проверка, что открылось окно авторизации Google'):
                self.wait.until(EC.url_contains(GOOGLE_AUTHORISATION_PAGE))
                allure.attach(self.driver.get_screenshot_as_png(),
                              name=f"{self.open_social_network_authorisation_form.__name__}_Google",
                              attachment_type=AttachmentType.PNG)
        elif social_network == APPLE_BUTTON:
            with allure.step('Проверка, что открылось окно авторизации Apple'):
                self.wait.until(EC.url_contains(APPLE_AUTHORISATION_PAGE))
                allure.attach(self.driver.get_screenshot_as_png(),
                              name=f"{self.open_social_network_authorisation_form.__name__}_Apple",
                              attachment_type=AttachmentType.PNG)
        elif social_network == FACEBOOK_BUTTON:
            with allure.step('Проверка, что открылось окно авторизации Facebok'):
                self.wait.until(EC.url_contains(FACEBOOK_AUTHORISATION_PAGE))
                allure.attach(self.driver.get_screenshot_as_png(),
                              name=f"{self.open_social_network_authorisation_form.__name__}_Faceebok",
                              attachment_type=AttachmentType.PNG)

    def change_local_page(self, language):
        self.find_and_click_element(LANGUAGE_SELECT)
        self.wait.until(EC.visibility_of_element_located(LANGUAGE_DROPDOWN))
        with allure.step('Проверка, что дропдаун с языками открыт'):
            self.wait.until(EC.text_to_be_present_in_element_attribute(CHECK_ATTRIBUTE_LANGUAGE_DROPDOWN, 'class',
                                                                       'mc-dropdown--is-open'))
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.change_local_page.__name__}_dropdown is opened",
                          attachment_type=AttachmentType.PNG)
        self.find_and_click_element(language)
        with allure.step('Проверка соответствия выбранной локали с открытой страницей'):
            if language == RU_LANGUAGE_BUTTON:
                self.wait.until(EC.url_contains('io/ru/auth/'))
            elif language == VI_LANGUAGE_BUTTON:
                self.wait.until(EC.url_contains('io/vi/auth/'))
            elif language == ES_LANGUAGE_BUTTON:
                self.wait.until(EC.url_contains('io/es/auth/'))
            elif language == PT_LANGUAGE_BUTTON:
                self.wait.until(EC.url_contains('io/pt/auth/'))
            elif language == TH_LANGUAGE_BUTTON:
                self.wait.until(EC.url_contains('io/th/auth/'))
            else:
                self.wait.until(EC.url_contains('io/auth/'))
        with allure.step('Проверка, что дропдаун с языками закрыт'):
            self.wait.until(EC.none_of(
                EC.text_to_be_present_in_element_attribute(CHECK_ATTRIBUTE_LANGUAGE_DROPDOWN, 'class',
                                                           'mc-dropdown--is-open')))

    def click_show_password_button(self):
        button = self.find(SHOW_PASSWORD_BUTTON)
        with allure.step('Наведение курсора на элемент'):
            self.actions.move_to_element(button).pause(2).perform()
        with allure.step('Дожидаемся появления тултипа'):
            self.wait.until(
                EC.text_to_be_present_in_element_attribute(CHECK_VISIBILITY_OF_TOOLTIP, 'class', 'v-tooltip-open'))
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.click_show_password_button.__name__}_tooltip is shown",
                          attachment_type=AttachmentType.PNG)
        with allure.step('Получение первоначального значения типа поля "пароль"'):
            initial_state_of_password_type = self.find(PASSWORD_FIELD).get_attribute('type')
        with allure.step('Клик на кнопку'):
            button.click()
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.click_show_password_button.__name__}_password does not secured",
                          attachment_type=AttachmentType.PNG)
        with allure.step('Проверка, что тип поля "пароль" изменился'):
            if initial_state_of_password_type == 'password':
                self.wait.until(EC.text_to_be_present_in_element_attribute(PASSWORD_FIELD, 'type', 'text'))
            elif initial_state_of_password_type == 'text':
                self.wait.until(EC.text_to_be_present_in_element_attribute(PASSWORD_FIELD, 'type', 'password'))

    def check_open_another_page(self, marker_of_invisibility, url):
        self.wait.until(EC.invisibility_of_element(marker_of_invisibility))
        with allure.step('Проверка, что произошел редирект на другую страницу'):
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.check_open_another_page.__name__}_in the same window",
                          attachment_type=AttachmentType.PNG)
            current_page = self.get_current_url()
            print(current_page)
            assert current_page == url, f'Redirect to {url} does not happened'

    def error_text_limit_attempts(self, locator):
        self.wait.until(EC.visibility_of_all_elements_located(locator))

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
        with allure.step('Проверка отображения ошибки "превышен лимит попыток"'):
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.error_text_limit_attempts.__name__}_is_shown",
                          attachment_type=AttachmentType.PNG)
            assert self.find(
                locator).text == text.error_limit_attempts, 'error text did not match'

    def check_invalid_email_error(self):
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

        with allure.step('Проверка отображения ошибки "некорректный" email'):
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.check_invalid_email_error.__name__}_is shown",
                          attachment_type=AttachmentType.PNG)
            assert self.find(
                ERROR_EMAIL_FIELD).text == text.invalid_email, 'error text did not match'

    def check_error_required_field(self):
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
        with allure.step('Проверка отображения ошибки "обязательное для заполнения поле"'):
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{self.check_error_required_field.__name__}_is shown",
                          attachment_type=AttachmentType.PNG)
            assert self.find(
                ERROR_BLOCK).text == text.required_field, 'error text did not match'
