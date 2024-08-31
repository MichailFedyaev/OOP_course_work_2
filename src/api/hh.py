from typing import Any

import requests

from src.api.abc_parser import Parser


class HH(Parser):
    """ Класс для работы с API HeadHunter """

    @staticmethod
    def __connection_to_api(api_params: dict) -> Any:
        """Приватный метод для подключения к API"""

        url = "https://api.hh.ru/vacancies"
        headers = {"User-Agent": "HH-User-Agent"}

        response = requests.get(url, headers=headers, params=api_params)

        if response.status_code != 200:
            raise requests.RequestException
        return response

    @classmethod
    def load_vacancies(cls, keyword: str) -> list:
        """Метод для получения вакансий по ключевому слову"""

        params = {"text": keyword, "page": 0, "per_page": 100, "area": 113}
        vacancies = []

        print("Загрузка данных ... ", end="")
        while params.get("page") != 20:
            print("#", end="")
            vacancies_page = cls.__connection_to_api(params).json()["items"]
            # print(type(vacancies_page), len(vacancies_page))
            vacancies.extend(vacancies_page)
            # print(type(vacancies), len(vacancies))
            params["page"] += 1

        return vacancies
