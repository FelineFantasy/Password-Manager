import random
import string
import os
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"

# Загрузка или генерация ключа шифрования
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        key = f.read()
else:
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

cipher = Fernet(key)

# Создание файла для паролей, если он не существует
if not os.path.exists("password.txt"):
    with open("password.txt", "w", encoding="utf-8") as f:
        f.write("")


def separator():
    """Выводит разделительную линию."""
    print("=" * 50)


def action_save_password():
    """Сохраняет пароль в зашифрованном виде."""
    separator()
    title = input("От какого приложения данный пароль?: ")
    password = input("Введите пароль: ")
    encrypted = cipher.encrypt(password.encode()).decode()
    with open("password.txt", "a", encoding="utf-8") as f:
        f.write(f"{title}|{encrypted}\n")
    separator()
    print("Пароль сохранён!")


def action_show_password():
    """Показывает все сохранённые пароли."""
    try:
        with open("password.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not lines:
            separator()
            print("Нет сохранённых паролей")
            return
        separator()
        for i, line in enumerate(lines, 1):
            try:
                title, enc_password = line.strip().split("|")
                decrypted = cipher.decrypt(enc_password.encode()).decode()
                print(f"{i}. {title}: {decrypted}")
            except Exception:
                print(f"{i}. Ошибка: {line.strip()}")
    except FileNotFoundError:
        separator()
        print("Файл с паролями не найден")


def action_generate_password():
    """Генерирует случайный пароль заданной длины."""
    separator()
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    try:
        length = int(input("Введите длину пароля: "))
        result = ''.join(random.choices(chars, k=length))
        separator()
        print(f"Результат: {result}")
    except ValueError:
        print("Введите число!")


def action_check_strength():
    """Проверяет надёжность пароля."""
    separator()
    password = input("Введите пароль: ")
    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c in "!@#$%^&*" for c in password):
        score += 1
    separator()
    match score:
        case 5:
            print("Очень надёжный")
        case 4:
            print("Надёжный")
        case 3:
            print("Средний")
        case 2:
            print("Низкая надёжность")
        case _:
            print("Очень ненадёжный")


def main():
    """Главный цикл программы."""
    while True:
        separator()
        print("Менеджер паролей")
        print("0. Выйти")
        print("1. Сохранить пароль")
        print("2. Посмотреть пароли")
        print("3. Сгенерировать пароль")
        print("4. Проверить стойкость пароля")
        separator()

        choice = input("Выберите вариант: ")

        match choice:
            case "0":
                break
            case "1":
                action_save_password()
            case "2":
                action_show_password()
            case "3":
                action_generate_password()
            case "4":
                action_check_strength()
            case _:
                print("Неверный выбор")


if __name__ == "__main__":
    main()