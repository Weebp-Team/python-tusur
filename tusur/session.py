"""
Module Documentation: Timetable and Ocenka Classes

This module contains two classes, Timetable and Ocenka, which provide methods for fetching student timetables and academic marks from the TUSUR University systems.

Timetable Class:
----------------
Timetable class provides methods to fetch student timetables from the TUSUR University's timetable system.

Attributes:
    __common_search_url (str): The base URL for the common search on the timetable system.
    __session (requests.Session): A session object to handle HTTP requests and maintain session state.

Methods:
    get_timetable(search_data: str, week_id: int = None) -> list:
        Fetches and parses the student's timetable.

        Parameters:
            search_data (str): Search query data, typically the student's group or other identifying information.
            week_id (int, optional): ID of the week for which the timetable is requested.

        Returns:
            list: A list of dictionaries containing timetable information for each day.

Ocenka Class:
-------------
Ocenka class provides methods to fetch student academic marks from the TUSUR University's academic marks system.

Attributes:
    __student_search_url (str): The URL for searching students in the academic marks system.
    __student_marks_url (str): The base URL for fetching student marks via the API.
    __student_statistics_url (str): The URL for fetching student statistics via the API.
    __session (requests.Session): A session object to handle HTTP requests and maintain session state.

Methods:
    get_all_marks(surname: str, name: str, group: str) -> dict:
        Fetches and returns all academic marks and related information for a student.

        Parameters:
            surname (str): Student's surname.
            name (str): Student's first name.
            group (str): Student's group.

        Returns:
            dict: A dictionary containing student information, available courses, and academic marks for each course.

    get_marks_by_course(surname: str, name: str, group: str, course: int) -> dict:
        Fetches and returns academic marks for a student for a specific course.

        Parameters:
            surname (str): Student's surname.
            name (str): Student's first name.
            group (str): Student's group.
            course (int): Course number.

        Returns:
            dict: A dictionary containing academic marks and related information for the specified course.
"""

import requests
import json

from requests import Response
from bs4 import BeautifulSoup
from .exceptions import TimetableNotFound, StudentNotFound


class Timetable:
    def __init__(self) -> None:
        self.__common_search_url = "https://timetable.tusur.ru/searches/common_search"
        self.__session = requests.session()

    def __get_timetable_url(self, search_data: int) -> str:
        params = {
            "utf8": "✓",
            "search[common]": search_data,
            "commit": ""
        }
        response = self.__session.get(url=self.__common_search_url,
                                      params=params)
        if len(response.history) == 0:
            raise TimetableNotFound(f'A search for "{search_data}" yielded no results')
        return response.url

    @staticmethod
    def __normalize_text(text: str) -> str | None:
        if text is not None:
            striped_text = text.strip()
            replaced_text = striped_text.replace("  ", "")
            return replaced_text.replace("\n", " ")
        return None

    def __parse_timetable(self, response: Response) -> list:
        timetable = []
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="table")
        thead = table.find("thead")
        tbody = table.find("tbody")
        days = thead.find_all("th")
        if days[0].text.strip() == '':
            days.pop(0)
        rows = tbody.find_all("tr")
        for i, day in enumerate(days):
            day = self.__normalize_text(day.text)
            lessons = []
            for ls in rows:
                time = ls.find("th", class_="time")
                lesson = ls.find_all("td")[i]
                discipline = lesson.find("span", class_="discipline")
                kind = lesson.find("span", class_="kind")
                teacher = lesson.find("span", class_="group")
                normalized_discipline = self.__normalize_text(discipline.text) if discipline else None
                normalized_kind = self.__normalize_text(kind.text) if kind else None
                normalized_teacher = self.__normalize_text(teacher.text) if teacher else None
                normalized_time = self.__normalize_text(time.text) if time else None
                lessons.append({"time": normalized_time,
                                "discipline": normalized_discipline,
                                "kind": normalized_kind,
                                "teacher": normalized_teacher})
            timetable.append({"day": day, "lessons": lessons})
        return timetable

    def get_timetable(self, search_data: str, week_id: int = None) -> list:
        timetable_url: str = self.__get_timetable_url(search_data=search_data)
        timetable: Response = self.__session.get(url=timetable_url,
                                                 params={"week_id": week_id})
        parsed_timetable: dict = self.__parse_timetable(timetable)
        return parsed_timetable


class Ocenka:
    def __init__(self) -> None:
        self.__student_search_url = "https://ocenka.tusur.ru/student_search"
        self.__student_marks_url = "https://ocenka.tusur.ru/api/students/{context_id}"
        self.__student_statistics_url = "https://ocenka.tusur.ru/api/students/{context_id}/statistics"
        self.__session = requests.session()

    def __get_student_url(self, surname: str, name: str, group: str) -> str:
        params = {
            "utf8": "✓",
            "surname": surname,
            "name": name,
            "group": group,
            "commit": "Найти"
        }
        response = self.__session.get(url=self.__student_search_url,
                                      params=params)
        if len(response.history) == 0:
            raise StudentNotFound(f'A search for "{surname} {name} {group}" yielded no results')
        return response.url

    def __get_context_id(self, response: Response) -> int:
        soup = BeautifulSoup(response.content, "html.parser")
        js_role_token = soup.find("span", class_="js-role-token")
        context_id = json.loads(js_role_token.get("data-role"))["context_id"]
        return context_id

    def __get_marks_by_api(self, context_id: int, course: int) -> dict:
        params = {
            "context_id": context_id,
            "context_type": "student",
            "course": course,
            "role": "student_search"
        }
        url: str = self.__student_marks_url.format(context_id=context_id)
        response: Response = self.__session.get(url=url, params=params)
        if response.status_code == 200:
            return response.json()
        return {}

    def get_all_marks(self, surname: str, name: str, group: str):
        student_url: str = self.__get_student_url(surname=surname,
                                                  name=name,
                                                  group=group)
        ocenka: Response = self.__session.get(url=student_url)
        context_id: int = self.__get_context_id(ocenka)
        result = self.__get_marks_by_api(context_id=context_id,
                                         course=1)
        available_courses = list(map(int, result["available_courses"]))
        marks = {
            "student": result["student"],
            "courses": [],
        }
        for course in available_courses:
            marks_by_course = self.__get_marks_by_api(context_id=context_id,
                                                      course=course)
            courses = marks["courses"]
            courses.append({
                "course": course,
                "semesters": marks_by_course.get("semesters"),
                "marks": marks_by_course.get("marks"),
                "future_exam_session": marks_by_course.get("future_exam_session"),
            })
            marks["courses"] = courses
        return marks

    def get_marks_by_course(self, surname: str, name: str,
                            group: str, course: int):
        student_url: str = self.__get_student_url(surname=surname,
                                                  name=name,
                                                  group=group)
        ocenka: Response = self.__session.get(url=student_url)
        context_id: int = self.__get_context_id(ocenka)
        result = self.__get_marks_by_api(context_id=context_id,
                                         course=course)
        return result


"""
Please note that the provided code contains the implementation of the Timetable and Ocenka classes.
This documentation only outlines the usage and purpose of the classes and their methods.
For detailed usage examples and exception handling, refer to the module where these classes are used.
"""
