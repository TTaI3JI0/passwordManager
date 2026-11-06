"""Точка входа в менеджер паролей."""

import getpass

from passwordmanager.manager import PasswordManager


def main() -> None:
    """Предлагает CLI и обрабатывает входные данные от пользователя."""
    manager = PasswordManager("passwords.json")

    if manager.is_initialized():
        if manager.unlock(getpass.getpass("Введите мастер-пароль: ", echo_char="*")):
            print("Успешный вход!")
        else:
            print("Неверный мастер-пароль!")
    else:
        manager.init_master(getpass.getpass("Придумайте мастер-пароль: ",
                                            echo_char="*"))


if __name__ == "__main__":
    main()
