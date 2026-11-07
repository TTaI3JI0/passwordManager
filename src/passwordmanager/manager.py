"""Модуль управления паролями."""

import base64
import hashlib
import json
import pathlib
import secrets
import string

from cryptography.fernet import Fernet


class PasswordManager:
    """Сущность менеджера."""

    def __init__(self, file_path: str) -> None:
        """Инициализирует менеджер и получает путь к файлу с паролями."""
        self.path = pathlib.Path(file_path)
        self.key: bytes | None = None

    def is_initialized(self) -> bool:
        """Проверка наличия файла методом из модуля pathlib."""
        return self.path.exists()

    def init_master(self, master_password: str) -> None:
        """Создаёт уникальный json-файл с паролями и записывает в него мастер-пароль."""
        salt = secrets.token_bytes(16)
        pwd_hash = hashlib.pbkdf2_hmac(
            "sha256", master_password.encode(), salt, 200_000
        ).hex()

        data = {"masterHash": pwd_hash, "salt": salt.hex(), "entries": {}}

        with open(self.path, "x", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def unlock(self, password: str) -> bool:
        """Проверяет мастер-пароль."""
        if not self.is_initialized():
            return False

        with open(self.path, encoding="utf-8") as file:
            data = json.load(file)

        salt = bytes.fromhex(data["salt"])
        actual_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt, 200_000
        ).hex()

        if actual_hash != data["masterHash"]:
            return False

        self.key = base64.urlsafe_b64encode(bytes.fromhex(actual_hash))
        return True

    def add_entry(self, name: str, login: str, pwd: str) -> None:
        """Добавляет новый пароль в хранилище."""
        if self.key is None:
            raise ValueError("Сначала нужно войти (unlock)")

        data = self._load()
        fernet = Fernet(self.key)
        encrypted_pwd = fernet.encrypt(pwd.encode()).decode()

        data["entries"][name] = {"login": login, "pwd": encrypted_pwd}  # type: ignore
        self._persist(data)

    def list_entries(self) -> list[str]:
        """Возвращает список ресурсов, для которых сохранен логин и пароль."""
        data = self._load()
        return list(data["entries"].keys())  # type: ignore

    def get_entry(self, name: str) -> str:
        """Возвращает логин и пароль от ресурса по имени."""
        if self.key is None:
            raise ValueError("Сначала нужно войти (unlock)")

        data = self._load()
        entries = data["entries"]
        if name in entries:  # type: ignore
            entry = entries[name]  # type: ignore
            fernet = Fernet(self.key)
            decrypted_pwd = fernet.decrypt(entry["pwd"].encode()).decode()
            return f"Логин: {entry['login']}, Пароль: {decrypted_pwd}"
        return "Запись не найдена."

    def delete_entry(self, name: str) -> None:
        """Удаляет пароль из хранилища по названию ресурса."""
        data = self._load()
        if name in data["entries"]:  # type: ignore
            del data["entries"][name]  # type: ignore
            self._persist(data)

    def generate_password(self) -> str:
        """Генерирует случайный пароль."""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        return "".join(secrets.choice(alphabet) for _ in range(16))

    def _persist(self, data: dict[str, object]) -> None:
        """Сохраняет файл с паролями."""
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def _load(self) -> dict[str, object]:
        """Загружает файл с паролями."""
        with open(self.path, encoding="utf-8") as file:
            return json.load(file)  # type: ignore
