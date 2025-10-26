from ls import *
from cd import *
from cat import *
def show_help():
    """Показывает справку по использованию"""
    print("СПРАВКА ПО КОМАНДЕ ls:")
    print("ls                      - показать текущую директорию")
    print("ls -l [путь]            - показать файлы")
    print("ls /home/user           - показать конкретную папку")
    print("ls -l                   - подробный вывод")
    print("ls -l /path             - подробный вывод для папки")
    print("cd <путь>               - сменить директорию")
    print("cd ~                    - перейти в домашнюю директорию")
    print("cd ..                   - перейти на уровень выше")
    print("cd ../..                - перейти на два уровня выше")
    print("cd /absolute/path       - абсолютный путь")
    print("cd relative/path        - относительный путь")
    print("cd .                    - текущая директория (обновить)")
    print("help                    - показать эту справку")
    print("exit, quit, q           - выход")

def interactive_mode():
    """Интерактивный режим с вводом от пользователя"""
    print("Интерактивный режим включен")
    print("Введите 'help' для справки, 'exit' для выхода")
    
    while True:
        try:
            # Показываем приглашение для ввода
            show_current_directory()
            user_input = input("Введите команду > ").strip()
            
            # Выход из программы
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Интерактивный режим выключен")
                break
            
            # Показать справку
            elif user_input.lower() == 'help':
                show_help()
            
            # Смена директории
            elif user_input.lower().startswith('cd '):
                path = user_input[3:].strip()
                if path:
                    change_directory(path)
                else:
                    print("Ошибка: Укажите путь для cd")
            
            # Команда ls (должна начинаться с ls)
            elif user_input.startswith('ls'):
                path, detailed = parse_ls_command(user_input)
                list_directory(path, detailed)

            elif user_input.startswith('cat'):
                path = parse_cat_command(user_input)
                cat_file(path)
            
            # Пустая команда - игнорируем
            elif not user_input:
                continue
            
            # Неизвестная команда
            else:
                print(f"Неизвестная команда: {user_input}")
                print("Введите 'help' для просмотра доступных команд")
          
        except Exception as e:
            print(f"Произошла ошибка: {e}")