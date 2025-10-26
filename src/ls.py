import os
import time
from exceptions import *
def get_file_type(file_path):
    """Определяет тип файла и возвращает соответствующий символ"""
    if os.path.islink(file_path):
        return 'l'
    elif os.path.isdir(file_path):
        return 'd'
    elif os.path.isfile(file_path):
        return '-'
    else:
        return '?'

def get_permissions(file_path):
    """Возвращает права доступа в формате rwx в порядке: владелец, группа, остальные"""
    try:
        stat_info = os.stat(file_path)
        permissions = ''
        
        permissions += 'r' if stat_info.st_mode & 0o400 else '-'
        permissions += 'w' if stat_info.st_mode & 0o200 else '-'
        permissions += 'x' if stat_info.st_mode & 0o100 else '-'
        
        permissions += 'r' if stat_info.st_mode & 0o040 else '-'
        permissions += 'w' if stat_info.st_mode & 0o020 else '-'
        permissions += 'x' if stat_info.st_mode & 0o010 else '-'
        
        permissions += 'r' if stat_info.st_mode & 0o004 else '-'
        permissions += 'w' if stat_info.st_mode & 0o002 else '-'
        permissions += 'x' if stat_info.st_mode & 0o001 else '-'
        
        return permissions
    except:
        return '?????????'

def format_size(size):
    """Форматирует размер файла в понятном виде"""
    for unit in ['B', 'K', 'M', 'G', 'T']:
        if size < 1024.0:
            if unit == 'B':
                return f"{size:4.0f} {unit}"
            else:
                return f"{size:4.1f} {unit}"
        size /= 1024.0
    return f"{size:4.1f} P"

def format_date(timestamp):
    """Форматирует дату в удобный формат"""
    return time.strftime('%b %d %H:%M', time.localtime(timestamp))

def get_detailed_info(file_path, filename):
    """Возвращает подробную информацию о файле"""
    try:
        stat_info = os.stat(file_path)
        
        file_type = get_file_type(file_path)
        permissions = get_permissions(file_path)
        size = format_size(stat_info.st_size)
        date_modified = format_date(stat_info.st_mtime)
        
        return f"{file_type}{permissions} {size} {date_modified}"
    except Exception:
        return f"?????????? ???? ??? ?? ?????? {filename}"

def list_directory(path=".", detailed=False):
    """Выводит содержимое директории"""
    try:
        abs_path = os.path.abspath(path)
        
        if not os.path.exists(abs_path):
            print(f"ls: cannot access '{path}': No such file or directory")
            return
        
        if os.path.isfile(abs_path):
            if detailed:
                print(get_detailed_info(abs_path, os.path.basename(abs_path)))
            else:
                print(os.path.basename(abs_path))
            return
        
        items = os.listdir(abs_path)
        items.sort()
        
        if not items:
            return
        
        if detailed:
            # Подробный вывод
            total_blocks = 0
            for item in items:
                item_path = os.path.join(abs_path, item)
                try:
                    total_blocks += os.stat(item_path).st_blocks
                except:
                    pass
            
            print(f"total {total_blocks // 2}")  # Блоки по 512 байт
            
            for item in items:
                item_path = os.path.join(abs_path, item)
                print(get_detailed_info(item_path, item))
        else:
            # Простой вывод (по колонкам)
            max_length = max(len(item) for item in items) + 2
            terminal_width = 80  # Стандартная ширина терминала
            
            # Вычисляем количество колонок
            num_columns = terminal_width // max_length
            if num_columns == 0:
                num_columns = 1
            
            # Выводим файлы в колонках
            for i, item in enumerate(items):
                print(item.ljust(max_length), end='')
                if (i + 1) % num_columns == 0:
                    print()
            
            # Если последняя строка не полная, добавляем перенос
            if len(items) % num_columns != 0:
                print()
                
    except PermissionError:
        print(f"ls: cannot open directory '{path}': Permission denied")
    except Exception as e:
        print(f"ls: cannot access '{path}': {e}")

def parse_ls_command(user_input):
    """Парсит команду ls и возвращает путь и флаги"""
    parts = user_input.strip().split()
    
    # Убираем 'ls' из начала команды если есть
    if parts and parts[0] == 'ls':
        parts = parts[1:]

    path = "."  # путь по умолчанию
    detailed = False  # флаг подробного вывода
    
    for part in parts:
        if part.startswith('-'):
            # Обрабатываем флаги
            if part == '-l':
                detailed = True
            else:
                raise Undefined_command_error("Неизвестная опция для ls")
        else:
            path = part
    
    return path, detailed

def show_current_directory():
    """Показывает текущую рабочую директорию"""
    print(f"\nТекущая директория: {os.getcwd()}")
