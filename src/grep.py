from src.logger import *
from src.exceptions import *
import os
import re

def parse_grep_command(user_input):
    """Парсит команду grep и возвращает параметры поиска"""
    parts = user_input.strip().split()
    if len(parts) < 2:
        return None, None, False, False
    
    pattern = None
    path = "."
    recursive = False
    ignore_case = False
    
    non_option_parts = []
    for i, part in enumerate(parts[1:], 1):
        if part.startswith('-'):
            if part == '-r':
                recursive = True
                logger.debug("Обнаружена опция рекурсивного поиска (-r)")
            elif part == '-i':
                ignore_case = True
                logger.debug("Обнаружена опция поиска без учета регистра (-i)")
            else:
                logger.error(f"Обнаружена неизвестная опция для grep: '{part}'")
                raise IncorrectCommandUsing(f"Неизвестная опция для grep: '{part}'")
        else:
            non_option_parts.append(part)
            logger.debug(f"Добавлен неопционный аргумент: '{part}'")
    
    if len(non_option_parts) == 1:
        pattern = non_option_parts[0]
        logger.info(f"Установлен шаблон поиска: '{pattern}', путь по умолчанию: '{path}'")
    elif len(non_option_parts) >= 2:
        pattern = non_option_parts[0]
        path = non_option_parts[1]
        logger.info(f"Установлен шаблон поиска: '{pattern}', путь: '{path}'")
    else:
        logger.warning("Не удалось определить шаблон для поиска")
        print("grep требует указания шаблона для поиска")
        return None, None, False, False
    
    logger.info(f"Парсинг grep завершен: pattern='{pattern}', path='{path}', recursive={recursive}, ignore_case={ignore_case}")
    return pattern, path, recursive, ignore_case

def search_in_file(file_path, pattern, relative_path = ""):
    """Ищет паттерн в одном файле и возвращает результаты"""
    results = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line_num, line in enumerate(f, 1):
            if pattern.search(line):
                display_path = relative_path if relative_path else file_path
                results.append((display_path, line_num, line.rstrip()))
    return results

def search_in_directory(dir_path, pattern, recursive, base_path = ""):
    """Ищет паттерн во всех файлах директории"""
    results = []
    try:
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            
            if base_path:
                relative_path = os.path.relpath(item_path, base_path)
            else:
                relative_path = item_path
            
            if os.path.isfile(item_path):
                file_results = search_in_file(item_path, pattern, relative_path)
                results.extend(file_results)
            elif os.path.isdir(item_path) and recursive:
                dir_results = search_in_directory(item_path, pattern, recursive, base_path or dir_path)
                results.extend(dir_results)     
    except PermissionError as e:
        logger.error(f"Ошибка доступа к директории {dir_path}: {e}")
    
    return results

def grep_search(user_input):
    """Основная функция для поиска grep"""
    try:
        logger.info(f"Выполнение команды grep: '{user_input}'")
        
        pattern_str, path, recursive, ignore_case = parse_grep_command(user_input)
        
        if pattern_str is None:
            logger.warning("Не удалось выполнить поиск - шаблон не указан")
            return
        flags = re.IGNORECASE if ignore_case else 0
        compiled_pattern = re.compile(pattern_str, flags)
        logger.debug(f"Шаблон '{pattern_str}' успешно скомпилирован")
        
        if not os.path.exists(path):
            logger.error(f"Путь '{path}' не существует")
            print(f"Ошибка: путь '{path}' не существует")
            return
        
        results = []
        
        if os.path.isfile(path):
            results = search_in_file(path, compiled_pattern)
        elif os.path.isdir(path):
            if recursive:
                results = search_in_directory(path, compiled_pattern, recursive, path)
            else:
                results = search_in_directory(path, compiled_pattern, False, path)
        else:
            logger.error(f"Путь '{path}' не является файлом или директорией")
            print(f"Ошибка: '{path}' не является файлом или директорией")
            return
        
        if results:
            logger.info(f"Найдено {len(results)} совпадений")
            for file_path, line_num, line_content in results:
                print(f"{file_path}:{line_num}:{line_content}")
        else:
            logger.info("Совпадений не найдено")
            print("Совпадений не найдено")
            
        logger.info("Поиск grep завершен успешно")

    except Exception as e:
        logger.exception(f"Ошибка при выполнении grep: {e}")
        print(f"Произошла ошибка: {e}")