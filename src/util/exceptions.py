__author__ = 'arkady'

class UserProgramError(Exception):
    pass

class RunError(UserProgramError):
    def __init__(self, val):
        self.value = val

    def __str__(self):
        return str(self.value)

class TimeOutError(UserProgramError):
    def __init__(self, val):
        self.value = val

    def __str__(self):
        return str(self.value)


class BuildFailedException(UserProgramError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

