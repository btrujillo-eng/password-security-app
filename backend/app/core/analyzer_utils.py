from schemas import PasswordBase

import re

async def get_capital_letter(password: PasswordBase) -> bool:
    """
    Returns True if the password contains at least one capital letter.
    Otherwise, returns False.
    """
    return bool(re.search(r"[A-Z]", password.password))

async def get_lowercase_letter(password: PasswordBase) -> bool:
    """
    Returns True if the password contains at least one lowercase letter.
    Otherwise, returns False.
    """
    return bool(re.search(r"[a-z]", password.password))

async def get_special_character(password: PasswordBase) -> bool:
    """
    Return True if the password contains at least one special character.
    Otherwise, returns False.
    """
    return bool(re.search(r"[^\w\s]", password.password))

async def get_minimum_length(password: PasswordBase, length: int = 8) -> bool:
    """
    Returns True if the password has a minimum secure length.
    Otherwise, returns False.
    """
    return length <= len(password.password)

async def get_descending_sequence(password: PasswordBase) -> bool:
    """
    Returns True if the password contains a descending sequence of least three characters.
    Otherwise, returns False.
    """
    for i in range(len(password.password) - 2):
        character_1 = ord(password.password[i])
        character_2 = ord(password.password[i + 1])
        character_3 = ord(password.password[i + 2])
            
        if character_2 == character_1 - 1 and character_3 == character_2 - 1:
            return True
        
    return False

async def get_ascending_sequence(password: PasswordBase) -> bool:
    """
    Returns True if the password contains an ascending sequence of at least three characters.
    Otherwise, returns False.
    """
    for i in range(len(password.password) - 2):
        character_1 = ord(password.password[i])
        character_2 = ord(password.password[i + 1])
        character_3 = ord(password.password[i + 2])
            
        if character_2 == character_1 + 1 and character_3 == character_2 + 1:
            return True
            
    return False

async def get_numbers(password: PasswordBase, minimum_quantity: int = 3) -> bool:
    """
    Return True if the password contains at least three numbers.
    Otherwise, return False.
    """
    numbers = re.finditer(r"\d", password.password)
    try:
        for _ in range(minimum_quantity):
            next(numbers)
        return True
    except StopIteration:
        return False