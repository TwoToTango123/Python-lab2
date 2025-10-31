import os
import sys
from unittest.mock import patch, mock_open
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.cat import cat_file, parse_cat_command

class TestCatFile:
    """Тесты cat_file"""
    
    def test_cat_file_not_found(self, capsys):
        """Файл не существует"""
        with patch('src.cat.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists:
            
            mock_expand.return_value = '/nonexistent.txt'
            mock_exists.return_value = False
            
            cat_file('/nonexistent.txt')
            
            captured = capsys.readouterr()
            assert "No such file or directory" in captured.out
    
    def test_cat_is_directory(self, capsys):
        """Попытка прочитать директорию"""
        with patch('src.cat.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir:
            
            mock_expand.return_value = '/some/dir'
            mock_exists.return_value = True
            mock_isdir.return_value = True
            
            cat_file('/some/dir')
            
            captured = capsys.readouterr()
            assert "Is a directory" in captured.out
    
    def test_cat_empty_file(self, capsys):
        """Чтение пустого файла"""
        with patch('src.cat.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('builtins.open', mock_open(read_data='')):
            
            mock_expand.return_value = '/empty.txt'
            mock_exists.return_value = True
            mock_isdir.return_value = False
            
            cat_file('/empty.txt')
            
            captured = capsys.readouterr()
            assert "(файл пустой)" in captured.out
    
    def test_cat_permission_error(self, capsys):
        """Ошибка прав доступа"""
        with patch('src.cat.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('builtins.open') as mock_open_file:
            
            mock_expand.return_value = '/protected.txt'
            mock_exists.return_value = True
            mock_isdir.return_value = False
            mock_open_file.side_effect = PermissionError("Denied")
            
            cat_file('/protected.txt')
            
            captured = capsys.readouterr()
            assert "Denied" in captured.out

class TestParseCatCommand:
    """Тесты parse_cat_command"""
    
    def test_parse_valid_command(self):
        """Корректный парсинг команды"""
        assert parse_cat_command("cat file.txt") == "file.txt"
        assert parse_cat_command("cat /path/file.txt") == "/path/file.txt"
