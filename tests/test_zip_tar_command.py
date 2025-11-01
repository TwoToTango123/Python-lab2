import os
import sys
from unittest.mock import patch
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.zip_tar import (
    create_zip, extract_zip, create_tar, extract_tar,
    parse_zip_command, parse_unzip_command, parse_tar_command, parse_untar_command
)

class TestCreateZip:
    """Тесты функции create_zip"""
    
    def test_create_zip_source_not_found(self, capsys):
        """Источник не существует"""
        with patch('src.zip_tar.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists:
            
            mock_expand.side_effect = lambda x: f"/expanded/{x}"
            mock_exists.return_value = False
            
            result = create_zip('nonexistent', 'zip_tar.zip')
            
            assert result is False
    
    def test_create_zip_not_directory(self, capsys):
        """Источник не является директорией"""
        with patch('src.zip_tar.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir:
            
            mock_expand.side_effect = lambda x: f"/expanded/{x}"
            mock_exists.return_value = True
            mock_isdir.return_value = False
            
            result = create_zip('file.txt', 'zip_tar.zip')
            
            assert result is False
    
    def test_create_zip_permission_denied(self, capsys):
        """Нет прав на чтение источника"""
        with patch('src.zip_tar.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.access') as mock_access:
            
            mock_expand.side_effect = lambda x: f"/expanded/{x}"
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_access.return_value = False
            
            result = create_zip('folder', 'zip_tar.zip')
            
            assert result is False

class TestExtractZip:
    """Тесты функции extract_zip"""
    
    def test_extract_zip_not_found(self, capsys):
        """Архив не существует"""
        with patch('src.zip_tar.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists:
            
            mock_expand.return_value = '/expanded/nonexistent.zip'
            mock_exists.return_value = False
            
            result = extract_zip('nonexistent.zip')
            
            assert result is False
    
    def test_extract_zip_not_zip_file(self, capsys):
        """Файл не является ZIP архивом"""
        with patch('src.zip_tar.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('zipfile.is_zipfile') as mock_is_zip:
            
            mock_expand.return_value = '/expanded/not_zip.txt'
            mock_exists.return_value = True
            mock_is_zip.return_value = False
            
            result = extract_zip('not_zip.txt')
            
            assert result is False
    
    def test_extract_zip_permission_denied(self, capsys):
        """Нет прав на чтение архива"""
        with patch('src.zip_tar.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('zipfile.is_zipfile') as mock_is_zip, \
             patch('os.access') as mock_access:
            
            mock_expand.return_value = '/expanded/protected.zip'
            mock_exists.return_value = True
            mock_is_zip.return_value = True
            mock_access.return_value = False
            
            result = extract_zip('protected.zip')
            
            assert result is False

class TestCreateTar:
    """Тесты функции create_tar"""
    
    def test_create_tar_source_not_found(self, capsys):
        """Источник не существует"""
        with patch('src.zip_tar.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists:
            
            mock_expand.side_effect = lambda x: f"/expanded/{x}"
            mock_exists.return_value = False
            
            result = create_tar('nonexistent', 'zip_tar.tar.gz')
            
            assert result is False

class TestExtractTar:
    """Тесты функции extract_tar"""
    
    def test_extract_tar_not_tar_file(self, capsys):
        """Файл не является TAR архивом"""
        with patch('src.zip_tar.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('tarfile.is_tarfile') as mock_is_tar:
            
            mock_expand.return_value = '/expanded/not_tar.txt'
            mock_exists.return_value = True
            mock_is_tar.return_value = False
            
            result = extract_tar('not_tar.txt')
            
            assert result is False

class TestParseZipCommands:
    """Тесты парсинга ZIP команд"""
    
    def test_parse_zip_command_valid(self):
        """Корректный парсинг команды zip"""
        folder, zip_tar = parse_zip_command("zip folder zip_tar")
        assert folder == "folder"
        assert zip_tar == "zip_tar.zip"
    
    def test_parse_zip_command_with_extension(self):
        """Парсинг команды zip с указанием расширения"""
        folder, zip_tar = parse_zip_command("zip folder zip_tar.zip")
        assert folder == "folder"
        assert zip_tar == "zip_tar.zip"
    
    def test_parse_unzip_command_valid(self):
        """Корректный парсинг команды unzip"""
        zip_tar = parse_unzip_command("unzip zip_tar")
        assert zip_tar == "zip_tar.zip"
    
    def test_parse_unzip_command_with_extension(self):
        """Парсинг команды unzip с указанием расширения"""
        zip_tar = parse_unzip_command("unzip zip_tar.zip")
        assert zip_tar == "zip_tar.zip"

class TestParseTarCommands:
    """Тесты парсинга TAR команд"""
    
    def test_parse_tar_command_valid(self):
        """Корректный парсинг команды tar"""
        folder, zip_tar = parse_tar_command("tar folder zip_tar")
        assert folder == "folder"
        assert zip_tar == "zip_tar.tar.gz"
    
    def test_parse_tar_command_with_extension(self):
        """Парсинг команды tar с указанием расширения"""
        folder, zip_tar = parse_tar_command("tar folder zip_tar.tar.gz")
        assert folder == "folder"
        assert zip_tar == "zip_tar.tar.gz"
    
    def test_parse_untar_command_valid(self):
        """Корректный парсинг команды untar"""
        zip_tar = parse_untar_command("untar zip_tar")
        assert zip_tar == "zip_tar.tar.gz"
    
    def test_parse_untar_command_with_extension(self):
        """Парсинг команды untar с указанием расширения"""
        zip_tar = parse_untar_command("untar zip_tar.tar.gz")
        assert zip_tar == "zip_tar.tar.gz"