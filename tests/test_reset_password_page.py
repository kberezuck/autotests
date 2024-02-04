import pytest

from config.links_of_pages import Links
from helper.data_generator import valid_email
from pages.base_page import ES_LANGUAGE_BUTTON, EN_LANGUAGE_BUTTON, TH_LANGUAGE_BUTTON, RU_LANGUAGE_BUTTON, \
    PT_LANGUAGE_BUTTON, VI_LANGUAGE_BUTTON
from pages.reset_password_page import *


@pytest.mark.reset_password
@allure.title('Тест перехода на stores')
@allure.feature('Reset password page')
@pytest.mark.parametrize('store', [APPSTORE_BUTTON, GOOGLE_STORE_BUTTON])
def test_open_stores(reset_password_page, store):
    reset_password_page.open_page()
    reset_password_page.open_store(store)


@pytest.mark.reset_password
@allure.title('Тест перехода на лендинг и стр.авторизации')
@allure.feature('Reset password page')
@pytest.mark.parametrize('url, locator',
                         [
                             (Links.authorisation_url, REMEMBER_PASSWORD_BUTTON),
                             (Links.landing_url, MCPAY_BUTTON),

                         ])
def test_back_to_authorisation_and_landing_page(reset_password_page, url, locator,
                                                marker_of_invisibility=RESET_PASSWORD_FIELD):
    reset_password_page.open_page()
    reset_password_page.find_and_click_element(locator)
    reset_password_page.check_open_another_page(marker_of_invisibility, url)


@pytest.mark.reset_password
@allure.feature('Reset password page')
@allure.title('Тест изменения локали страницы')
@pytest.mark.parametrize('local_language',
                         [ES_LANGUAGE_BUTTON, RU_LANGUAGE_BUTTON, PT_LANGUAGE_BUTTON, VI_LANGUAGE_BUTTON,
                          TH_LANGUAGE_BUTTON, EN_LANGUAGE_BUTTON])
def test_change_local_language(reset_password_page, local_language):
    reset_password_page.open_page()
    reset_password_page.change_local_page(local_language)


@pytest.mark.reset_password
@allure.feature('Reset password page')
@allure.title('Тест отправки пустого поля')
def test_submit_with_empty_fields(reset_password_page):
    reset_password_page.open_page()
    reset_password_page.find_and_clean_field(EMAIL_FIELD)
    reset_password_page.find_and_click_element(SUBMIT_BUTTON_FROM_RECOVER_PAGE)
    reset_password_page.check_error_required_field()


@pytest.mark.reset_password
@allure.feature('Reset password page')
@allure.title('Тест отправки невалидного email')
@pytest.mark.parametrize('email', ['without.at', 'without@dot', 'wrong.place@of_punctuation'])
def test_send_invalid_email(reset_password_page, email):
    reset_password_page.open_page()
    reset_password_page.find_and_clean_field(EMAIL_FIELD)
    reset_password_page.find_and_send_text_in_field(EMAIL_FIELD, email)
    reset_password_page.find_and_click_element(SUBMIT_BUTTON_FROM_RECOVER_PAGE)
    reset_password_page.check_invalid_email_error()


@pytest.mark.reset_password
@allure.feature('Reset password page')
@allure.title('Тест отправки валидного email')
def test_send_valid_email(reset_password_page, email=valid_email):
    reset_password_page.open_page()
    reset_password_page.find_and_clean_field(EMAIL_FIELD)
    reset_password_page.find_and_send_text_in_field(EMAIL_FIELD, email)
    reset_password_page.find_and_click_element(SUBMIT_BUTTON_FROM_RECOVER_PAGE)
    reset_password_page.successful_sent_email(email)
