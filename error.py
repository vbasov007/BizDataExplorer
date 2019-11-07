# definition for Error type
class Error:
    def __init__(self, val):
        if isinstance(val, Exception):
            self._val = str(val)
        elif isinstance(val, str):
            self._val = val
        elif val is None:
            self._val = None
        else:
            raise Exception('Error value must be a string, Exception or None')

    def __str__(self):
        if self._val is None:
            return ''
        else:
            return self._val

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        elif isinstance(other, str):
            return other == self._val
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __bool__(self):
        return self._val is not None
