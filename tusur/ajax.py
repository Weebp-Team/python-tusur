from .exceptions import TusurError
from .constants import AJAX_SERVICE_URL
from requests import Session


class Ajax:
    def __init__(self, session: Session) -> None:
        self.__session = session

    def _send(self, params: dict, data: dict) -> dict:
        """
        Send an AJAX request to a specified URL
        with the provided parameters and data.

        Args:
            params (dict): Query parameters to be included in the request URL.
            data (dict): JSON data payload to be sent in the request body.

        Returns:
            dict: A dictionary containing the JSON response
            received from the AJAX request.

        Raises:
            TusurError: If an error is encountered in the JSON response.

        Example:
            ajax_instance = Ajax(session)
            params = {'key': 'value'}
            data = {'data_key': 'data_value'}
            response = ajax_instance._send(params, data)
        """
        response = self.__session.post(AJAX_SERVICE_URL,
                                       params=params, json=data)

        if response.status_code == 200:
            json_response = response.json()

            if type(json_response) is list:
                if json_response[0]["error"]:
                    raise TusurError(json_response[0]["error"])
            else:
                if json_response["error"]:
                    raise TusurError(json_response["error"])

            return json_response
