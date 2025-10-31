import os
from src.logger import *
from src.cd import expand_path
import shutil
from src.exceptions import *

def copy_item(origin, target, recursive_copy=False):
    """Копирует файлы и папки из исходного места в указанное"""
    try:
        full_origin_path = expand_path(origin)
        full_target_path = expand_path(target)
        
        if not os.path.exists(full_origin_path):
            print(f"cp: {origin}: No such file or directory")
            logger.error(f"Copy failed: {origin} -> {target} - Source not found")
            return False
        
        if os.path.isdir(full_target_path):
            origin_name = os.path.basename(full_origin_path)
            full_target_path = os.path.join(full_target_path, origin_name)
        
        if os.path.isfile(full_origin_path):
            try:
                shutil.copy2(full_origin_path, full_target_path)
                file_bytes = os.path.getsize(full_origin_path)
            except PermissionError:
                print(f"cp: {target}: Permission denied")
                logger.error(f"Copy failed: {target} - Access denied")
                return False
        
        elif os.path.isdir(full_origin_path):
            if not recursive_copy:
                print(f"cp: {origin}: Is a directory (use recursive copying)")
                logger.error(f"Copy failed: {origin} is folder but -r flag missing")
                return False
            
            try:
                shutil.copytree(full_origin_path, full_target_path)
                return True
                
            except FileExistsError:
                print(f"cp: {target}: Directory already exists")
                logger.error(f"Copy failed: {target} - Folder exists")
                return False
            except PermissionError:
                print(f"cp: {target}: Permission denied")
                logger.error(f"Copy failed: {target} - Access denied")
                return False
        
    except Exception as e:
        print(f"cp: {str(e)}")
        logger.error(f"Copy failed: {origin} -> {target} - {str(e)}")
        return False

def parse_cp_command(user_input):
    """Разбирает команду копирования и возвращает параметры"""
    words = user_input.strip().split()
    
    if len(words) < 3:
        print("Команда cp требует указания что копировать и куда")
        return None, None, False
    
    copied_item = words[-2]
    destination_item = words[-1]
    recursive_mode = False
    
    for word in words[1:]:
        if word == '-r':
            recursive_mode = True
        elif word.startswith('-'):
            raise IncorrectCommandUsing(f"Неизвестная опция для cp: '{word}'")
    if '-r' in words:
        recursive_mode = True
    
    return copied_item, destination_item, recursive_mode