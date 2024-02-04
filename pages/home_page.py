from pages.base_page import BasePage
from config.links_of_pages import local

WELCOME_MODAL = ('xpath', '//div[@class="tm-studio-onboarding-modal__body_benefits"]')

class HomePage(BasePage):
    page_url = f'{local}/home/account'
