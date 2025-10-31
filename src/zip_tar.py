import os
import zipfile
import tarfile
from src.logger import *
from src.cd import expand_path
from src.exceptions import *

def create_zip(folder_path, archive_name):
    """Создание ZIP архива из директории"""
    try:
        expand_folder = expand_path(folder_path)
        expand_archive = expand_path(archive_name)
        
        if not os.path.exists(expand_folder):
            print(f"zip: {folder_path}: No such file or directory")
            logger.error(f"Failed zip creation: {folder_path} -> {archive_name} - Source not found")
            return False
        
        if not os.path.isdir(expand_folder):
            print(f"zip: {folder_path}: Not a directory")
            logger.error(f"Failed zip creation: {folder_path} -> {archive_name} - Not a directory")
            return False
        
        if not os.access(expand_folder, os.R_OK):
            print(f"zip: {folder_path}: Permission denied")
            logger.error(f"Failed zip creation: {folder_path} - Read permission denied")
            return False
        
        with zipfile.ZipFile(expand_archive, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, d, files in os.walk(expand_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, expand_folder)
                    zipf.write(file_path, arcname)
        logger.info(f"zip: {expand_folder} -> {expand_archive}")
        
    except Exception as e:
        print(f"zip: {str(e)}")
        logger.error(f"Failed zip creation: {folder_path} -> {archive_name} - {str(e)}")
        return False

def extract_zip(archive_path):
    """Распаковка ZIP архива в текущую директорию"""
    try:
        expand_archive = expand_path(archive_path)
        
        if not os.path.exists(expand_archive):
            print(f"unzip: {archive_path}: No such file or directory")
            logger.error(f"Failed unzip: {archive_path} - Archive not found")
            return False
        
        if not zipfile.is_zipfile(expand_archive):
            print(f"unzip: {archive_path}: Not a ZIP archive")
            logger.error(f"Failed unzip: {archive_path} - Not a ZIP file")
            return False
        
        if not os.access(expand_archive, os.R_OK):
            print(f"unzip: {archive_path}: Permission denied")
            logger.error(f"Failed unzip: {archive_path} - Read permission denied")
            return False
        
        with zipfile.ZipFile(expand_archive, 'r') as zipf:
            zipf.extractall()
            logger.info(f"unzip: {archive_path} -> {os.getcwd()}")
        return True
        
    except Exception as e:
        print(f"unzip: {str(e)}")
        logger.error(f"Failed unzip: {archive_path} - {str(e)}")
        return False

def create_tar(folder_path, archive_name):
    """Создание TAR.GZ архива из директории"""
    try:
        expand_folder = expand_path(folder_path)
        expand_archive = expand_path(archive_name)
        
        if not os.path.exists(expand_folder):
            print(f"tar: {folder_path}: No such file or directory")
            logger.error(f"Failed tar creation: {folder_path} -> {archive_name} - Source not found")
            return False
        
        if not os.path.isdir(expand_folder):
            print(f"tar: {folder_path}: Not a directory")
            logger.error(f"Failed tar creation: {folder_path} -> {archive_name} - Not a directory")
            return False
        
        if not os.access(expand_folder, os.R_OK):
            print(f"tar: {folder_path}: Permission denied")
            logger.error(f"Failed tar creation: {folder_path} - Read permission denied")
            return False
        
        with tarfile.open(expand_archive, 'w:gz') as tar:
            tar.add(expand_folder, arcname=os.path.basename(expand_folder))

        return True
        
    except Exception as e:
        print(f"tar: {str(e)}")
        logger.error(f"Failed tar creation: {folder_path} -> {archive_name} - {str(e)}")
        return False

def extract_tar(archive_path):
    """Распаковка TAR.GZ архива в текущую директорию"""
    try:
        expand_archive = expand_path(archive_path)
        
        if not os.path.exists(expand_archive):
            print(f"untar: {archive_path}: No such file or directory")
            logger.error(f"Failed untar: {archive_path} - Archive not found")
            return False
        
        if not tarfile.is_tarfile(expand_archive):
            print(f"untar: {archive_path}: Not a TAR archive")
            logger.error(f"Failed untar: {archive_path} - Not a TAR file")
            return False
        
        if not os.access(expand_archive, os.R_OK):
            print(f"untar: {archive_path}: Permission denied")
            logger.error(f"Failed untar: {archive_path} - Read permission denied")
            return False
        
        with tarfile.open(expand_archive, 'r:gz') as tar:
            tar.extractall()
            logger.info(f"Successful untar: {archive_path} -> {os.getcwd()}")
        return True
        
    except Exception as e:
        print(f"untar: {str(e)}")
        logger.error(f"Failed untar: {archive_path} - {str(e)}")
        return False

def parse_zip_command(user_input):
    """Парсит команду zip и возвращает папку и имя архива"""
    parts = user_input.strip().split()
    
    if len(parts) < 3:
        raise IncorrectCommandUsing("zip требует указания папки и имени архива")
    
    folder = parts[1]
    archive = parts[2]
    
    if not archive.endswith('.zip'):
        archive += '.zip'
    
    return folder, archive

def parse_unzip_command(user_input):
    """Парсит команду unzip и возвращает имя архива"""
    parts = user_input.strip().split()
    
    if len(parts) < 2:
        raise IncorrectCommandUsing("unzip требует указания архива")
    
    archive = parts[1]
    
    if not archive.endswith('.zip'):
        archive += '.zip'
    
    return archive

def parse_tar_command(user_input):
    """Парсит команду tar и возвращает папку и имя архива"""
    parts = user_input.strip().split()
    
    if len(parts) < 3:
        raise IncorrectCommandUsing("требует указания папки и имени архива")
    
    folder = parts[1]
    archive = parts[2]
    
    if not archive.endswith('.tar.gz'):
        archive += '.tar.gz'
    
    return folder, archive

def parse_untar_command(user_input):
    """Парсит команду untar и возвращает имя архива"""
    parts = user_input.strip().split()
    
    if len(parts) < 2:
        raise IncorrectCommandUsing("untar требует указания архива")
    
    archive = parts[1]
    
    if not archive.endswith('.tar.gz'):
        archive += '.tar.gz'
    
    return archive