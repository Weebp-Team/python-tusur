Get notifications example
=====================

Import class ``Notifications`` from module ``tusur``

Use method ``get_notifications`` with params:

 * login: str - Email.
 * password: int - Password.

.. code-block:: python

    >>> from tusur import Notifications
    >>> login = ""
    >>> password = "" 
    >>> notifications = Notifications(login, password)
    >>> notifications.get_notifications("571-2", week_id=666)
    [
        {
            "error": false,
            "data": ""
        }
    ]