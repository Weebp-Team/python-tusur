Get ocenka example
=====================

Import class ``Ocenka`` from module ``tusur``

Use method ``get_all_marks`` with params:

 * surname: str - Student surname.
 * name: str - Student name.
 * group: str - Student group.

or

Use method ``get_marks_by_course`` with params:

 * surname: str - Student surname.
 * name: str - Student name.
 * group: str - Student group.
 * course: int - Student course.

.. code-block:: python

    >>> from tusur import Ocenka
    >>> ocenka = Ocenka()
    >>> ocenka.get_marks_by_course("Исайченко", "Никита", "571-2", 1)
    {
        "student": {
            "fullname": "Исайченко Никита Евгеньевич",
            "group_number": "571-2",
            "correspondence": false,
            "faculty_abbr": "FVS",
            "current_semester_id": 20
        },
        "semesters": ...,
        "marks": ...,
        "future_exam_session": ...,
        "available_courses": ...,
        "course": ...,
        "discipline_info_kinds": ...
    }