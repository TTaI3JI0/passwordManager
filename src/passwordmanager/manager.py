"""Модуль управления паролями."""

import json
import pathlib


class PasswordManager:
    """Сущность менеджера."""

    def __init__(self, file_path: str) -> None:
        """Инициализирует менеджер и получает путь к файлу с паролями."""
        self.path = pathlib.Path(file_path)

    def is_initialized(self) -> bool:
        """Проверка наличия файла методом из модуля pathlib."""
        return self.path.exists()

    def init_master(self, master_password: str) -> None:
        """Создаёт уникальный json-файл с паролями и записывает в него мастер-пароль."""
        with open(self.path, "x") as file:
            json.dump({"masterPassword": master_password}, file, indent=4)

    def unlock(self, password: str) -> bool:
        """Проверяет мастер-пароль."""
        if not self.is_initialized():
            return False

        with open(self.path, encoding="utf-8") as file:
            data = json.load(file)

        saved_password = data["masterPassword"]
        return bool(saved_password == password)

    def add_entry(self, name: str, login: str, pwd: str) -> None:
        """Добавляет новый пароль в хранилище."""
        pass

    def list_entries(self) -> list[str]:
        """Вовзращает список ресурсов, для которые сохранен логи и пароль."""
        return []

    def get_entry(self, name: str) -> str:
        """Возвращает логин и пароль от ресурса по имени."""
        return ""

    def delete_entry(self, name: str) -> None:
        """Удаляет пароль из хранилища по названию ресурса."""
        pass

    def _persist(self) -> None:
        """Сохраняет файл с паролями."""
        pass

    def _load(self) -> dict[str, str]:
        """Загружает файл с паролями."""
        return {}
