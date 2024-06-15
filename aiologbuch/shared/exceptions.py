class AIOLogbuchException(Exception): ...


class WouldDeadlock(AIOLogbuchException):
    def __init__(self):
        message = (
            "Can not acquire the lock because it is currently being used by another "
            "coroutine"
        )
        super().__init__(message)
