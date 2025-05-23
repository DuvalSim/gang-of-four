class InvalidRequestException(Exception):
    """Exception raised for invalid requests."""

    def __init__(self, message="Invalid request"):
        self.message = message
        super().__init__(self.message)
