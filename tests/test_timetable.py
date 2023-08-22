import pytest
from tusur import Timetable
from tusur.exceptions import TimetableNotFound


def test_get_timetable():
    timetable = Timetable()
    assert type(timetable.get_timetable("571-2")) == list


def test_get_wrong_timetable():
    timetable = Timetable()
    with pytest.raises(TimetableNotFound):
        timetable.get_timetable("wrong-table")
