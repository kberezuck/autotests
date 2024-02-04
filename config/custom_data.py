
import os
from dotenv import load_dotenv

load_dotenv()

class Custom_Data:
    email_2fa = os.getenv('email_2fa')
    password_2fa = os.getenv('password_2fa')

    email_no_2fa = os.getenv('email_no_2fa')
    password_no_2fa = os.getenv('password_no_2fa')

    # данные для тестов верификации

    email1 = os.getenv('email1')
    email2 = os.getenv('email2')


    valid_mobile_phone = {'Spain': '34651714549', 'France':'33757054355', 'Germany': '4915219658265' }