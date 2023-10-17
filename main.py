# Импорт классов
from classes import HeadHunterAPI, DMBWriteManager, DMBReadManager


def user_interaction():
    """
    Функция для работы с пользователем.
    Получает ввод данных.
    Возвращает ответ в виде файла с вакансиями.
    Сортирует их по заданным критериям.
    """
    headhunter = HeadHunterAPI()
    prof_list = headhunter.parse_vacancies()

    write_manager = DMBWriteManager(prof_list)

    write_manager.write_to_database()
    user_input = input("Введите ключевое слово: ").title()
    read_manager = DMBReadManager(user_input)

    # a = read_manager.get_companies_and_vacancies_count()
    # b = read_manager.get_all_vacancies()
    # c = read_manager.get_avg_salary()
    # d = read_manager.get_vacancies_with_higher_salary()
    f = read_manager.get_vacancies_with_keyword()

    print(f)


if __name__ == "__main__":
    user_interaction()


