import re

def is_password_secure(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "Пароль должен быть минимум 8 символов!"

    if not re.search(r"[a-z]", password):
        return False, "Добавьте хотя бы одну строчную букву!"

    if not re.search(r"[A-Z]", password):
        return False, "Добавьте хотя бы одну заглавную букву!"

    if not re.search(r"[0-9]", password):
        return False, "Добавьте хотя бы одну цифру!"

    if not re.search(r"[\W_]", password):
        return False, "Добавьте хотя бы один спецсимвол!"
    return True, None