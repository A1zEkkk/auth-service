from core.exceptions.base import InvalidPhoneNumberError

def normalize_phone_number(phone_number: str) -> str:
    total = 0
    normalize_number = ""
    for i in phone_number:
        if i.isdigit():
            normalize_number += i
            total += 1

    if total != 11:
        raise InvalidPhoneNumberError

    return normalize_number