class APIError(RuntimeError):
    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(f"Euron API error {status_code}: {detail}")
        self.status_code = status_code
        self.detail = detail