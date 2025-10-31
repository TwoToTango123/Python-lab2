import os
from src.cd import expand_path
from src.exceptions import *
from src.logger import *

def cat_file(file_path):
    try:
        expanded_path = expand_path(file_path)
        
        # Проверка существования
        if not os.path.exists(expanded_path):
            print(f"cat: {file_path}: No such file or directory")
            logger.error(f"Failed cat attempt: {file_path} - File not found")
            return False
        
        # Проверка что это файл, а не директория
        if os.path.isdir(expanded_path):
            print(f"cat: {file_path}: Is a directory")
            logger.error(f"Failed cat attempt: {file_path} - Is a directory")
            return False
        
        # Чтение и вывод содержимого
        with open(expanded_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
            
            if not content:
                print("(файл пустой)")
        
    except Exception as e:
        print(f"cat: {file_path}: {str(e)}")
        logger.error(f"Failed cat attempt: {file_path} - {str(e)}")
        return False
    
def parse_cat_command(user_input):
    parts = user_input.strip().split()
    
    if len(parts) < 2:
        raise IncorrectCommandUsing("cat требует указания файла")
    return parts[1]