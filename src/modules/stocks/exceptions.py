class MissingTransactionIdError(Exception):
    def __init__(self, message="InvalidSalt"):
        self.message = message
        super().__init__(self.message)
