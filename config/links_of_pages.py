# подставляем локаль для теста. пустая = EN

import os
from dotenv import load_dotenv

load_dotenv()

local = '/ru'
class Links:
    HOST = os.getenv('HOST')

    registration_url = f'{HOST}{local}/auth/sign-up'
    authorisation_url = f'{HOST}{local}/auth/sign-in'
    reset_password_url = f'{HOST}{local}/auth/reset'
    twofa_url = f'{HOST}{local}/auth/2fa?type=default'
    home_url = f'{HOST}{local}/home/account'
    landing_url = f'{HOST}{local}'



