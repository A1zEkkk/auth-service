def normalize_number(number: str) -> str:
    normalized_number = ""
    for i in number:
        if i not in "+-() ":
            normalized_number += i

    return normalized_number
