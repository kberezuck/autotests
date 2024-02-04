import pytest

from config.links_of_pages import Links
from helper.data_generator import valid_length_backup_code, invalid_length_backup_code, list_of_six_backup_codes, \
    list_with_verification_codes
from pages.verification_page import *


@pytest.mark.verification_2fa
@pytest.mark.run(order=1)
@allure.title('Тест перехода на stores')
@allure.feature('Verification page')
@pytest.mark.parametrize('store', [APPSTORE_BUTTON, GOOGLE_STORE_BUTTON])
def test_open_stores(verification_page_2fa, store):
    verification_page_2fa.open_store(store)


@pytest.mark.verification_2fa
@pytest.mark.run(order=2)
@allure.title('Тест перехода на лендинг и стр.авторизации')
@allure.feature('Verification page')
@pytest.mark.parametrize('url, locator',
                         [
                             (Links.authorisation_url, BACK_BUTTON),
                             (Links.landing_url, MCPAY_BUTTON),

                         ])
def test_back_to_authorisation_and_landing_page(verification_page_2fa, url, locator,
                                                marker_of_invisibility=VERIFICATION_FIELD):
    verification_page_2fa.find_and_click_element(locator)
    verification_page_2fa.check_open_another_page(marker_of_invisibility, url)


@pytest.mark.verification_2fa
@pytest.mark.run(order=3)
@allure.title('Тест первоначального состояния страницы верификации: задизейблена кнопка + таймер')
@allure.feature('Verification page')
def test_check_initial_state_of_verification_page(verification_page_2fa):
    verification_page_2fa.check_that_field_is_empty(INPUT_FIELD)
    verification_page_2fa.check_button_is_disabled_timer_runs()


@pytest.mark.verification_2fa
@pytest.mark.run(order=5)
@allure.title('Тест запроса нового 2фа кода')
@allure.feature('Verification page')
def test_request_new_2fa_code(verification_page_2fa):
    verification_page_2fa.check_button_is_disabled_timer_runs()
    verification_page_2fa.one_minute_pause()
    verification_page_2fa.request_new_verification_code()

@pytest.mark.verification_2fa
@pytest.mark.run(order=4)
@allure.title('Тест ввода невалидного кода 2фа')
@allure.feature('Verification page')
def test_fill_2fa_code(verification_page_2fa):
    verification_page_2fa.fill_out_2fa_once(INPUT_FIELD, ['1', '2', '3', '4', '5', '6'])
    verification_page_2fa.error_invalid_2fa_code()


@pytest.mark.verification_2fa
@pytest.mark.run(order=6)
@allure.title('Тест ввода невалидного кода 2фа 5 раз')
@allure.feature('Verification page')
def test_error_request_new_2fa_code(verification_page_2fa):
    verification_page_2fa.fill_2fa_five_times(INPUT_FIELD, list_with_verification_codes)
    verification_page_2fa.error_request_new_verification_code()



@pytest.mark.verification_backup
@allure.title('Тест перехода на страницу ввода резервных кодов, ввод (не)валидного по длине кода')
@allure.feature('Verification page')
@pytest.mark.parametrize('data', [valid_length_backup_code, invalid_length_backup_code])
def test_invalid_data_in_backup_field(verification_page_backup, data):
    verification_page_backup.find_and_click_element(ENTER_BACKUP_CODE_BUTTON)
    verification_page_backup.check_backup_page_is_open_button_disabled()
    verification_page_backup.find_and_send_text_in_field(BACKUP_CODE_FIELD, data)
    verification_page_backup.check_validation_of_backup_codes_by_lenght(data)


@pytest.mark.verification_backup
@allure.title('Тест текста ошибки при вводе невалидного резервного кода')
@allure.feature('Verification page')
def test_enter_invalid_code_check_error(verification_page_backup):
    verification_page_backup.find_and_click_element(ENTER_BACKUP_CODE_BUTTON)
    verification_page_backup.check_backup_page_is_open_button_disabled()
    verification_page_backup.find_and_send_text_in_field(BACKUP_CODE_FIELD, valid_length_backup_code)
    verification_page_backup.find_and_click_element(CONFIRM_BACKUP_BUTTON)
    verification_page_backup.error_text_after_invalid_backup_code()


@pytest.mark.verification_backup
@allure.title('Тест текста ошибки при вводе 5 невалидных резервных кодов')
@allure.feature('Verification page')
def test_limits_attempts_error(verification_page_backup):
    verification_page_backup.find_and_click_element(ENTER_BACKUP_CODE_BUTTON)
    verification_page_backup.check_backup_page_is_open_button_disabled()
    verification_page_backup.five_attempts(list_of_six_backup_codes, BACKUP_CODE_FIELD, CONFIRM_BACKUP_BUTTON,
                                    ERROR_BACKUP_CODE)
    verification_page_backup.error_text_limit_attempts(ERROR_BACKUP_CODE)


@pytest.mark.verification_backup
@allure.title('Тест отправки нового рерервного кода после минутного блока')
@allure.feature('Verification page')
def test_enter_backup_code_after_one_minutes_block(verification_page_backup):
    verification_page_backup.find_and_click_element(ENTER_BACKUP_CODE_BUTTON)
    verification_page_backup.check_backup_page_is_open_button_disabled()
    verification_page_backup.five_attempts(list_of_six_backup_codes, BACKUP_CODE_FIELD, CONFIRM_BACKUP_BUTTON,
                                    ERROR_BACKUP_CODE)
    verification_page_backup.error_text_limit_attempts(ERROR_BACKUP_CODE)
    verification_page_backup.one_minute_pause()
    verification_page_backup.find_and_clean_field(BACKUP_CODE_FIELD)
    verification_page_backup.find_and_send_text_in_field(BACKUP_CODE_FIELD, valid_length_backup_code)
    verification_page_backup.find_and_click_element(CONFIRM_BACKUP_BUTTON)
    verification_page_backup.error_text_after_invalid_backup_code()
