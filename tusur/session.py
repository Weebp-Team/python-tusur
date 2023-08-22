import requests
import json

from requests import Response
from bs4 import BeautifulSoup
from .exceptions import TimetableNotFound, StudentNotFound
from .constants import (
    COMMON_SEARCH_URL,
    STUDENT_MARKS_URL,
    STUDENT_SEARCH_URL
)


class Timetable:
    def __init__(self) -> None:
        """
        Initialize an instance of the Timetable class.
        """
        self.__session = requests.session()

    def __get_timetable_url(self, search_data: int) -> str:
        """
        Retrieve the timetable URL for the given search data.

        Args:
            search_data (int): Search data used to generate the timetable URL.

        Returns:
            str: The generated timetable URL.

        Raises:
            TimetableNotFound: If the timetable URL is not found.
        """
        params = {
            "utf8": "✓",
            "search[common]": search_data,
            "commit": ""
        }
        response = self.__session.get(url=COMMON_SEARCH_URL,
                                      params=params)
        if len(response.history) == 0:
            raise TimetableNotFound(search_data)
        return response.url

    @staticmethod
    def __normalize_text(text: str) -> str | None:
        """
        Normalize the provided text by removing extra spaces and newlines.

        Args:
            text (str): The text to normalize.

        Returns:
            str | None: The normalized text, or None if the input was None.
        """
        if text is not None:
            striped_text = text.strip()
            replaced_text = striped_text.replace("  ", "")
            return replaced_text.replace("\n", " ")
        return None

    def __parse_timetable(self, response: Response) -> list:
        """
        Parse the timetable information from the provided response.

        Args:
            response (Response): The response containing timetable information.

        Returns:
            list: A list of dictionaries representing the parsed timetable.

        Example:
            parsed_timetable = self.__parse_timetable(response)
        """
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
        """
        Get the timetable for the provided search data.

        Args:
            search_data (str): Search data for finding the timetable.
            week_id (int, optional): The week ID for filtering the timetable. Default is None.

        Returns:
            list: A list of dictionaries representing the retrieved timetable.

        Example:
            timetable = self.get_timetable("search_data_here", week_id=2)
        """
        timetable_url: str = self.__get_timetable_url(search_data=search_data)
        timetable: Response = self.__session.get(url=timetable_url,
                                                 params={"week_id": week_id})
        parsed_timetable: dict = self.__parse_timetable(timetable)
        return parsed_timetable


class Ocenka:
    def __init__(self) -> None:
        """
        Initialize an instance of the Ocenka class.
        """
        self.__session = requests.session()

    def __get_student_url(self, surname: str, name: str, group: str) -> str:
        """
        Retrieve the student's URL using their surname, name, and group.

        Args:
            surname (str): Student's surname.
            name (str): Student's name.
            group (str): Student's group.

        Returns:
            str: The generated student URL.

        Raises:
            StudentNotFound: If the student URL is not found.
        """
        params = {
            "utf8": "✓",
            "surname": surname,
            "name": name,
            "group": group,
            "commit": "Найти"
        }
        response = self.__session.get(url=STUDENT_SEARCH_URL,
                                      params=params)
        if len(response.history) == 0:
            raise StudentNotFound(surname, name, group)
        return response.url

    def __get_context_id(self, response: Response) -> int:
        """
        Get the context ID from the provided response.

        Args:
            response (Response): The response containing the context ID.

        Returns:
            int: The extracted context ID.

        Example:
            context_id = self.__get_context_id(response)
        """
        soup = BeautifulSoup(response.content, "html.parser")
        js_role_token = soup.find("span", class_="js-role-token")
        context_id = json.loads(js_role_token.get("data-role"))["context_id"]
        return context_id

    def __get_marks_by_api(self, context_id: int, course: int) -> dict:
        """
        Get the student's marks using the API.

        Args:
            context_id (int): The context ID of the student.
            course (int): The course for which to retrieve marks.

        Returns:
            dict: A dictionary containing the retrieved marks.

        Example:
            marks = self.__get_marks_by_api(context_id, course)
        """
        params = {
            "context_id": context_id,
            "context_type": "student",
            "course": course,
            "role": "student_search"
        }
        url: str = STUDENT_MARKS_URL.format(context_id=context_id)
        response: Response = self.__session.get(url=url, params=params)
        if response.status_code == 200:
            return response.json()
        return {}

    def get_all_marks(self, surname: str, name: str, group: str):
        """
        Get all marks for the provided student.

        Args:
            surname (str): Student's surname.
            name (str): Student's name.
            group (str): Student's group.

        Returns:
            dict: A dictionary containing student information and their marks.

        Example:
            all_marks = self.get_all_marks("Smith", "John", "GroupA")
        """
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
        """
        Get marks for the provided student and course.

        Args:
            surname (str): Student's surname.
            name (str): Student's name.
            group (str): Student's group.
            course (int): The course for which to retrieve marks.

        Returns:
            dict: A dictionary containing the student's marks for the specified course.

        Example:
            course_marks = self.get_marks_by_course("Smith", "John", "GroupA", 1)
        """
        student_url: str = self.__get_student_url(surname=surname,
                                                  name=name,
                                                  group=group)
        ocenka: Response = self.__session.get(url=student_url)
        context_id: int = self.__get_context_id(ocenka)
        result = self.__get_marks_by_api(context_id=context_id,
                                         course=course)
        return result
