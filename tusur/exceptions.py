class TimetableNotFound(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f"A search for `{message}` yielded no results.")


class StudentNotFound(Exception):
    def __init__(self, *args: object) -> None:
        message = " ".join(args)
        super().__init__(f"A search for `{message}` yielded no results.")


class AuthorizationFailed(Exception):
    def __init__(self) -> None:
        super().__init__("Authorization failed! " +
                         "Check your email and password.")


class TusurError(Exception):
    ...
