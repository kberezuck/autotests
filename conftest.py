import pytest, os, shutil

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pages.authorisation_page import EMAIL_FIELD, PASSWORD_FIELD, LOGIN_BUTTON_AUTORISATION_PAGE
from config.custom_data import Custom_Data
from dotenv import load_dotenv

from pages.registration_page import RegistrationPage
from pages.authorisation_page import AuthorisationPage
from pages.verification_page import VerificationPage
from pages.reset_password_page import ResetPasswordPage


@pytest.fixture(scope='session')
def move_directory_within_project():
    project_root = os.getcwd()
    results_dir = r'allure-results'
    report_dir = r"allure-report"
    history_dir = r'allure-report\history'
    history_results = r'allure-results\history'
    #Создание путей к необходимым директориям

    results_dir_path = os.path.join(project_root, results_dir)
    report_dir_path = os.path.join(project_root, report_dir)
    history_dir_path = os.path.join(project_root,history_dir)
    history_results_dir_path = os.path.join(project_root, history_results)

    # Проверяем, что results директория существует внутри проекта и удаляем ее при наличии

    if os.path.exists(results_dir_path):
        shutil.rmtree(results_dir_path)
    else:
        print(f'{results_dir} does not exist')
        pass

    # Проверяем, что history существует внутри проекта и перемещаем ее при наличии

    if os.path.exists(history_dir_path):
        shutil.copytree(history_dir_path, history_results_dir_path)
    else:
        print(f'{history_dir} does not exist')
        pass


    # Проверяем, что report существует внутри проекта и при наличии - удаляем его
    if os.path.exists(report_dir_path):
        shutil.rmtree(report_dir_path)
    else:
        print(f'{report_dir} does not exist')


load_dotenv()

@pytest.fixture()
def driver():

    options = Options()
    options.add_argument("--window-size=1920,1080")
    # options.add_argument('--headless')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    chrome_driver = webdriver.Chrome(options=options)
    actions_element = ActionChains(chrome_driver)
    yield chrome_driver, actions_element
    chrome_driver.quit()



@pytest.fixture()
def authorisation_page(driver):
    chrome_driver, actions_element = driver
    return AuthorisationPage(chrome_driver, actions_element)


@pytest.fixture()
def registration_page(driver):
    chrome_driver, actions_element = driver
    return RegistrationPage(chrome_driver, actions_element)


@pytest.fixture()
def verification_page_2fa(authorisation_page):
    email = Custom_Data.email3
    password = Custom_Data.password_no_2fa
    authorisation_page.open_page()
    authorisation_page.find_and_clean_field(EMAIL_FIELD)
    authorisation_page.find_and_send_text_in_field(EMAIL_FIELD, email)
    authorisation_page.find_and_clean_field(PASSWORD_FIELD)
    authorisation_page.find_and_send_text_in_field(PASSWORD_FIELD, password)
    authorisation_page.one_minute_pause()
    authorisation_page.find_and_click_element(LOGIN_BUTTON_AUTORISATION_PAGE)
    authorisation_page.check_redirect_to_2fa_after_login()
    return VerificationPage(authorisation_page.driver, authorisation_page.actions)


@pytest.fixture()
def verification_page_backup(authorisation_page):
    email = Custom_Data.email2
    password = Custom_Data.password_2fa
    authorisation_page.open_page()
    authorisation_page.find_and_clean_field(EMAIL_FIELD)
    authorisation_page.find_and_send_text_in_field(EMAIL_FIELD, email)
    authorisation_page.find_and_clean_field(PASSWORD_FIELD)
    authorisation_page.find_and_send_text_in_field(PASSWORD_FIELD, password)
    authorisation_page.one_minute_pause()
    authorisation_page.find_and_click_element(LOGIN_BUTTON_AUTORISATION_PAGE)
    authorisation_page.check_redirect_to_2fa_after_login()
    return VerificationPage(authorisation_page.driver, authorisation_page.actions)


@pytest.fixture()
def reset_password_page(driver):
    chrome_driver, actions_element = driver
    return ResetPasswordPage(chrome_driver, actions_element)
