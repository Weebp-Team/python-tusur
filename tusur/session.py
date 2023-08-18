import requests
from requests import Response
from bs4 import BeautifulSoup
from .exceptions import TimetableNotFound


class Timetable:
    def __init__(self) -> None:
        self.__common_search_url = "https://timetable.tusur.ru/searches/common_search"

    def __get_timetable_url(self, search_data: int) -> str:
        params = {
            "utf8": "✓",
            "search[common]": search_data,
            "commit": ""
        }
        response = requests.get(url=self.__common_search_url, params=params)
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
                teacher = lesson.find("span", class_="kind")
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
        timetable: Response = requests.get(url=timetable_url,
                                           params={"week_id": week_id})
        parsed_timetable: dict = self.__parse_timetable(timetable)
        return parsed_timetable
