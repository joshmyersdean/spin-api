class InitialRequestError(Exception):
    """Exception raised for errors in the initial request."""

    def __init__(self, status_code: int) -> None:
        self.status_code: int = status_code
        self.message: str = f"Failed to get redirect URL. Status code: {status_code}"
        super().__init__(self.message)
