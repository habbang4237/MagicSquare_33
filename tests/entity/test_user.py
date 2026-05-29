"""Domain Track tests for User entity (no mocks)."""

from __future__ import annotations

import pytest

from entity.errors import DomainError
from entity.user import User
from entity.user_constants import (
    MAX_DISPLAY_NAME_LENGTH,
    MAX_USER_ID_LENGTH,
)


class TestUserCreate:
    """Tests for ``User.create`` factory."""

    # Test-ID: U-ENT-01 — valid user creation
    def test_create_valid_user(self) -> None:
        """Valid inputs produce a frozen User with normalized fields."""
        # Arrange
        raw_id = "  user-001  "
        raw_name = "  Alice  "
        raw_email = "  Alice@Example.COM  "

        # Act
        user = User.create(raw_id, raw_name, raw_email)

        # Assert
        assert user.user_id == "user-001"
        assert user.display_name == "Alice"
        assert user.email == "alice@example.com"
        assert user.is_active is True

    def test_create_inactive_user(self) -> None:
        """is_active=False is preserved at creation."""
        # Arrange & Act
        user = User.create("u1", "Bob", "bob@test.com", is_active=False)

        # Assert
        assert user.is_active is False


class TestUserIdValidation:
    """Tests for user_id invariants."""

    def test_empty_user_id_raises(self) -> None:
        """Blank user_id violates INVALID_USER_ID."""
        # Arrange & Act & Assert
        with pytest.raises(DomainError) as exc_info:
            User.create("   ", "Alice", "alice@test.com")

        assert exc_info.value.code == "INVALID_USER_ID"

    def test_user_id_too_long_raises(self) -> None:
        """user_id longer than MAX_USER_ID_LENGTH is rejected."""
        # Arrange
        too_long_id = "x" * (MAX_USER_ID_LENGTH + 1)

        # Act & Assert
        with pytest.raises(DomainError) as exc_info:
            User.create(too_long_id, "Alice", "alice@test.com")

        assert exc_info.value.code == "INVALID_USER_ID"


class TestDisplayNameValidation:
    """Tests for display_name invariants."""

    def test_empty_display_name_raises(self) -> None:
        """Blank display_name violates INVALID_DISPLAY_NAME."""
        # Arrange & Act & Assert
        with pytest.raises(DomainError) as exc_info:
            User.create("u1", "  ", "alice@test.com")

        assert exc_info.value.code == "INVALID_DISPLAY_NAME"

    def test_display_name_too_long_raises(self) -> None:
        """display_name longer than MAX_DISPLAY_NAME_LENGTH is rejected."""
        # Arrange
        too_long_name = "n" * (MAX_DISPLAY_NAME_LENGTH + 1)

        # Act & Assert
        with pytest.raises(DomainError) as exc_info:
            User.create("u1", too_long_name, "alice@test.com")

        assert exc_info.value.code == "INVALID_DISPLAY_NAME"


class TestEmailValidation:
    """Tests for email invariants."""

    @pytest.mark.parametrize(
        "invalid_email",
        [
            "not-an-email",
            "@nodomain.com",
            "local@",
            "local@domain",
        ],
    )
    def test_invalid_email_format_raises(self, invalid_email: str) -> None:
        """Malformed email raises INVALID_EMAIL."""
        # Arrange & Act & Assert
        with pytest.raises(DomainError) as exc_info:
            User.create("u1", "Alice", invalid_email)

        assert exc_info.value.code == "INVALID_EMAIL"


class TestUserBehavior:
    """Tests for entity behavior beyond creation."""

    def test_user_is_immutable(self) -> None:
        """Frozen User cannot be mutated."""
        # Arrange
        user = User.create("u1", "Alice", "alice@test.com")

        # Act & Assert
        with pytest.raises(AttributeError):
            user.display_name = "Eve"  # type: ignore[misc]

    def test_deactivate_returns_inactive_copy(self) -> None:
        """deactivate() returns new User without mutating original."""
        # Arrange
        active = User.create("u1", "Alice", "alice@test.com")

        # Act
        inactive = active.deactivate()

        # Assert
        assert active.is_active is True
        assert inactive.is_active is False
        assert inactive.user_id == active.user_id

    def test_equal_users_with_same_fields(self) -> None:
        """Two Users with identical fields compare equal."""
        # Arrange
        left = User.create("u1", "Alice", "alice@test.com")
        right = User.create("u1", "Alice", "alice@test.com")

        # Act & Assert
        assert left == right
