class UserEmailDoesNotExist(Exception):
    def __init__(self, message="Пользователя с такой почтой не существует"):
        self.message = message
        super().__init__(self.message)


class ResetTokenPasswordIncorrect(Exception):
    def __init__(self, message="Пароли в токене и в бд не совпадают"):
        self.message = message
        super().__init__(self.message)

    # def __call__(self, *args, **kwargs):


class InvalidSalt(Exception):
    def __init__(self, message="InvalidSalt"):
        self.message = message
        super().__init__(self.message)


class EmailExist(Exception):
    def __init__(self, message="Email already exist"):
        self.message = message
        super().__init__(self.message)


class LoginExist(Exception):
    def __init__(self, message="Login already exist"):
        self.message = message
        super().__init__(self.message)


class UnexpectedError(Exception):
    def __init__(self, message="UnexpectedError! Already fixing!"):
        self.message = message
        super().__init__(self.message)


class MissUserIdOrEmail(Exception):
    def __init__(self, message="Missing user id or user email!"):
        self.message = message
        super().__init__(self.message)
