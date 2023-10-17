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


class DMBWriteManager:
    """
    Класс для записи данных в БД
    При создании экземпляра в него приходит аргумент - список вакансий
    """

    def __init__(self, vacancy_list):
        self.vacancy_list = vacancy_list

    def write_to_database(self):
        """
        Метод для записи данных из списка вакансий в базу данных
        """
        with psycopg2.connect(host="localhost", database="parsing_hh_company", user="postgres",
                              password="gdfggta56") as conn:
            with conn.cursor() as cur:
                cur.execute("TRUNCATE TABLE vacancy ")

                for item in self.vacancy_list:
                    cur.execute("INSERT INTO company (company_id, company_name) VALUES (%s, %s)"
                                "ON CONFLICT (company_id) DO NOTHING;",
                                (int(item["company_id"]), item["company_name"]))

                    cur.execute("INSERT INTO vacancy (company_id, vacancy_name, payment_from, payment_to, url)"
                                "VALUES (%s, %s, %s, %s, %s)"
                                "ON CONFLICT (url) DO NOTHING;",
                                (int(item["company_id"]), item["vacancy_name"], item["payment_from"],
                                 item["payment_to"], item["url"]))

            conn.commit()


class DMBReadManager:
    """
    Класс для получения данных из БД
    """

    def __init__(self, word):
        self.conn = psycopg2.connect(host="localhost", database="parsing_hh_company", user="postgres",
                                     password="gdfggta56")
        self.word = word

    def get_companies_and_vacancies_count(self):
        """
        Подключается к БД.
        Возвращает список всех компаний и количество вакансий у каждой компании.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT company_name, COUNT(vacancy.company_id) FROM company "
                    "INNER JOIN vacancy USING(company_id) "
                    "GROUP BY company_name ")
        rows = cur.fetchall()
        cur.close()
        self.conn.close()
        return rows

    def get_all_vacancies(self):
        """
        Подключается к БД.
        Возвращает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """
        cur = self.conn.cursor()
        cur.execute("SELECT company.company_name, vacancy_name, payment_from, payment_to, url FROM company "
                    "INNER JOIN vacancy USING(company_id) "
                    "GROUP BY company.company_name, vacancy_name, payment_from, payment_to, url "
                    "ORDER BY company_name ")
        rows = cur.fetchall()
        cur.close()
        self.conn.close()
        return rows

    def get_avg_salary(self):
        """
        Подключается к БД.
        Возвращает среднюю зарплату по вакансиям.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT ROUND(AVG(payment_from)) FROM vacancy "
                    "WHERE payment_from > 0 ")
        rows_1 = cur.fetchall()
        cur.execute("SELECT ROUND(AVG(payment_to)) FROM vacancy "
                    "WHERE payment_to > 0 ")
        rows_2 = cur.fetchall()
        cur.close()
        self.conn.close()
        return rows_1, rows_2

    def get_vacancies_with_higher_salary(self):
        """
        Подключается к БД.
        Возвращает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM vacancy WHERE payment_to > (SELECT AVG(payment_to)"
                    "FROM vacancy WHERE payment_to > 0) ")
        rows = cur.fetchall()
        cur.close()
        self.conn.close()
        return rows

    def get_vacancies_with_keyword(self):
        """
        Подключается к БД.
        Возвращает список всех вакансий,
        в названии которых содержатся переданные в метод слова, например python
        """
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM vacancy WHERE vacancy_name LIKE '%{self.word}%' ")
        rows = cur.fetchall()
        cur.close()
        self.conn.close()
        return rows

