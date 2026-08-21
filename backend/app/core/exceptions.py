"""
Application-specific exceptions for Voryent AI Studio.
"""


class DuplicateEmailError(Exception):
    """Raised when attempting to register with an email that already exists."""

    def __init__(self, message: str = "Email is already registered."):
        self.message = message
        super().__init__(self.message)


class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid."""

    def __init__(self, message: str = "Invalid email or password."):
        self.message = message
        super().__init__(self.message)


class InactiveUserError(Exception):
    """Raised when a valid user attempts to log in but the account is inactive."""

    def __init__(self, message: str = "User account is inactive."):
        self.message = message
        super().__init__(self.message)
