import re


class ValidStr:
    """ validStr class checks if a given string is printable."""

    def __init__(self, txt):
        self.txt = txt

    @property
    def txt(self):
        return self.__txt

    @txt.setter
    def txt(self, txt):
        if isinstance(txt, str):
            if txt and txt.isprintable():
                self.__txt = txt.strip()
            else:
                self.__txt = None
        else:
            self.__txt = None

    def __eq__(self, other):
        if isinstance(other, ValidStr):
            return self.txt == other.txt
        else:
            return False


class ValidEmail(ValidStr):
    """ validPEmail class checks if a given email address fulfills
    generally accepted requirements for creating an email address.
    """

    def __init__(self, email):
        super().__init__(email)
        self.email = email

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.txt = email
        if self.txt and re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            self.__email = email
        else:
            self.__email = None


class ValidPassword(ValidStr):
    """ validPassword class checks if a given password fulfills conditions
    given below:
        1. Contains at least one number.
        2. Contains at least one uppercase and lowercsae character.
        3. Contains at least one special symbol !@#$%^&*()-_+={}|:;<>,./~`.
        4. It's length is between [8, 16].
    """

    def __init__(self, password):
        super().__init__(password)
        self.password = password

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.txt = password
        if self.txt and re.fullmatch(r"^.*(?=.{8,16})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()-_+={}|:;<>,.~`.]).*$", password):
            self.__password = password
        else:
            self.__password = None
