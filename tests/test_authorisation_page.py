
import pytest

from config.custom_data import Custom_Data
from helper.data_generator import valid_email, valid_hexdigits_password
from pages.authorisation_page import *
from pages.base_page import ES_LANGUAGE_BUTTON, EN_LANGUAGE_BUTTON, PT_LANGUAGE_BUTTON, TH_LANGUAGE_BUTTON, \
    VI_LANGUAGE_BUTTON, RU_LANGUAGE_BUTTON


@pytest.mark.authorisation
@allure.title('Тест открытия Privacy Policy')
@allure.feature('Authorization page')
def test_open_privacy_policy(authorisation_page):
    authorisation_page.open_page()
    authorisation_page.open_document(PRIVACY_POLICY_AUTORISARION_PAGE)


@pytest.mark.authorisation
@allure.title('Тест перехода на stores')
@allure.feature('Authorization page')
@pytest.mark.parametrize('store', [APPSTORE_BUTTON, GOOGLE_STORE_BUTTON])
def test_open_stores(authorisation_page, store):
    authorisation_page.open_page()
    authorisation_page.open_store(store)


@pytest.mark.authorisation
@allure.feature('Authorization page')
@allure.title('Тест открытия окон авторизации в соц. сети')
@pytest.mark.parametrize('social_network', [GOOGLE_BUTTON, APPLE_BUTTON, FACEBOOK_BUTTON])
def test_open_social_network_authorisation_form(authorisation_page, social_network):
    authorisation_page.open_page()
    authorisation_page.open_social_network_authorisation_form(social_network)


@pytest.mark.authorisation
@allure.feature('Authorization page')
@allure.title('Тест перехода на лэндинг, страницы регистрации и восстановления пароля')
@pytest.mark.parametrize('url, locator',
                         [
                             (Links.landing_url, MCPAY_BUTTON),
                             (Links.registration_url, SIGN_IN_BUTTON_AUTORISATION_PAGE),
                             (Links.reset_password_url, FORGOT_PASSWORD_BUTTON)
                         ])
def test_redirect_to_diff_page_by_button(authorisation_page, url, locator,
                                         marker_of_invisibility=SIGN_IN_AREA_AUTHORISATION_PAGE):
    authorisation_page.open_page()
    authorisation_page.find_and_click_element(locator)
    authorisation_page.check_open_another_page(marker_of_invisibility, url)


@pytest.mark.authorisation
@allure.feature('Authorization page')
@allure.title('Тест изменения локали страницы')
@pytest.mark.parametrize('local_language',
                         [ES_LANGUAGE_BUTTON, RU_LANGUAGE_BUTTON, PT_LANGUAGE_BUTTON, VI_LANGUAGE_BUTTON,
                          TH_LANGUAGE_BUTTON, EN_LANGUAGE_BUTTON])
def test_change_local_language(authorisation_page, local_language):
    authorisation_page.open_page()
    authorisation_page.change_local_page(local_language)


@pytest.mark.authorisation
@allure.feature('Authorization page')
@allure.title('Тест авторизации с пустыми полями')
def test_authorization_with_empty_fields(authorisation_page):
    authorisation_page.open_page()
    authorisation_page.find_and_clean_field(EMAIL_FIELD)
    authorisation_page.find_and_clean_field(PASSWORD_FIELD)
    authorisation_page.find_and_click_element(LOGIN_BUTTON_AUTORISATION_PAGE)
    authorisation_page.check_error_required_field()


@pytest.mark.authorisation
@allure.feature('Authorization page')
@allure.title('Тест авторизации с невалидными email, password')
@pytest.mark.parametrize('email, password',
                         [('without.at', '12345678'),
                          ('without@dot', 'qwertyzxc'),
                          ('wrong.place@of_punctuation', 'qwerty123')
                          ])
def test_authorization_with_invalid_data(authorisation_page, email, password):
    authorisation_page.open_page()
    authorisation_page.find_and_clean_field(EMAIL_FIELD)
    authorisation_page.find_and_send_text_in_field(EMAIL_FIELD, email)
    authorisation_page.find_and_clean_field(PASSWORD_FIELD)
    authorisation_page.find_and_send_text_in_field(PASSWORD_FIELD, password)
    authorisation_page.find_and_click_element(LOGIN_BUTTON_AUTORISATION_PAGE)
    authorisation_page.check_invalid_email_error()


@pytest.mark.authorisation
@allure.feature('Authorization page')
@allure.title('Тест авторизации с валидным email, не существующим в БД')
def test_authorization_with_valid_no_existed_data(authorisation_page, email=valid_email,
                                                  password=valid_hexdigits_password):
    authorisation_page.open_page()
    authorisation_page.find_and_clean_field(EMAIL_FIELD)
    authorisation_page.find_and_send_text_in_field(EMAIL_FIELD, email)
    authorisation_page.find_and_clean_field(PASSWORD_FIELD)
    authorisation_page.find_and_send_text_in_field(PASSWORD_FIELD, password)
    authorisation_page.find_and_click_element(LOGIN_BUTTON_AUTORISATION_PAGE)
    authorisation_page.check_no_exist_on_DB_email_error()


@pytest.mark.authorisation
@allure.feature('Authorization page')
@allure.title('Тест авторизации с валидным email и включенной 2fa + работоспособность кнопки "показать пароль"')
def test_login_to_account_with_enabled_2fa(authorisation_page, email=Custom_Data.email_2fa,
                                           password=Custom_Data.password_2fa):
    authorisation_page.open_page()
    authorisation_page.find_and_clean_field(EMAIL_FIELD)
    print(f"email: {email}")
    authorisation_page.find_and_send_text_in_field(EMAIL_FIELD, email)
    authorisation_page.find_and_clean_field(PASSWORD_FIELD)
    authorisation_page.find_and_send_text_in_field(PASSWORD_FIELD, password)
    authorisation_page.one_minute_pause()
    authorisation_page.click_show_password_button()
    authorisation_page.find_and_click_element(LOGIN_BUTTON_AUTORISATION_PAGE)
    authorisation_page.check_redirect_to_2fa_after_login()


@pytest.mark.authorisation
@allure.feature('Authorization page')
@allure.title('Тест авторизации с валидным email и ВЫКЛЮЧЕННОЙ 2fa')
def test_login_to_account_with_disabled_2fa(authorisation_page, email=Custom_Data.email_no_2fa,
                                            password=Custom_Data.password_no_2fa):
    authorisation_page.open_page()
    authorisation_page.find_and_clean_field(EMAIL_FIELD)
    authorisation_page.find_and_send_text_in_field(EMAIL_FIELD, email)
    authorisation_page.find_and_clean_field(PASSWORD_FIELD)
    authorisation_page.find_and_send_text_in_field(PASSWORD_FIELD, password)
    authorisation_page.one_minute_pause()
    authorisation_page.find_and_click_element(LOGIN_BUTTON_AUTORISATION_PAGE)
    authorisation_page.check_redirect_to_home_account()


@pytest.mark.authorisation
@allure.feature('Authorization page')
@allure.title('Тест перехода на страницу восстановления пароля с заполненным email')
def test_go_to_password_recover_page_with_filled_email(authorisation_page, email=valid_email):
    authorisation_page.open_page()
    authorisation_page.find_and_clean_field(EMAIL_FIELD)
    authorisation_page.find_and_send_text_in_field(EMAIL_FIELD, email)
    authorisation_page.find_and_click_element(FORGOT_PASSWORD_BUTTON)
    authorisation_page.check_open_another_page(SIGN_IN_AREA_AUTHORISATION_PAGE, Links.reset_password_url)
