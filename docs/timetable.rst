Get timetable example
=====================

Import class ``Timetable`` from module ``tusur``

Use method ``get_timetable`` with params:

 * search_data: str - Data for timetable search.
 * week_id: int - Optional. Week id

.. code-block:: python

    >>> from tusur import Timetable
    >>> timetable = Timetable()
    >>> timetable.get_timetable("571-2", week_id=666)
    [
        { "day": "пн, 22 мая",
        "lessons": [
            {
            "discipline": "ОРБД",
            "kind": "Лабораторная работа",
            "teacher": "Лабораторная работа",
            "time": "08:50 10:25"
        },
        {
            "discipline": "ОРБД",
            "kind": "Лабораторная работа",
            "teacher": "Лабораторная работа",
            "time": "10:40 12:15"
        },
        {
            "discipline": "МЛиТА",
            "kind": "Практика",
            "teacher": "Практика",
            "time": "13:15 14:50"
        },
        ...
    ]