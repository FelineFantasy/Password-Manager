import random
import string
import os
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"
PASSWORD_FILE = "password.txt"


def get_cipher():
    """Загружает или создаёт ключ шифрования."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    return Fernet(key)


def init_password_file():
    """Создаёт файл для паролей, если он не существует."""
    if not os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "w", encoding="utf-8") as f:
            f.write("")


def clear_console():
    """Очищает консоль."""
    os.system("cls" if os.name == "nt" else "clear")


def wait_and_clear():
    """Ожидает нажатия Enter и очищает консоль."""
    input("\nДля выхода в меню нажмите Enter...")
    clear_console()


def load_passwords():
    """Загружает все пароли из файла."""
    try:
        with open(PASSWORD_FILE, "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        return []


def save_passwords(lines):
    """Сохраняет пароли в файл."""
    with open(PASSWORD_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)


def get_services_list(lines):
    """Возвращает список сервисов из строк файла."""
    services = []
    for line in lines:
        try:
            title = line.strip().split("|")[0]
            services.append(title)
        except Exception:
            pass
    return services


def show_services_menu(lines):
    """Показывает нумерованный список сервисов."""
    services = get_services_list(lines)
    for i, title in enumerate(services, 1):
        print(f"{i}. {title}")
    return services


def get_user_choice(max_choice):
    """Получает от пользователя номер выбора."""
    try:
        choice = int(input("Введите номер: "))
        if 1 <= choice <= max_choice:
            return choice
        print("Неверный номер")
    except ValueError:
        print("Введите число!")
    return None


def generate_random_password(length=12):
    """Генерирует случайный пароль заданной длины."""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choices(chars, k=length))


def get_password_from_user():
    """Запрашивает у пользователя пароль (вручную или генерирует)."""
    print("1. Ввести пароль вручную")
    print("2. Сгенерировать пароль автоматически")
    choice = input("Выберите вариант (1 или 2): ").strip()

    if choice == "2":
        try:
            length = int(input("Введите длину пароля (по умолчанию 12): ") or "12")
            password = generate_random_password(length)
        except ValueError:
            print("Неверная длина, будет использован пароль длиной 12 символов")
            password = generate_random_password(12)
        print(f"Сгенерированный пароль: {password}")
    else:
        password = input("Введите пароль: ")

    return password


def action_save_password(cipher):
    """Сохраняет пароль в зашифрованном виде."""
    print("=" * 50)
    title = input("От какого приложения данный пароль?: ")
    password = get_password_from_user()

    encrypted = cipher.encrypt(password.encode()).decode()

    with open(PASSWORD_FILE, "a", encoding="utf-8") as f:
        f.write(f"{title}|{encrypted}\n")

    print("=" * 50)
    print("Пароль сохранён!")


def action_update_password(cipher):
    """Обновляет существующий пароль."""
    print("=" * 50)
    lines = load_passwords()

    if not lines:
        print("Нет сохранённых паролей")
        return

    print("Сохранённые сервисы:")
    services = show_services_menu(lines)
    choice = get_user_choice(len(services))

    if not choice:
        return

    old_title = services[choice - 1]
    old_enc_password = lines[choice - 1].strip().split("|")[1]

    try:
        old_password = cipher.decrypt(old_enc_password.encode()).decode()
        print(f"Старый пароль для '{old_title}': {old_password}")
    except Exception:
        print("Не удалось расшифровать старый пароль")

    new_password = get_password_from_user()
    encrypted = cipher.encrypt(new_password.encode()).decode()
    lines[choice - 1] = f"{old_title}|{encrypted}\n"
    save_passwords(lines)

    print("=" * 50)
    print(f"Пароль для '{old_title}' обновлён!")


def action_delete_password():
    """Удаляет пароль из файла."""
    print("=" * 50)
    lines = load_passwords()

    if not lines:
        print("Нет сохранённых паролей")
        return

    print("Сохранённые сервисы:")
    services = show_services_menu(lines)
    choice = get_user_choice(len(services))

    if not choice:
        return

    deleted_title = services[choice - 1]
    del lines[choice - 1]
    save_passwords(lines)

    print("=" * 50)
    print(f"Пароль для '{deleted_title}' успешно удалён!")


def action_show_password(cipher):
    """Показывает все сохранённые пароли."""
    lines = load_passwords()

    if not lines:
        print("=" * 50)
        print("Нет сохранённых паролей")
        return

    print("=" * 50)
    for i, line in enumerate(lines, 1):
        try:
            title, enc_password = line.strip().split("|")
            decrypted = cipher.decrypt(enc_password.encode()).decode()
            print(f"{i}. {title}: {decrypted}")
        except Exception:
            print(f"{i}. Ошибка: {line.strip()}")


def action_generate_password():
    """Генерирует случайный пароль заданной длины."""
    print("=" * 50)
    try:
        length = int(input("Введите длину пароля: "))
        result = generate_random_password(length)
        print("=" * 50)
        print(f"Результат: {result}")
    except ValueError:
        print("Введите число!")


def check_password_strength(password):
    """Проверяет надёжность пароля и возвращает оценку."""
    checks = [
        len(password) >= 8,
        any(c.isdigit() for c in password),
        any(c.isupper() for c in password),
        any(c.islower() for c in password),
        any(c in "!@#$%^&*" for c in password)
    ]
    return sum(checks)


def action_check_strength():
    """Проверяет надёжность пароля."""
    print("=" * 50)
    password = input("Введите пароль: ")
    score = check_password_strength(password)

    strength_levels = {
        5: "Очень надёжный",
        4: "Надёжный",
        3: "Средний",
        2: "Низкая надёжность"
    }
    print("=" * 50)
    print(strength_levels.get(score, "Очень ненадёжный"))


def main():
    """Главный цикл программы."""
    clear_console()
    init_password_file()
    cipher = get_cipher()

    menu_actions = {
        "1": lambda: action_save_password(cipher),
        "2": lambda: action_update_password(cipher),
        "3": action_delete_password,
        "4": lambda: action_show_password(cipher),
        "5": action_generate_password,
        "6": action_check_strength,
    }

    while True:
        print("Менеджер паролей")
        print("=" * 50)
        print("0. Выйти")
        print("1. Сохранить пароль")
        print("2. Обновить пароль")
        print("3. Удалить пароль")
        print("4. Посмотреть пароли")
        print("5. Сгенерировать пароль")
        print("6. Проверить стойкость пароля")
        print("=" * 50)

        choice = input("Выберите вариант: ")

        if choice == "0":
            break

        action = menu_actions.get(choice)
        if action:
            action()
        else:
            print("Неверный выбор")

        wait_and_clear()


if __name__ == "__main__":
    main()