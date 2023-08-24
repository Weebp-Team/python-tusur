import os
from dotenv import load_dotenv
import pytest
from tusur import Messages
from tusur.exceptions import AuthorizationFailed

load_dotenv()


def test_get_messages():
    login = os.getenv('TUSUR_LOGIN')
    password = os.getenv('TUSUR_PASSWORD')
    messages = Messages(login, password)
    assert type(messages.get_messages()) == list


def test_get_wrong_messages():
    login = "wrong-login"
    password = "wrong-password"
    with pytest.raises(AuthorizationFailed):
        _ = Messages(login, password)
