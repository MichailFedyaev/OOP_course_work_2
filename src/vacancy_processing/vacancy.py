from typing import Any

from src.vacancy_processing.abc_vacancy_worker import VacancyWorker


class Vacancy(VacancyWorker):
    """Класс для работы с вакансиями"""

    id: int
    name: str
    location: str
    salary: float
    salary_string: str
    published_at: str
    url: str
    name_employer: str
    schedule: str
    employment: str
    experience: str
    requirement: str
    responsibility: str

    __slots__ = (
        "id",
        "name",
        "location",
        "salary",
        "salary_string",
        "published_at",
        "url",
        "name_employer",
        "schedule",
        "employment",
        "experience",
        "requirement",
        "responsibility",
    )

    def __init__(self, vacancy: dict) -> None:
        """На вход конструктора ожидается словарь с ключами, аналогичными в __slots__
        В классе реализованы методы, позволяющие обработать данные от hh для приведения их в нужный вид
        """

        for vacancy_attribute in self.__slots__:
            if self.__check_attribute(vacancy_attribute, vacancy.keys()):
                setattr(self, vacancy_attribute, vacancy[vacancy_attribute])
            else:
                setattr(self, vacancy_attribute, None)

    def __str__(self) -> str:
        """Получение информации о вакансии"""

        return (f"{self.name}\n"
                f"Ссылка на вакансию: {self.url}\n"
                f"Зарплата: {(self.salary_string + " " * 20)[:20]}\n"
                f"Город: {self.location}\n"
                f"График: {self.schedule}\n"
                f"Описание: {self.requirement}\n")

    def to_dict(self) -> dict:
        """Метод возвращает вакансию в формате словаря"""

        result = {}

        for attr in self.__slots__:
            result[attr] = getattr(self, attr)

        return result

    @staticmethod
    def get_list_of_vacancies(vacancies: list[dict]) -> list:
        """Создание списка из объектов класса Vacancy"""

        return [Vacancy(vacancy) for vacancy in vacancies]

    @staticmethod
    def get_list_of_dicts_vacancies(vacancies: list) -> list:
        """Создание списка словарей из списка объектов вакансий"""

        return [vacancy.to_dict() for vacancy in vacancies]

    def __check_attribute(self, attribute: Any, keys: list) -> Any:
        """Валидация аттрибутов при создании объекта класса"""

        return attribute in keys

    @staticmethod
    def get_list_id_vacancies(vacancies: list) -> list:
        """Получить список ID из списка вакансий (объектов или словарей)"""

        return [vacancy.id if isinstance(vacancy, Vacancy) else vacancy["id"] for vacancy in vacancies]

    def get_salary(self) -> str:
        """Получить значение зарплаты"""

        return self.salary_string

    def __get_salary_for_comparison(self) -> Any:
        """Получить значение зарплаты для сравнения. По умолчанию берется значение "от", если ничего не указано - 0"""

        return self.salary

    def __eq__(self, other: Any) -> Any:
        """Метод сравнения вакансий по зарплате - для равенства =="""

        if type(other) is Vacancy:
            return self.__get_salary_for_comparison() == other.__get_salary_for_comparison()
        else:
            raise TypeError

    def __ne__(self, other: Any) -> Any:
        """Метод сравнения вакансий по зарплате - для неравенства !="""

        if type(other) is Vacancy:
            return self.__get_salary_for_comparison() != other.__get_salary_for_comparison()
        else:
            raise TypeError

    def __lt__(self, other: Any) -> Any:
        """Метод сравнения вакансий по зарплате - для оператора меньше <"""
        if type(other) is Vacancy:
            return self.__get_salary_for_comparison() < other.__get_salary_for_comparison()
        else:
            raise TypeError

    def __le__(self, other: Any) -> Any:
        """Метод сравнения вакансий по зарплате - для оператора меньше или равно <="""

        if type(other) is Vacancy:
            return self.__get_salary_for_comparison() <= other.__get_salary_for_comparison()
        else:
            raise TypeError

    def __gt__(self, other: Any) -> Any:
        """Метод сравнения вакансий по зарплате - для оператора больше >"""

        if type(other) is Vacancy:
            return self.__get_salary_for_comparison() > other.__get_salary_for_comparison()
        else:
            raise TypeError

    def __ge__(self, other: Any) -> Any:
        """Метод сравнения вакансий по зарплате - для оператора больше или равно >="""

        if type(other) is Vacancy:
            return self.__get_salary_for_comparison() >= other.__get_salary_for_comparison()
        else:
            raise TypeError

    @staticmethod
    def get_top_salary_vacancies(vacancies: list, top_n: int) -> list:
        """Получить топ вакансий по зарплате в заданном количестве"""

        if isinstance(vacancies[0], Vacancy):
            sorted_vacancies = sorted(vacancies, reverse=True)
        else:
            sorted_vacancies = sorted(vacancies, key=lambda x: x["salary"], reverse=True)

        return sorted_vacancies[:top_n]

    @staticmethod
    def filter_by_keywords(vacancies: list, keywords: list) -> list:
        """Оставляет в списке только те вакансии, которые содержат ключевые слова в названии,
        требованиях или обязанностях
        """

        filtered_vacancies = []
        for vacancy in vacancies:
            string_for_searching = (vacancy.name + str(vacancy.requirement) + str(vacancy.responsibility)).lower()
            check_status = True
            for keyword in keywords:
                if keyword.lower() in string_for_searching:
                    pass
                else:
                    check_status = False
            if check_status:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    @classmethod
    def vacancies_from_hh_processing(cls, vacancies: list[dict]) -> list[dict]:
        """Приведение данных от hh к формату для дальнейшей обработки"""

        vacancies_processing = []
        for vacancy in vacancies:
            vacancy_processing = {}
            for key in cls.__slots__:
                vacancy_processing[key] = cls.__get_attribute_value_from_hh(key, vacancy)

            vacancies_processing.append(vacancy_processing)
        return vacancies_processing

    @staticmethod
    def __get_attribute_value_from_hh(attribute: str, vacancy: dict) -> Any:
        """Привязка мест хранения аттрибутов в данных от hh"""

        match attribute:
            case "id":
                return vacancy["id"]

            case "name":
                return vacancy["name"]

            case "location":
                return vacancy["area"]["name"]

            case "salary":
                if not vacancy["salary"]:
                    return 0

                if not vacancy["salary"]["from"] and not vacancy["salary"]["to"]:
                    return 0

                if not vacancy["salary"]["from"]:
                    return vacancy["salary"]["to"]

                if not vacancy["salary"]["to"]:
                    return vacancy["salary"]["from"]

                return min(vacancy["salary"]["from"], vacancy["salary"]["to"])

            case "salary_string":
                if not vacancy["salary"]:
                    return "Зарплата не указана"

                if not vacancy["salary"]["from"] and not vacancy["salary"]["to"]:
                    return "Зарплата не указана"

                if not vacancy["salary"]["from"]:
                    return f"До {vacancy["salary"]["to"]}"

                if not vacancy["salary"]["to"]:
                    return f"От {vacancy["salary"]["from"]}"

                return f"От {vacancy["salary"]["from"]} до {vacancy["salary"]["to"]}"

            case "published_at":
                return vacancy["published_at"]

            case "url":
                return vacancy["alternate_url"]

            case "name_employer":
                return vacancy["employer"]["name"]

            case "schedule":
                return vacancy["schedule"]["name"]

            case "employment":
                return vacancy["employment"]["name"]

            case "experience":
                return vacancy["experience"]["name"]

            case "requirement":
                return vacancy["snippet"]["requirement"]

            case "responsibility":
                return vacancy["snippet"]["responsibility"]

            case _:
                return None




if __name__ == '__main__':
    asd = Vacancy({
        "id": "88886759",
        "name": "Java-разработчик",
        "location": "Ярославль",
        "salary": 0,
        "salary_string": "Зарплата не указана",
        "published_at": "2024-08-08T09:53:11+0300",
        "url": "https://hh.ru/vacancy/88886759",
        "name_employer": "КРИСТА, НПО",
        "schedule": "Полный день",
        "employment": "Полная занятость",
        "experience": "Нет опыта",
        "requirement": "Опыт разработки веб-систем, знание веб-технологий. Знание <highlighttext>Java</highlighttext>. Знание одного или нескольких пунктов из следующих технологий и инструментов: Oracle...",
        "responsibility": "Участие в крупных проектах по разработке веб-систем."
    })
    print(asd.to_dict())

