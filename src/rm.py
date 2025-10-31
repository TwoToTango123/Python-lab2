from src.logger import *
import os
from src.cd import expand_path
import shutil
from src.exceptions import *

def remove_file_or_directory(path, recursive=False):
    """Реализация команды rm - удаление файлов и директорий"""
    try:
        expanded_path = expand_path(path)
        
        if not os.path.exists(expanded_path):
            print(f"rm: {path}: No such file or directory")
            logger.error(f"Failed rm attempt: {path} - Not found")
            return False
        
        if expanded_path == '/':
            print(f"rm: {path}: Cannot remove root directory")
            logger.error(f"Failed rm attempt: {path} - Root directory protection")
            return False
        
        if expanded_path in ['..', '../'] or expanded_path.endswith('/..'):
            print(f"rm: {path}: Cannot remove parent directory")
            logger.error(f"Failed rm attempt: {path} - Parent directory protection")
            return False
        
        if not os.access(expanded_path, os.W_OK):
            print(f"rm: {path}: Permission denied")
            logger.error(f"Failed rm attempt: {path} - Permission denied")
            return False
        
        if os.path.isfile(expanded_path):
            try:
                os.remove(expanded_path)
                return True
            except PermissionError:
                print(f"rm: {path}: Permission denied")
                logger.error(f"Failed rm attempt: {path} - Delete permission denied")
                return False
        
        elif os.path.isdir(expanded_path):
            if not recursive:
                print(f"rm: {path}: Is a directory (use -r to remove recursively)")
                logger.error(f"Failed rm attempt: {path} is directory but -r flag not used")
                return False
            
            try:
                shutil.rmtree(expanded_path)
                return True
                
            except PermissionError:
                print(f"rm: {path}: Permission denied")
                logger.error(f"Failed rm attempt: {path} - Delete permission denied")
                return False
        
    except Exception as e:
        print(f"rm: {str(e)}")
        logger.error(f"Failed rm attempt: {path} - {str(e)}")
        return False

def parse_rm_command(user_input):
    """Парсит команду rm и возвращает путь и флаги"""
    parts = user_input.strip().split()
    
    if len(parts) < 2:
        print("rm требует указания пути")
        return None, False
    
    path = parts[-1]
    recursive = False
    for part in parts[1:]:
        if part == '-r':
            recursive = True
        elif part.startswith('-'):
            raise IncorrectCommandUsing(f"Неизвестная опция для rm: '{part}'")
    
    return path, recursive