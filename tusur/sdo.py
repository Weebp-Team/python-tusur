from .authorization import Auth
from .exceptions import TusurError


class Notifications(Auth):
    """
    Class for retrieving notifications from the TUSUR system.

    Args:
        login (str): User's login.
        password (str): User's password.

    Attributes:
        __notifications_url (str): URL for retrieving notifications.
        __service_url (str): Service URL.

    Methods:
        get_notifications(): Retrieves user notifications.
    """
    def __init__(self, login: str, password: str) -> None:
        """
        Initializes a Notifications object.

        Args:
            login (str): User's login.
            password (str): User's password.
        """

        super().__init__(login, password)
        self.__notifications_url = "https://sdo.tusur.ru/message/output/popup/notifications.php"
        self.__service_url = "https://sdo.tusur.ru/lib/ajax/service.php"

    def get_notifications(self) -> dict:
        """
        Retrieves user notifications.

        Returns:
            dict: Dictionary containing notification data.
        Raises:
            TusurError: If an error occurs while retrieving notifications.
        """

        response = self.session.get(self.__notifications_url)
        sesskey = self.get_sesskey(response)
        contextInstanceId = self.get_contextInstanceId(response)
        data = [{
            "index": 0,
            "methodname": "message_popup_get_popup_notifications",
            "args": {
                "limit": 1000,
                "offset": 0,
                "useridto": contextInstanceId
            }
        }]
        notifications = self.session.post(self.__service_url,
                                          params={
                                              "sesskey": sesskey,
                                              "info": "message_popup_get_popup_notifications"
                                          },
                                          json=data).json()
        if notifications[0]["error"]:
            raise TusurError(notifications["error"])
        return notifications
