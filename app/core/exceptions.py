class ResourceNotFound(Exception):
    """Raised when a requested resource does not exist."""
    pass

class UnauthorizedAccess(Exception):
    """Raised when user is not authorized."""
    pass

class FirebaseOperationError(Exception):
    """Raised when a Firebase operation fails."""
    pass