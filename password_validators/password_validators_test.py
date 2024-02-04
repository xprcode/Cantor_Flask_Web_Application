import pytest
from modules.password_validators.password_validators import (
    DigitValidator,
    SpecialCharValidator,
    UpperCharValidator,
    LowerCharValidator,
    LengthValidator,
    IfPownedValidator,
    ValidationError,
    PasswordValidator
)


def test_digit_in_password():
    validator = DigitValidator('abc1')
    assert validator.is_valid() is True

def test_digit_in_password_negative():
    validator = DigitValidator('abc')
    with pytest.raises(ValidationError) as error:
        validator.is_valid()
        assert 'Password must contain at least on digit. ' in str(error.value)

def test_special_in_password():
    validator = SpecialCharValidator('.,/')
    assert validator.is_valid() is True

def test_special_in_password_negative():
    validator = SpecialCharValidator('abc1')
    with pytest.raises(ValidationError) as error:
        validator.is_valid()
        assert 'Password must contain at least on special character. ' in str(error.value)

def test_lenght_in_password():
    validator1 = LengthValidator('12345678') # password = 8
    validator2 = LengthValidator('123456789') # passowrd > 8
    assert validator1.is_valid() and validator2.is_valid() is True

def test_lenght_in_password_negative():
    validator = SpecialCharValidator('12345671') # password < 8
    with pytest.raises(ValidationError) as error:
        validator.is_valid()
        assert 'Password must contain at least 8 characters. ' in str(error.value)

def test_uppercase_in_password():
    validator = UpperCharValidator('Abcdefghijk')
    assert validator.is_valid() is True

def test_uppercase_in_password_negative():
    validator = UpperCharValidator('abcdefghijk')
    with pytest.raises(ValidationError) as error:
        validator.is_valid()
        assert 'Password must contain at least one capital letter. ' in str(error.value)

def test_ulowercase_in_password():
    validator = LowerCharValidator('aBCDEFGHIJK')
    assert validator.is_valid() is True

def test_lowercase_in_password_negative():
    validator = LowerCharValidator('ABCDEFGHIJK')
    with pytest.raises(ValidationError) as error:
        validator.is_valid()
        assert 'Password must contain at least one capital letter. ' in str(error.value)

def If_powned_test(requests_mock):
    data = '22AE348AEB5660FC2140AEC35850C4DA997:1786404\n00294015E5A8513C73396D18309F3FFF34A:8'
    requests_mock.get('https://api.pwnedpasswords.com/range/D033E', text=data)
    validator = IfPownedValidator('admin')
    with pytest.raises(ValidationError) as error:
        validator.is_valid()
        assert 'Password has been leaked. ' in str(error.value)

def test_password_validator_1():
    validator = PasswordValidator('AAAAAAA9:[]')
    with pytest.raises(ValidationError, match='Password must contain at least one lowercase letter.'):
        validator.is_valid()
