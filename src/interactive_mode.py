from src.ls import *
from src.cd import *
from src.cat import *
from src.cp import *
from src.mv import *
from src.rm import *
from src.zip_tar import *
from src.grep import *
def show_help():
    """Показывает справку по использованию"""
    print("СПРАВКА ПО КОМАНДЕ ls:")
    print("ls                         - показать текущую директорию")
    print("ls -l [путь]               - показать файлы")
    print("ls /home/user              - показать конкретную папку")
    print("ls -l                      - подробный вывод")
    print("ls -l /path                - подробный вывод для папки")
    print("cd <путь>                  - сменить директорию")
    print("cd ~                       - перейти в домашнюю директорию")
    print("cd ..                      - перейти на уровень выше")
    print("cd ../..                   - перейти на два уровня выше")
    print("cd /absolute/path          - абсолютный путь")
    print("cd relative/path           - относительный путь")
    print("cd .                       - текущая директория (обновить)")
    print("cp file1.txt file2.txt     - копировать файл")
    print("cp -r dir1/ dir2/          - рекурсивное копирование директории")
    print("cp file.txt ~/back/        - копировать в домашнюю директорию")
    print("mv <источник> <назначение> - перемещение/переименование")
    print("rm file.txt                - удалить файл")
    print("rm -r folder/              - удалить папку с содержимым")
    print("zip <папка> <arch.zip>     - создание архива формата ZIP")
    print("unzip <arch.zip>           - распаковка архива формата ZIP в текущем каталоге")
    print("tar <папка> <arch.zip>     - создание архива формата TAR.GZ.")
    print("untar <arch.zip>           - распаковка архива формата TAR.GZ.")
    print("grep <паттерн> <путь>      - поиск строк соответсвующих шаблону <паттерн> в файлах")
    print("grep -r <паттерн> <путь>   - поиск строк соответсвующих шаблону <паттерн> в файлах с рекурсивным поиском в подкаталогах")
    print("grep -i <паттерн> <путь>   - поиск строк соответсвующих шаблону <паттерн> в файлах без учета регистра")
    print("help                       - показать эту справку")
    print("exit, quit, q              - выход")

def interactive_mode():
    """Интерактивный режим с вводом от пользователя"""
    print("Интерактивный режим включен")
    print("Введите 'help' для справки, 'exit' для выхода")
    
    while True:
        try:
            show_current_directory()
            user_input = input("Введите команду > ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Интерактивный режим выключен")
                break
            
            elif user_input.lower() == 'help':
                show_help()
            
            elif user_input.lower().startswith('cd'):
                path = parse_cd_command(user_input)
                change_directory(path)

            elif user_input.startswith('ls'):
                path, detailed = parse_ls_command(user_input)
                list_directory(path, detailed)

            elif user_input.startswith('cat'):
                path = parse_cat_command(user_input)
                cat_file(path)

            elif user_input.startswith('cp'):
                copied_item, destination_item, recursive_mode = parse_cp_command(user_input)
                copy_item(copied_item, destination_item, recursive_mode)
            
            elif user_input.startswith('mv'):
                source, destination = parse_mv_command(user_input)
                move_file_or_directory(source, destination)
            
            elif user_input.startswith('rm'):
                path, recursive = parse_rm_command(user_input)
                remove_file_or_directory(path, recursive)

            elif user_input.startswith('zip'):
                folder_path, archive_name = parse_zip_command(user_input)
                create_zip(folder_path, archive_name)
            
            elif user_input.startswith('unzip'):
                archive_path = parse_unzip_command(user_input)
                extract_zip(archive_path)
            
            elif user_input.startswith('tar'):
                folder_path, archive_name = parse_tar_command(user_input)
                create_tar(folder_path, archive_name)
            
            elif user_input.startswith('untar'):
                archive_path = parse_untar_command(user_input)
                extract_tar(archive_path)

            elif user_input.startswith('grep'):
                grep_search(user_input)

            elif not user_input:
                continue
            
            else:
                print(f"Неизвестная команда: {user_input}")
                print("Введите 'help' для просмотра доступных команд")
          
        except Exception as e:
            print(f"Произошла ошибка: {e}")