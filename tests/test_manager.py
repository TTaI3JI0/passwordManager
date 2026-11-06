"""Тесты для модуля manager."""
from passwordmanager.manager import PasswordManager


def test_unlock(tmp_path) -> None:
    """Проверяет вход по правильному и неправильному паролю."""
    test_file = tmp_path / "test_passwords.json"
    manager = PasswordManager(str(test_file))

    manager.init_master("secret123")

    assert manager.unlock("secret123") is True
    assert manager.unlock("wrong") is False