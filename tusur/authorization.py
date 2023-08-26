import re
from requests import session, Response
from .exceptions import AuthorizationFailed
from .constants import AUTH_URL, SDO_AUTH_REDIRECT_URL


class Auth:
    def __init__(self, login: str, password: str) -> None:
        """
        Initialize an instance of the Auth class.

        Args:
            login (str): The user's login/email.
            password (str): The user's password.
        """
        self.__login = login
        self.__password = password
        self._session = session()
        self.__auth()
        self.__sdo_auth()

    def __auth(self):
        """
        Perform tusur.ru authentication.

        Raises:
            AuthorizationFailed: If authentication is unsuccessful.
        """
        form = {
            "utf8": "✓",
            "user[email]": self.__login,
            "user[password]": self.__password
        }
        response = self._session.post(AUTH_URL, data=form)
        if not response.url.endswith("dashboard"):
            raise AuthorizationFailed()

    def __sdo_auth(self):
        """
        Perform sdo.tusur.ru authentication.
        """
        self._session.get(AUTH_URL,
                          params={
                              "redirect_url": SDO_AUTH_REDIRECT_URL
                          })

    def _get_sesskey(self, response: Response) -> str:
        """
        Extract and return the sesskey from the response text.

        Args:
            response (Response): The response object
                                 from which to extract the sesskey.

        Returns:
            str: The extracted sesskey, or an empty string if not found.
        """
        sesskey = re.search(r'"sesskey":"(.*?)"', response.text)
        if sesskey:
            sesskey = sesskey.group(1)
        return sesskey

    def _get_contextInstanceId(self, response: Response) -> str:
        """
        Extract and return the contextInstanceId from the response text.

        Args:
            response (Response): The response object
                                 from which to extract the contextInstanceId.

        Returns:
            str: The extracted contextInstanceId,
                 or an empty string if not found.
        """
        contextInstanceId = re.search(r'"contextInstanceId":(.*?),',
                                      response.text)
        if contextInstanceId:
            contextInstanceId = contextInstanceId.group(1)
        return contextInstanceId
