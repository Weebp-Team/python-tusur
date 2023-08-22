from typing import List
from .authorization import Auth
from .ajax import Ajax
from .constants import NOTIFICATIONS_URL


class Notifications(Auth, Ajax):
    def __init__(self, login: str, password: str) -> None:
        """
        Initialize an instance of the Notifications class.

        Args:
            login (str): The user's login/email.
            password (str): The user's password.
        """
        Auth.__init__(self, login, password)
        Ajax.__init__(self)

    def get_notifications(self, limit: int = 1000,
                          offset: int = 0) -> List[dict]:
        """
        Get notifications for the authenticated user.

        Args:
            limit (int, optional): The maximum number of notifications
                                   to retrieve. Default is 1000.
            offset (int, optional): The offset to start retrieving
                                    notifications from. Default is 0.

        Returns:
            List[dict]: A list of dictionaries representing
                        the retrieved notifications.

        Example:
            notifications_instance = Notifications('user@example.com', 'password')
            notifications = notifications_instance.get_notifications(limit=10, offset=0)
        """
        response = self._session.get(NOTIFICATIONS_URL)
        sesskey = self._get_sesskey(response)
        contextInstanceId = self._get_contextInstanceId(response)
        data = [{
            "index": 0,
            "methodname": "message_popup_get_popup_notifications",
            "args": {
                "limit": limit,
                "offset": offset,
                "useridto": contextInstanceId
            }
        }]
        params = {
            "sesskey": sesskey,
            "info": "message_popup_get_popup_notifications"
        }
        notifications = self._ajax_send(params=params, data=data)
        return notifications
