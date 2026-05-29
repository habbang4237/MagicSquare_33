"""Entity layer: domain data and invariants."""

from entity.errors import DomainError
from entity.user import User

__all__ = ["DomainError", "User"]
