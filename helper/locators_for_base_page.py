GOOGLE_BUTTON = ('xpath', '//span[contains(text(),"Google")]')
FACEBOOK_BUTTON = ('xpath', '//span[contains(text(),"Facebook")]')
APPLE_BUTTON = ('xpath', '//span[contains(text(),"Apple")]')

MCPAY_BUTTON = ('xpath', "//div[@class ='pt-auth-header__logo']")

GOOGLE_STORE_BUTTON = ('xpath', "//img[@alt = 'GooglePlay']")
APPSTORE_BUTTON = ('xpath', "//img[@alt = 'AppStore']")

LANGUAGE_SELECT = ('xpath', '//div[@tabindex="0"]//span[@class="mc-button__append"]')
LANGUAGE_DROPDOWN = ('xpath', "//section[@class = 'mc-dropdown-panel']")
CHECK_ATTRIBUTE_LANGUAGE_DROPDOWN = ('xpath', '//div[contains(@class," tm-wg-locales-dropdown")]')

ERROR_BLOCK = ('xpath', '//div[@class="mc-field-text__footer"]')

PASSWORD_FIELD = ('xpath', '//input[@id = "password"]')
SHOW_PASSWORD_BUTTON = ('xpath', '//button[@tabindex ="-1"]')
TOOLTIP_BY_PASSWORD = ('xpath', '//div[@class = "tooltip-inner__content"]')
CHECK_VISIBILITY_OF_TOOLTIP = ('xpath', '//div[contains(@class, "mc-tooltip-target has-tooltip")]')

ERROR_EMAIL_FIELD = ('xpath',
                     '//label[@for = "email"]/following-sibling::div[@class ="mc-field-text__footer"]//div[@ class="mc-title__text"]')