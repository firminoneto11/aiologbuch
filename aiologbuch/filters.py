class Filter:
    def __init__(self, level: int):
        self._level = level

    @property
    def level(self):
        return self._level

    def filter(self, level: int):
        return level >= self.level


class ExclusiveFilter(Filter):
    def filter(self, level: int):
        return level == self.level
