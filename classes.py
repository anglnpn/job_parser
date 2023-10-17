import requests
import psycopg2


class HeadHunterAPI:
    """
    Класс для получения вакансий с HeadHunter
    """

    def __init__(self):

        self.companies = [{'id': "1740", 'name': "Яндекс"},
                          {'id': "7172", 'name': "Лента"},
                          {'id': "2120", 'name': "Азбука вкуса"},
                          {'id': "2537115", 'name': "МТС"},
                          {'id': "15478", 'name': "Вконтакте"},
                          {'id': "49357", 'name': "Магнит"},
                          {'id': "1942330", 'name': "Пятерочка"},
                          {'id': "54979", 'name': "Ашан"},
                          {'id': "1634", 'name': "Оби"},
                          {'id': "1276", 'name': "Окей"}]

        self.vacancy_list = None

    def parse_vacancies(self):
        """
        Функция использует api для парсинга
        сайта hh.ru.
        Возвращает список вакансий
        """

        base_url = 'https://api.hh.ru/'
        endpoint = 'vacancies'
        vacancy_list = []

        for company in self.companies:
            """
            Определяем вводимые параметры запроса
            """
            params = {'employer_id': company["id"],
                      'per_page': 5}

            """
            Выполняем запрос к сайту по API ключу и вводным параметрам
            """
            response = requests.get(f'{base_url}{endpoint}', params=params)
            if response.status_code == 200:
                vacancies = response.json()
                for i in vacancies['items']:
                    name = i['name']
                    alternate_url = i['alternate_url']
                    payment_from = i['salary']['from'] if i['salary'] and 'from' in i['salary'] else None
                    payment_to = i['salary']['to'] if i['salary'] and 'to' in i['salary'] else None

                    if payment_from is None:
                        payment_from = 0

                    if payment_to is None:
                        payment_to = 0

                    dict_vacancy = {'company_id': company["id"], 'company_name': company['name'], 'vacancy_name': name,
                                    'payment_from': payment_from,
                                    'payment_to': payment_to, 'url': alternate_url}

                    vacancy_list.append(dict_vacancy)

            self.vacancy_list = vacancy_list

        return self.vacancy_list

