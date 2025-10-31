import os
import time
from src.logger import *
def format_date(timestamp):
    """Форматирует дату в удобный формат"""
    return time.strftime('%b %d %H:%M', time.localtime(timestamp))

def expand_path(path):
    """Расширяет специальные символы в пути (~, .., .)"""
    if path == '~' or path.startswith('~/'):
        home_dir = os.path.expanduser('~')
        if path == '~':
            return home_dir
        else:
            return os.path.join(home_dir, path[2:])
    
    if path.startswith('../'):
        return os.path.abspath(os.path.join(os.getcwd(), path))
    elif path == '..':
        return os.path.abspath(os.path.join(os.getcwd(), '..'))
    elif path == '.':
        return os.getcwd()
    elif path.startswith('./'):
        return os.path.abspath(os.path.join(os.getcwd(), path[2:]))
    
    return path

def change_directory(path):
    """Реализация команды cd с поддержкой специальных символов и логированием"""
    try:
        expanded_path = expand_path(path)
        
        if not os.path.exists(expanded_path):
            print(f"cd: {path}: No such file or directory")
            logger.error(f"Failed cd attempt: {path} -> {expanded_path} - Directory not found")
            return False
        
        if not os.path.isdir(expanded_path):
            print(f"cd: {path}: Not a directory")
            logger.error(f"Failed cd attempt: {path} -> {expanded_path} - Not a directory")
            return False
        
        os.chdir(expanded_path)
        return True
        
    except PermissionError:
        print(f"cd: {path}: Permission denied")
        logger.error(f"Failed cd attempt: {path} - Permission denied")
        return False
    except Exception as e:
        print(f"cd: {path}: {e}")
        logger.error(f"Failed cd attempt: {path} - {str(e)}")
        return False
    
def parse_cd_command(user_input):
    """Парсит команду cd и возвращает путь"""
    parts = user_input.strip().split()
    if len(parts) < 2:
        return "~"
    
    return parts[1]