"""User domain entity."""

from __future__ import annotations

import re
from dataclasses import dataclass

from entity.errors import DomainError
from entity.user_constants import (
    MAX_DISPLAY_NAME_LENGTH,
    MAX_EMAIL_LENGTH,
    MAX_USER_ID_LENGTH,
    MIN_DISPLAY_NAME_LENGTH,
    MIN_EMAIL_LENGTH,
    MIN_USER_ID_LENGTH,
)

_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True, slots=True)
class User:
    """Domain entity representing a puzzle solver account.

    Invariants:
        - ``user_id`` is non-empty after strip, length within configured bounds.
        - ``display_name`` is non-empty after strip, length within bounds.
        - ``email`` matches a minimal ``local@domain.tld`` pattern.
        - ``is_active`` defaults to ``True`` at creation.

    Attributes:
        user_id: Unique account identifier (opaque string).
        display_name: Human-readable name shown in the UI.
        email: Contact email address.
        is_active: Whether the account may interact with the system.
    """

    user_id: str
    display_name: str
    email: str
    is_active: bool = True

    @classmethod
    def create(
        cls,
        user_id: str,
        display_name: str,
        email: str,
        *,
        is_active: bool = True,
    ) -> User:
        """Create a validated ``User`` instance.

        Args:
            user_id: Unique account identifier.
            display_name: Display name for the user.
            email: Email address.
            is_active: Active flag; defaults to ``True``.

        Returns:
            A frozen ``User`` satisfying all invariants.

        Raises:
            DomainError: If any invariant is violated.
        """
        normalized_id = cls._validate_user_id(user_id)
        normalized_name = cls._validate_display_name(display_name)
        normalized_email = cls._validate_email(email)
        return cls(
            user_id=normalized_id,
            display_name=normalized_name,
            email=normalized_email,
            is_active=is_active,
        )

    @staticmethod
    def _validate_user_id(user_id: str) -> str:
        """Validate and normalize ``user_id``.

        Args:
            user_id: Raw identifier string.

        Returns:
            Stripped, valid user id.

        Raises:
            DomainError: If id is empty or out of bounds.
        """
        normalized = user_id.strip()
        length = len(normalized)
        if length < MIN_USER_ID_LENGTH or length > MAX_USER_ID_LENGTH:
            raise DomainError(
                code="INVALID_USER_ID",
                message=(
                    f"user_id length must be between "
                    f"{MIN_USER_ID_LENGTH} and {MAX_USER_ID_LENGTH}."
                ),
            )
        return normalized

    @staticmethod
    def _validate_display_name(display_name: str) -> str:
        """Validate and normalize ``display_name``.

        Args:
            display_name: Raw display name.

        Returns:
            Stripped, valid display name.

        Raises:
            DomainError: If name is empty or out of bounds.
        """
        normalized = display_name.strip()
        length = len(normalized)
        if length < MIN_DISPLAY_NAME_LENGTH or length > MAX_DISPLAY_NAME_LENGTH:
            raise DomainError(
                code="INVALID_DISPLAY_NAME",
                message=(
                    f"display_name length must be between "
                    f"{MIN_DISPLAY_NAME_LENGTH} and {MAX_DISPLAY_NAME_LENGTH}."
                ),
            )
        return normalized

    @staticmethod
    def _validate_email(email: str) -> str:
        """Validate and normalize ``email``.

        Args:
            email: Raw email string.

        Returns:
            Lowercased, valid email.

        Raises:
            DomainError: If email format or length is invalid.
        """
        normalized = email.strip().lower()
        length = len(normalized)
        if length < MIN_EMAIL_LENGTH or length > MAX_EMAIL_LENGTH:
            raise DomainError(
                code="INVALID_EMAIL",
                message=(
                    f"email length must be between "
                    f"{MIN_EMAIL_LENGTH} and {MAX_EMAIL_LENGTH}."
                ),
            )
        if not _EMAIL_PATTERN.match(normalized):
            raise DomainError(
                code="INVALID_EMAIL",
                message="email must match local@domain.tld format.",
            )
        return normalized

    def deactivate(self) -> User:
        """Return a copy of this user marked inactive.

        Returns:
            New ``User`` with ``is_active=False``.
        """
        return User(
            user_id=self.user_id,
            display_name=self.display_name,
            email=self.email,
            is_active=False,
        )
