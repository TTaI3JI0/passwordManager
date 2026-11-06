"""Точка входа в менеджер паролей."""

import getpass

from passwordmanager.manager import PasswordManager


def main() -> None:
    """Предлагает CLI и обрабатывает входные данные от пользователя."""
    manager = PasswordManager("passwords.json")

    while True:
        if manager.is_initialized():
            if manager.unlock(getpass.getpass("Введите мастер-пароль: ",
                                              echo_char="*")):
                print("Успешный вход!")
                break
            else:
                print("Неверный мастер-пароль!")
        else:
            manager.init_master(
                getpass.getpass("Придумайте мастер-пароль: ", echo_char="*")
            )

    while True:
        print("\n--- Меню ---")
        print("1. Добавить пароль")
        print("2. Показать список")
        print("3. Найти пароль")
        print("4. Удалить пароль")
        print("0. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            name = input("Введите название ресурса: ")
            login = input("Введите логин: ")
            pwd = getpass.getpass("Введите пароль: ", echo_char="*")
            manager.add_entry(name, login, pwd)
            print(f"Запись для {name} добавлена!")

        elif choice == "2":
            print("Список ресурсов, для которых сохранён пароль:")
            entries = manager.list_entries()
            for entry in entries:
                print(f"- {entry}")

        elif choice == "3":
            name = input("Введите название ресурса: ")
            print(manager.get_entry(name))

        elif choice == "4":
            name = input("Введите название ресурса для удаления: ")
            manager.delete_entry(name)
            print(f"Запись {name} удалена.")

        elif choice == "0":
            print("Выход...")
            break
        else:
            print("Неверный ввод, попробуйте снова.")


if __name__ == "__main__":
    main()
