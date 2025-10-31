from src.logger import *
import os
from src.cd import expand_path
import shutil
from src.exceptions import *

def move_file_or_directory(source, destination):
    """Реализация команды mv - перемещение и переименование файлов и директорий"""
    try:
        expanded_source = expand_path(source)
        expanded_dest = expand_path(destination)
        
        if not os.path.exists(expanded_source):
            print(f"mv: {source}: No such file or directory")
            logger.error(f"Failed mv attempt: {source} -> {destination} - Source not found")
            return False
        
        if os.path.isdir(expanded_dest):
            source_name = os.path.basename(expanded_source)
            expanded_dest = os.path.join(expanded_dest, source_name)
        
        if not os.access(expanded_source, os.R_OK):
            print(f"mv: {source}: Permission denied")
            logger.error(f"Failed mv attempt: {source} - Read permission denied")
            return False
        
        try:
            shutil.move(expanded_source, expanded_dest)          
            return True
            
        except PermissionError:
            print(f"mv: {destination}: Permission denied")
            logger.error(f"Failed mv attempt: {destination} - Permission denied")
            return False
        except OSError as e:
            if "already exists" in str(e):
                print(f"mv: {destination}: File already exists")
                logger.error(f"Failed mv attempt: {destination} - File exists")
                return False
            else:
                raise e
        
    except Exception as e:
        print(f"mv: {str(e)}")
        logger.error(f"Failed mv attempt: {source} -> {destination} - {str(e)}")
        return False

def parse_mv_command(user_input):
    """Парсит команду mv и возвращает источник и назначение"""
    parts = user_input.strip().split()
    
    if len(parts) < 3:
        raise IncorrectCommandUsing("mv требует указания источника и назначения")
    
    source = parts[1]
    destination = parts[2]
    
    return source, destination
