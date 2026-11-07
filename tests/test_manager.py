"""Тесты для модуля manager."""

from pathlib import Path

from passwordmanager.manager import PasswordManager


def test_unlock(tmp_path: Path) -> None:
    """Проверяет вход по правильному и неправильному паролю."""
    test_file = tmp_path / "test_passwords.json"
    manager = PasswordManager(str(test_file))

    manager.init_master("secret123")

    assert manager.unlock("secret123") is True
    assert manager.unlock("wrong") is False


def test_add_and_get_entry(tmp_path: Path) -> None:
    """Проверяет добавление и получение записи с шифрованием."""
    test_file = tmp_path / "test_passwords.json"
    manager = PasswordManager(str(test_file))

    manager.init_master("secret123")
    manager.unlock("secret123")

    manager.add_entry("vk.ru", "user123", "pass456")

    result = manager.get_entry("vk.ru")
    assert "user123" in result
    assert "pass456" in result


def test_delete_entry(tmp_path: Path) -> None:
    """Проверяет удаление записи из хранилища."""
    test_file = tmp_path / "test_passwords.json"
    manager = PasswordManager(str(test_file))

    manager.init_master("secret123")
    manager.unlock("secret123")

    manager.add_entry("vk.ru", "user123", "pass456")
    assert "vk.ru" in manager.list_entries()

    manager.delete_entry("vk.ru")

    assert "vk.ru" not in manager.list_entries()
    assert manager.get_entry("vk.ru") == "Запись не найдена."


def test_generate_password() -> None:
    """Проверяет, что генератор создаёт правильный пароль."""
    manager = PasswordManager("dummy.json")  # путь не важен для этого теста
    pwd = manager.generate_password()

    assert len(pwd) == 16
    assert isinstance(pwd, str)
