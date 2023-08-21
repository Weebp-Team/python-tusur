import re
from requests import session, Response
from .exceptions import AuthorizationFailed


class Auth:
    """
    Class for handling authentication with TUSUR services.

    Args:
        login (str): User's login.
        password (str): User's password.

    Attributes:
        __login (str): User's login.
        __password (str): User's password.
        __auth_url (str): URL for authentication.
        session (Session): Requests session for making HTTP requests.

    Methods:
        get_sesskey(response: Response) -> str: Extracts sesskey from the response.
        get_contextInstanceId(response: Response) -> str: Extracts contextInstanceId from the response.
    """
    def __init__(self, login: str, password: str) -> None:
        """
        Initializes an Auth object.

        Args:
            login (str): User's login.
            password (str): User's password.
        """
        self.__login = login
        self.__password = password
        self.__auth_url = "https://profile.tusur.ru/en/users/sign_in"
        self.__sdo_auth_redirect = "https://sdo.tusur.ru/auth/edu/?id=1"
        self.session = session()
        self.__auth()
        self.__sdo_auth()

    def __auth(self):
        """
        Performs user authentication.

        Raises:
            AuthorizationFailed: If the authorization fails.
        """
        form = {
            "utf8": "✓",
            "user[email]": self.__login,
            "user[password]": self.__password
        }
        response = self.session.post(self.__auth_url, data=form)
        if not response.url.endswith("dashboard"):
            raise AuthorizationFailed("Authorization failed! " +
                                      "Check your email and password.")

    def __sdo_auth(self):
        """
        Performs SDO authentication after profile authentication.
        """
        self.session.get(self.__auth_url,
                         params={
                             "redirect_url": self.__sdo_auth_redirect
                         })

    def get_sesskey(self, response: Response) -> str:
        """
        Extracts sesskey from the response.

        Args:
            response (Response): HTTP response containing the sesskey.

        Returns:
            str: Extracted sesskey.
        """
        sesskey = re.search(r'"sesskey":"(.*?)"', response.text)
        if sesskey:
            sesskey = sesskey.group(1)
        return sesskey

    def get_contextInstanceId(self, response: Response) -> str:
        """
        Extracts contextInstanceId from the response.

        Args:
            response (Response): HTTP response containing contextInstanceId.

        Returns:
            str: Extracted contextInstanceId.
        """
        contextInstanceId = re.search(r'"contextInstanceId":(.*?),',
                                      response.text)
        if contextInstanceId:
            contextInstanceId = contextInstanceId.group(1)
        return contextInstanceId
