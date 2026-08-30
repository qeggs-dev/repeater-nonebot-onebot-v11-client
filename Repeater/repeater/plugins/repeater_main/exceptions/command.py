from .base import RepeaterException

class RepeaterCommandException(RepeaterException):
    """
    Repeater Command Base Exception
    """
    pass

class ProcessControlException(RepeaterCommandException):
    """
    Process Control Exception
    """
    pass

class BreakHandler(ProcessControlException):
    """
    Break Handler Exception
    """

    def __init__(self, code: int = 0, *args: object, **kwargs: object):
        self.code: int = code
        super().__init__(*args, **kwargs)

class BreakWithErrorMessage(BreakHandler):
    """
    Break Handler Exception with Error Message
    """
    pass