class ValidationError(Exception):
    """
    Error to signal something does not pass a validation check.
    """
    pass


class BytecodeMismatch(Exception):
    """
    Error to signal that package bytecode does not match deployed bytecode.
    """
    pass
