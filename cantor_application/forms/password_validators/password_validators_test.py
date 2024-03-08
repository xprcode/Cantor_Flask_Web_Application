import pytest
from password_validators import (
    DigitValidator,
    SpecialCharValidator,
    UpperCharValidator,
    LowerCharValidator,
    LengthValidator,
    IfPownedValidator,
    PasswordValidator
)


def test_digit_in_password():
    validator = DigitValidator('abc1')
    assert validator.is_valid() is False

def test_digit_in_password_negative():
    validator = DigitValidator('abc')
    assert validator.is_valid() == 'Password must contain at least on digit. ' 

def test_special_in_password():
    validator = SpecialCharValidator('.,/')
    assert validator.is_valid() is False

def test_special_in_password_negative():
    validator = SpecialCharValidator('abc1')
    assert validator.is_valid() == 'Password must contain at least on special character. ' 

def test_lenght_in_password():
    validator1 = LengthValidator('123456798') # password = 8
    assert validator1.is_valid() is False

def test_lenght_in_password_negative():
    validator = LengthValidator('1234567') # password < 8
    assert validator.is_valid() == 'Password must contain at least 8 characters. '
        

def test_uppercase_in_password():
    validator = UpperCharValidator('Abcdefghijk')
    assert validator.is_valid() is False

def test_uppercase_in_password_negative():
    validator = UpperCharValidator('abcdefghijk')
    assert validator.is_valid() == 'Password must contain at least one capital letter. '

def test_ulowercase_in_password():
    validator = LowerCharValidator('aBCDEFGHIJK')
    assert validator.is_valid() is False

def test_lowercase_in_password_negative():
    validator = LowerCharValidator('ABCDEFGHIJK')
    assert validator.is_valid() == 'Password must contain at least one lowercase letter. '
