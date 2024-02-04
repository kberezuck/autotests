import random
from string import hexdigits, digits

from faker import Faker


def generate_valid_email():
    fake = Faker()
    first_name = fake.first_name_male()
    last_name = fake.last_name()
    return f"{first_name}.{last_name}@{fake.domain_name()}"


valid_email = generate_valid_email()


def generate_valid_name_and_last_name():
    fake = Faker()
    first_name = fake.first_name_male()
    last_name = fake.last_name()
    return first_name, last_name


valid_first_name = generate_valid_name_and_last_name()[0]
valid_last_name = generate_valid_name_and_last_name()[1]


def random_letter_digits_string(begin=1, end=30):
    simbols = hexdigits
    string = ''
    for _ in range(random.randint(begin, end)):
        string += random.choice(simbols)
    return string


valid_hexdigits_password = random_letter_digits_string(8, 16)


def random_string_all_symbols(begin=1, end=30):
    simbols = hexdigits
    string = ''
    for _ in range(random.randint(begin, end)):
        string += random.choice(simbols)
    return string


invalid_length_backup_code = random_string_all_symbols(1, 11)


def random_twelve_symbols(begin=12, end=12):
    simbols = hexdigits
    string = ''
    for _ in range(random.randint(begin, end)):
        string += random.choice(simbols)
    return string


valid_length_backup_code = random_twelve_symbols()


def get_list_of_six_codes():
    codes = []
    for i in range(6):
        codes.append(random_twelve_symbols())
    return codes


list_of_six_backup_codes = get_list_of_six_codes()


def random_digits_string(begin=6, end=6):
    simbols = digits
    string = ''
    for _ in range(random.randint(begin, end)):
        string += random.choice(simbols)
    return string


verification_code = random_digits_string(6, 6)


def get_list_of_verification_codes():
    verification_codes = []
    for i in range(5):
        verification_codes.append(random_digits_string())
    return verification_codes


print(get_list_of_verification_codes())


def split_verification_codes():
    list_of_codes = get_list_of_verification_codes()
    new_list = []
    for i in list_of_codes:
        split_code = list(i)
        new_list.append(split_code)

    return new_list


list_with_verification_codes = split_verification_codes()
