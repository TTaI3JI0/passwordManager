"""Точка входа в менеджер паролей."""
import getpass
import json


def init_master(master_password: str) -> None:
    """Создаёт уникальный json-файл с паролями и записывает в него мастер-пароль."""
    with open("passwords.json", "x") as file:
        json.dump({"masterPassword": master_password}, file, indent=4)


def main() -> None:
    """Предлагает CLI и обрабатывает входные данные от пользователя."""
    try:
        with open("passwords.json", "r+") as file:
            passwords = json.load(file)
            print(passwords)

    except FileNotFoundError:
        init_master(getpass.getpass("Введите мастер-пароль: ", echo_char="*"))


if __name__ == "__main__":
    main()
