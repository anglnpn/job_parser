# Импорт классов
from classes import HeadHunterAPI, DMBWriteManager, DMBReadManager


def user_interaction():
    """
    Функция для работы с пользователем.
    Получает ввод данных.
    Возвращает ответ в виде списка вакансий(по заданным
    критериям), среднюю зарплату.
    Сортирует их по заданным критериям.
    """
    vacancy = None

    headhunter = HeadHunterAPI()
    job_vacancies_list = headhunter.parse_vacancies()

    write_manager = DMBWriteManager(job_vacancies_list)
    write_manager.write_to_database()

    read_manager = DMBReadManager()

    # запрос ввода у пользователя
    user_choice = int(input("Выберите действие: \n"
                            "1) Получить список всех компаний и количество вакансий у каждой компании. \n"
                            "2) Получить список всех вакансий с указанием названия компании, названия вакансии, "
                            "зарплаты и ссылки на вакансию. \n"
                            "3) Получить среднюю зарплату по вакансиям.\n"
                            "4) Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n"
                            "5) Получает список всех вакансий по заданному запросу.\n"))
    if user_choice == 1:
        vacancy = read_manager.get_companies_and_vacancies_count()
    elif user_choice == 2:
        vacancy = read_manager.get_all_vacancies()
    elif user_choice == 3:
        vacancy = read_manager.get_avg_salary()
    elif user_choice == 4:
        vacancy = read_manager.get_vacancies_with_higher_salary()
    elif user_choice == 5:
        user_input = input("Введите ключевое слово по запросу вакансий: ")
        vacancy = read_manager.get_vacancies_with_keyword(user_input)
    else:
        print("Введено недопустимое число. Программа завершается.")

    print(vacancy)


if __name__ == "__main__":
    user_interaction()


