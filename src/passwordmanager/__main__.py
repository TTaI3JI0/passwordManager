"""Точка входа в менеджер паролей."""

import getpass

from passwordmanager.manager import PasswordManager


def main() -> None:
    """Предлагает CLI и обрабатывает входные данные от пользователя."""
    manager = PasswordManager("passwords.json")

    while True:
        if manager.is_initialized():
            if manager.unlock(
                getpass.getpass("Введите мастер-пароль: ", echo_char="*")
            ):
                print("Успешный вход!")
                break
            else:
                print("Неверный мастер-пароль!")
        else:
            try:
                manager.init_master(
                    getpass.getpass("Придумайте мастер-пароль: ", echo_char="*")
                )
            except FileExistsError:
                print("Ошибка: файл хранилища уже существует!")
            except Exception as e:
                print(f"Ошибка при создании хранилища: {e}")

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
            while True:
                print("1. Создать новый пароль")
                print("2. Сгенерировать пароль")
                choice2 = input("Выберите действие: ")
                if choice2 == "1":
                    pwd = getpass.getpass("Введите пароль: ", echo_char="*")
                    break
                elif choice2 == "2":
                    pwd = manager.generate_password()
                    break
                else:
                    print("Неверный ввод, попробуйте снова.")

            try:
                manager.add_entry(name, login, pwd)
                print(f"Запись для {name} добавлена!")
            except ValueError as e:
                print(f"Ошибка: {e}")
            except Exception as e:
                print(f"Не удалось добавить запись: {e}")

        elif choice == "2":
            print("\nСписок ресурсов, для которых сохранён пароль:")
            try:
                entries = manager.list_entries()
                for entry in entries:
                    print(f"- {entry}")
            except Exception as e:
                print(f"Не удалось получить список: {e}")

        elif choice == "3":
            name = input("Введите название ресурса: ")
            try:
                print(manager.get_entry(name))
            except Exception as e:
                print(f"Ошибка при поиске: {e}")

        elif choice == "4":
            name = input("Введите название ресурса для удаления: ")
            try:
                if name in manager.list_entries():
                    manager.delete_entry(name)
                    print(f"Запись {name} удалена.")
                else:
                    print(f"Запись {name} не найдена.")
            except Exception as e:
                print(f"Ошибка при удалении: {e}")

        elif choice == "0":
            print("Выход...")
            break
        else:
            print("Неверный ввод, попробуйте снова.")


if __name__ == "__main__":
    main()
