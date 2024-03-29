Проект «Парсер вакансий и работа с SQL»

## Описание программы

- В файле classes.py 3 основных класса: HeadHunterAPI, DMBWriteManager, DMBReadManager:
  - HeadHunterAPI - класс, который получает список вакансий по десяти выбранным компаниям. В этом классе описана 1 основная функция: 
    - Функция parse_vacancies парсит вакансии с сайта HeadHunter и получает список вакансий.
  - DMBWriteManager - класс, который записывает полученные данные из списка в таблицы SQL. В этом классе описана 1 основная функция: 
    - Функция write_to_database записывает данные по двум таблицам(company, vacancy, в которых 2 и 5 колонок соответственно).
  - DMBReadManager - класс, который получает необходимые данные из таблицы по выбранному пользователем запросу. В этом классе описаны 5 основных функций:
    - Функция get_companies_and_vacancies_count получает список всех компаний и количество вакансий у каждой компании.
    - Функция get_all_vacancies получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
    - Функция get_avg_salary получает среднюю зарплату по вакансиям.
    - Функция get_vacancies_with_higher_salary получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
    - Функция get_vacancies_with_keyword получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.

- В файле main.py происходит работа с пользователем:
    - В зависимости от выбора пользователя на экран будут выводиться вакансии из таблиц, соответствующие требованию запроса.


## Ожидаемое поведение
- Код будет выполняться и выводить на экран результат обращения к таблице SQL, в случае возникновения ошибки на одной 
из стадий запроса, выведется либо пустой список, не удовлетворяющий требованиям запроса, либо на экране появится ошибка: 
"Введено недопустимое число. Программа завершается.".
