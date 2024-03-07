"""Password Validation Module

This module provides validators for checking the strength and security of given passwords.
Validators include checks for length, presence of uppercase and lowercase characters, 
digits, special characters, and verification against the Have I Been Pwned database.

Note:
    Before using IfPownedValidator, make sure to review and comply with 
    the Have I Been Pwned API terms of use: https://haveibeenpwned.com/API/Consuming
    IfPownedValidator connects to the Have I Been Pwned API
    to check if the password has been compromised.
    Remember not to publicly share your real password, and always keep it safe.
"""

from abc import ABC, abstractmethod
from hashlib import sha1
from requests import get


class Validator(ABC):
    """Interface for validators"""
    @abstractmethod
    def __init__(self, text) -> None:
        """Force to impement __init__ method"""

    @abstractmethod
    def is_valid(self):
        """Force to impement is_valid method"""



class LengthValidator(Validator):
    """Checking the length of given text."""
    def __init__(self, text) -> None:
        self.text = text

    def is_valid(self):
        """Check if the length of the passowrd is valide.

        Raises:
            ValidationError: password is not valide 
            because it is shorter than 8 characters lenght.

        Returns:
            bool: lenght is correct.
        """
        if len(self.text) >= 8:
            return False
        message = 'Password must contain at least 8 characters. '
        return message

class DigitValidator(Validator):
    """Checking presence of at least one digit in a given text."""
    def __init__(self, text) -> None:
        self.text = text

    def is_valid(self):
        """Check if the password contain digit and is valid.

        Raises:
            ValidationError: password is not valide
            becuase it does not contain any digit.

        Returns:
            bool: text contain digit .
        """
        digit = sum(1 for char in self.text if char.isdigit())
        if  digit > 0:
            return False

        message = 'Password must contain at least on digit. '
        return message
        

class SpecialCharValidator(Validator):
    """Checking presence of at least one special character in a given text."""
    def __init__(self, text) -> None:
        self.text = text

    def is_valid(self):
        """Check if the password contain special character and is valid.

        Raises:
            ValidationError: password is not valide
            becuase it does not contain any special character.

        Returns:
            bool: passowrd contain special character.
        """
        special = sum(1 for char in self.text if char.isascii() and not char.isalnum())
        if special > 0:
            return False

        message = 'Password must contain at least on special character. '
        return message


class UpperCharValidator(Validator):
    """Checking presence of at least one upper character in a given text."""
    def __init__(self, text) -> None:
        self.text = text

    def is_valid(self):
        """Check if the password contain uppercase character and is valid.

        Raises:
            ValidationError: password is not valide
            becuase it does not contain any uppercase character.

        Returns:
            bool: text contain uppercase character.
        """
        capital = sum(1 for char in self.text if char.isupper())
        if capital > 0:
            return False
        
        message = 'Password must contain at least one capital letter. '
        return message

class LowerCharValidator(Validator):
    """Checking presence of at least one lowercase character in a given text."""
    def __init__(self, text) -> None:
        self.text = text

    def is_valid(self):
        """Check if the password contain lowercase character and is valid.

        Raises:
            ValidationError: password is not valide
            becuase it does not contain any lowercase cahracter.

        Returns:
            bool: text contain lwoercase character.
        """
        lower = sum(1 for char in self.text if char.islower())
        if lower > 0:
            return False

        message = 'Password must contain at least one lowercase letter. '
        return message

class IfPownedValidator(Validator):
    """Connecting with pwnedpassowrds api and checking if password has leaked"""
    def __init__(self, password) -> None:
        self.password = password

    def is_valid(self):
        """Checking if password has leaked.

        Raises:
            ValidationError: password is not valide
            becuase it leaked in the past in hacker atack.

        Returns:
            bool: password is safe and it has not leaked.
        """
        my_hash = sha1(self.password.encode('utf-8')).hexdigest().upper()
        url = f'https://api.pwnedpasswords.com/range/{my_hash[:5]}'
        response_from_api = get(url, timeout=10)
        text = my_hash[5:]
        for line in response_from_api.text.splitlines():
            if text in line:
                message = 'Password has been leaked'
                return message

        return False


class PasswordValidator(Validator):
    """ Organizing all validators in one list and giving them the password. 
    Checking one by one if password is valid"""
    def __init__(self, password) -> None:
        self.password = password
        self.validators = [
            LengthValidator,
            SpecialCharValidator,
            UpperCharValidator,
            LowerCharValidator,
            DigitValidator,
            IfPownedValidator
        ]

    def is_valid(self):
        """Check all validator one by one.

        Returns:
            bool: if passowrd passed all validators. 
        """
        for class_name in self.validators:
            validator = class_name(self.password)
            if validator.is_valid():
                return(validator.is_valid())
        return False
