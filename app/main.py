import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(__file__)))




def info():
    print("""
                Меню
-------------------------------------------
      add - Добавить новую книгу
      del - Удалить книгу по id
      find - Найти книги
      ls - Получить все книги
      update - Изменение статуса книги
      help - Повторение информации
      exit - Выход из приложения
-------------------------------------------

""")


def main():

    try:
        from app.view import View
        end_point = {
            'add': View.add_item_form_templates,
            'del': View.del_item_form_templates,
            'find': View.get_item_filter_form_templates,
            'ls': View.get_items_form_templates,
            'update': View.update_item_form_templates
        }
        info()
        while True:
            choice = input('>>')
            choice =choice.strip()
            if choice == 'help()':
                info()
                continue
            elif choice == 'exit()':
                break
            else:
                if choice not in end_point.keys():
                    print('Введено неверное значение, или ошибка в команде. Если вам нужна помощь используйте help()')
                    continue
                try:
                    end_point[choice]()
                except Exception as e:
                    print(e)
                    continue
    except FileNotFoundError:
        print('Ошибка подключения в базе данных')
        print('Выход из системы ...')


if __name__ == '__main__':
    main()
