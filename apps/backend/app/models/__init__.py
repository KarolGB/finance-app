#Here you import all the models so later you can use alembic to autogenerate migrations
from .User import User
from .RefreshToken import RefreshToken

__all__ = ["User", "RefreshToken"]