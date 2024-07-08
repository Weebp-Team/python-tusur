import re
from typing import List

from bs4 import BeautifulSoup

from tusur.exceptions import TusurError
from .authorization import Auth
from .ajax import Ajax
from .constants import NOTIFICATIONS_URL, USER_INDEX_URL, USER_VIEW_URL


class Notifications(Auth):
    def __init__(self, login: str, password: str) -> None:
        """
        Initialize an instance of the Notifications class.

        Args:
            login (str): The user's login/email.
            password (str): The user's password.
        """
        super().__init__(login, password)
        self.__ajax = Ajax(self._session)

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
        notifications = self.__ajax._send(params=params, data=data)
        return notifications


class Messages(Auth):
    def __init__(self, login: str, password: str) -> None:
        """
        Initialize an instance of the Notifications class.

        Args:
            login (str): The user's login/email.
            password (str): The user's password.
        """
        super().__init__(login, password)
        self.__ajax = Ajax(self._session)

    def get_messages(self, favourites: bool = False) -> list:
        response = self._session.get(USER_INDEX_URL)
        sesskey = self._get_sesskey(response)
        contextInstanceId = self._get_contextInstanceId(response)
        data = [{
            "index": 0,
            "methodname": "core_message_get_conversations",
            "args": {
                "favourites": favourites,
                "limitfrom": 0,
                "limitnum": 51,
                "type": None,
                "userid": contextInstanceId
            }
        }]
        params = {
            "sesskey": sesskey,
            "info": "core_message_get_conversations"
        }
        messages = self.__ajax._send(params=params, data=data)
        return messages


class User(Auth):

    def __init__(self, login: str, password: str) -> None:
        """
        Initialize an instance of the User class.

        Args:
            login (str): The user's login/email.
            password (str): The user's password.
        """
        super().__init__(login, password)

    def __get_content(self, url: str, params: dict) -> bytes:
        response = self._session.get(url=url, params=params)
        if response.status_code != 200:
            raise TusurError("Хуй знает")
        return response.content

    def __parse_user(self, soup: BeautifulSoup) -> dict:
        name = soup.find("div", class_="page-header-headings").text
        card = soup.find("div", class_="card-body")
        contentnode = card.find_all("li", class_="contentnode")
        email = contentnode[0].find("dd").find("a").text
        country = contentnode[1].find("dd").text
        town = contentnode[2].find("dd").text
        time_zone = contentnode[3].find("dd").text
        groups = contentnode[4].find("dd").text.strip()
        return dict(name=name, email=email, country=country, town=town,
                    time_zone=time_zone, groups=groups)

    def __parse_participants(self, soup: BeautifulSoup) -> list[dict]:
        table = soup.find("table", id="participants")
        rows = table.find_all("tr", id=re.compile("^user-index"))
        participants = []
        for row in rows:
            a = row.find("a")
            if not a:
                continue
            span = a.find("span")
            if span:
                span.clear()
            name = a.text
            href = a.get("href")
            role = row.find("td", class_="c2").text
            groups = row.find("td", class_="c3").text
            last_entry = row.find("td", class_="c4").text
            participants.append(dict(name=name, url=href, role=role,
                                     groups=groups, last_entry=last_entry))
        return participants

    def get_participants(self, id: int, tilast: str = None,
                         tifirst: str = None, perpage: int = None,
                         page: int = 0) -> dict:
        params = dict(id=id, tifirst=tifirst, tilast=tilast,
                      perpage=perpage, page=page)
        content = self.__get_content(url=USER_INDEX_URL, params=params)
        soup = BeautifulSoup(content, "html.parser")
        return self.__parse_participants(soup)

    def get_user(self, id: int) -> dict:
        params = dict(id=id)
        content = self.__get_content(url=USER_VIEW_URL, params=params)
        soup = BeautifulSoup(content, "html.parser")
        return self.__parse_user(soup)
