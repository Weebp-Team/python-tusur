import os
from dotenv import load_dotenv
import pytest
from tusur import Notifications
from tusur.exceptions import AuthorizationFailed

load_dotenv()


def test_get_notifications():
    login = os.getenv('TUSUR_LOGIN')
    password = os.getenv('TUSUR_PASSWORD')
    notifications = Notifications(login, password)
    assert type(notifications.get_notifications()) == list


def test_get_wrong_notifications():
    login = os.getenv('wrong-login')
    password = os.getenv('wrong-password')
    with pytest.raises(AuthorizationFailed):
        notifications = Notifications(login, password)
        notifications.get_notifications()
