import os
from datetime import datetime
stat_info = os.stat('src\main.py')

# Размер файла в байтах
print(f"Размер: {stat_info.st_size} байт")

# Время последнего доступа
print(f"Последний доступ: {stat_info.st_atime}")

# Время последнего изменения
print(f"Последнее изменение: {stat_info.st_mtime}")

# Время создания (на некоторых системах)
print(f"Время создания: {stat_info.st_ctime}")

# ID владельца
print(f"ID владельца: {stat_info.st_uid}")

# ID группы
print(f"ID группы: {stat_info.st_gid}")

# Права доступа
print(f"Права доступа: {oct(stat_info.st_mode)}")

# Номер inode
print(f"Inode: {stat_info.st_ino}")

mod_time = datetime.fromtimestamp(stat_info.st_mtime)
print(f"Файл изменен: {mod_time}")