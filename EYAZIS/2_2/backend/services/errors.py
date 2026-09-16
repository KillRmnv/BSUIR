class AppError(Exception):
    """Base exception for all application errors."""
    status_code = 500

    def __init__(self, message="Internal server error"):
        self.message = message
        super().__init__(self.message)


class ValidationError(AppError):
    status_code = 400


class NotFoundError(AppError):
    status_code = 404


class ServiceError(AppError):
    status_code = 500
