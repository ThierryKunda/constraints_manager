class DataNotProvided(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


class SchemaNotProvided(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)