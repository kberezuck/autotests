import pytest

from config.custom_data import Custom_Data
from helper.data_generator import valid_email, valid_hexdigits_password
from helper.data_generator import valid_first_name, valid_last_name
from pages.base_page import ES_LANGUAGE_BUTTON, EN_LANGUAGE_BUTTON, PT_LANGUAGE_BUTTON, TH_LANGUAGE_BUTTON, \
    VI_LANGUAGE_BUTTON, RU_LANGUAGE_BUTTON
from pages.registration_page import *


@pytest.mark.registration
@allure.title('Тест открытия документов')
@allure.feature('Registration page')
@pytest.mark.parametrize('document', [PRIVACY_POLICY_REGISTRATION_PAGE, TERMS_OF_SERVISE_REGISTRATION_PAGE])
def test_open_documents(registration_page, document):
    registration_page.open_page()
    registration_page.open_document(document)


@pytest.mark.registration
@allure.title('Тест перехода на stores')
@allure.feature('Registration page')
@pytest.mark.parametrize('store', [APPSTORE_BUTTON, GOOGLE_STORE_BUTTON])
def test_open_stores(registration_page, store):
    registration_page.open_page()
    registration_page.open_store(store)


@pytest.mark.registration
@allure.feature('Registration page')
@allure.title('Тест открытия окон авторизации в соц. сети')
@pytest.mark.parametrize('social_network', [GOOGLE_BUTTON, APPLE_BUTTON, FACEBOOK_BUTTON])
def test_open_social_network_authorisation_form(registration_page, social_network):
    registration_page.open_page()
    registration_page.open_social_network_authorisation_form(social_network)


@pytest.mark.registration
@allure.feature('Registration page')
@allure.title('Тест перехода на лэндинг и стр. авторизации mcpay')
@pytest.mark.parametrize('url, locator',
                         [
                             (Links.landing_url, MCPAY_BUTTON),
                             (Links.authorisation_url, LOGIN_FROM_SIGNIN_PAGE),

                         ])
def test_redirect_to_diff_page_by_button(registration_page, url, locator,
                                         marker_of_invisibility=SIGN_UP_AREA_REGISTRATION_PAGE):
    registration_page.open_page()
    registration_page.find_and_click_element(locator)
    registration_page.check_open_another_page(marker_of_invisibility, url)


@pytest.mark.registration
@allure.feature('Registration page')
@allure.title('Тест изменения локали страницы')
@pytest.mark.parametrize('local_language',
                         [ES_LANGUAGE_BUTTON, RU_LANGUAGE_BUTTON, PT_LANGUAGE_BUTTON, VI_LANGUAGE_BUTTON,
                          TH_LANGUAGE_BUTTON, EN_LANGUAGE_BUTTON])
def test_change_local_language(registration_page, local_language):
    registration_page.open_page()
    registration_page.change_local_page(local_language)


@pytest.mark.registration
@allure.feature('Registration page')
@allure.title('Регистрация с пустыми полями')
def test_registration_with_empty_field(registration_page):
    registration_page.open_page()
    registration_page.find_and_clean_field(NAME_FIELD)
    registration_page.find_and_clean_field(LAST_NAME_FIELD)
    registration_page.find_and_clean_field(EMAIL_FIELD)
    registration_page.find_and_clean_field(PASSWORD_FIELD)
    registration_page.find_and_clean_field(PHONE_FIELD)
    registration_page.find_and_click_element(SIGN_IN_BUTTON)
    registration_page.wait.until(EC.visibility_of_all_elements_located(ERROR_BLOCK))
    registration_page.check_error_required_field()


@pytest.mark.registration1
@allure.feature('Registration page')
@allure.title('Регистрация с невалидными данными и не прожатым чек-боксом')
@pytest.mark.parametrize('first_name, last_name, email_data, phone_data, password_data, country',
                         [('Jhон', 'Lenon5', 'without.at', '375556324100', 'qwertyui', 'Germany'),
                          ('25Sara', '$Lolo', 'witout@dot', '37529824672', '12345678', 'Poland'),
                          ('www2', 'ccc3', 'wrong.place@of_symbols', '654846513', 'qwe123', 'Hungary')
                          ])
def test_registration_with_invalid_data(registration_page, first_name, last_name, email_data, phone_data, password_data,
                                        country):
    registration_page.open_page()
    registration_page.change_country(country)
    registration_page.find_and_clean_field(NAME_FIELD)
    registration_page.find_and_send_text_in_field(NAME_FIELD, first_name)
    registration_page.find_and_clean_field(LAST_NAME_FIELD)
    registration_page.find_and_send_text_in_field(LAST_NAME_FIELD, last_name)
    registration_page.find_and_clean_field(EMAIL_FIELD)
    registration_page.find_and_send_text_in_field(EMAIL_FIELD, email_data)
    registration_page.clean_and_fill_phone_field(PHONE_FIELD, phone_data)
    registration_page.find_and_clean_field(PASSWORD_FIELD)
    registration_page.find_and_send_text_in_field(PASSWORD_FIELD, password_data)
    registration_page.find_and_click_element(SIGN_IN_BUTTON)
    registration_page.check_validation_error_text_field()
    registration_page.check_validation_error_checkbox()


@pytest.mark.registration
@allure.feature('Registration page')
@allure.title('Тест на работоспособность кнопки "показать пароль"')
def test_show_password_button(registration_page):
    registration_page.open_page()
    registration_page.find_and_clean_field(PASSWORD_FIELD)
    registration_page.find_and_send_text_in_field(PASSWORD_FIELD, 'qwerty1234')
    registration_page.click_show_password_button()


@pytest.mark.registration
@allure.feature('Registration page')
@allure.title('Регистрация с валидными данными и прожатым чек-боксом')
def test_registration_with_valid_data(registration_page, first_name=valid_first_name, last_name=valid_last_name,
                                      email_data=valid_email, phone_data=Custom_Data.valid_mobile_phone['Spain'],
                                      password_data=valid_hexdigits_password, country='Spain'):
    registration_page.open_page()
    registration_page.change_country(country)
    registration_page.find_and_clean_field(NAME_FIELD)
    registration_page.find_and_send_text_in_field(NAME_FIELD, first_name)
    registration_page.find_and_clean_field(LAST_NAME_FIELD)
    registration_page.find_and_send_text_in_field(LAST_NAME_FIELD, last_name)
    registration_page.find_and_clean_field(EMAIL_FIELD)
    registration_page.find_and_send_text_in_field(EMAIL_FIELD, email_data)
    registration_page.clean_and_fill_phone_field(PHONE_FIELD, phone_data)
    registration_page.find_and_clean_field(PASSWORD_FIELD)
    registration_page.find_and_send_text_in_field(PASSWORD_FIELD, password_data)
    registration_page.click_checkbox(CHECKBOX_PRIVACY, CHECKBOX_PRIVACY_STATUS)
    registration_page.find_and_click_element(SIGN_IN_BUTTON)
    registration_page.check_welcome_modal_home_page()


@pytest.mark.registration
@allure.feature('Registration page')
@allure.title('Регистрация с валидными данными и НЕ прожатым чек-боксом')
def test_registration_valid_data_no_checked_checkbox(registration_page, first_name=valid_first_name,
                                                     last_name=valid_last_name, email_data=valid_email,
                                                     phone_data=Custom_Data.valid_mobile_phone['Germany'],
                                                     password_data=valid_hexdigits_password, country='Germany'):
    registration_page.open_page()
    registration_page.change_country(country)
    registration_page.find_and_clean_field(NAME_FIELD)
    registration_page.find_and_send_text_in_field(NAME_FIELD, first_name)
    registration_page.find_and_clean_field(LAST_NAME_FIELD)
    registration_page.find_and_send_text_in_field(LAST_NAME_FIELD, last_name)
    registration_page.find_and_clean_field(EMAIL_FIELD)
    registration_page.find_and_send_text_in_field(EMAIL_FIELD, email_data)
    registration_page.clean_and_fill_phone_field(PHONE_FIELD, phone_data)
    registration_page.find_and_clean_field(PASSWORD_FIELD)
    registration_page.find_and_send_text_in_field(PASSWORD_FIELD, password_data)
    registration_page.find_and_click_element(SIGN_IN_BUTTON)
    registration_page.check_validation_error_checkbox()


@pytest.mark.registration
@allure.feature('Registration page')
@allure.title('Проверка поля email на регистрацию с уже имеющимся в базе email адресом')
def test_registration_with_existed_email(registration_page, email=Custom_Data.email_2fa):
    registration_page.open_page()
    registration_page.find_and_clean_field(EMAIL_FIELD)
    registration_page.find_and_send_text_in_field(EMAIL_FIELD, email)
    registration_page.find_and_click_element(SIGN_IN_BUTTON)
    registration_page.check_error_email_already_exists()
