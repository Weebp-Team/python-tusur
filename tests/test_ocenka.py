import pytest
from tusur import Ocenka
from tusur.exceptions import StudentNotFound


def test_get_all_marks():
    ocenka = Ocenka()
    surname = "Исайченко"
    name = "Никита"
    group = "571-2"
    assert type(ocenka.get_all_marks(surname, name, group)) == dict


def test_get_wrong_all_marks():
    ocenka = Ocenka()
    surname = "Не Исайченко"
    name = "Никита"
    group = "571-2"
    with pytest.raises(StudentNotFound):
        ocenka.get_all_marks(surname, name, group)


def test_get_marks_by_course():
    ocenka = Ocenka()
    surname = "Исайченко"
    name = "Никита"
    group = "571-2"
    course = 1
    assert type(ocenka.get_marks_by_course(surname, name,
                                           group, course)) == dict


def test_get_wrong_marks_by_course():
    ocenka = Ocenka()
    surname = "Не Исайченко"
    name = "Никита"
    group = "571-2"
    course = 1
    with pytest.raises(StudentNotFound):
        ocenka.get_marks_by_course(surname, name, group, course)
