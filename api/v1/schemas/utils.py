from core.exceptions.validation import AuthDataError

def normalize_phone_number(phone_number: str) -> str:
    total = 0
    normalize_number = ""
    for i in phone_number:
        if i.isdigit():
            normalize_number += i
            total += 1

    if total != 11:
        raise AuthDataError("Invalid lenght error")

    return normalize_number