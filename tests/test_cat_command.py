import os
import sys
from unittest.mock import patch, mock_open
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.cat import (
    cat_file,
    parse_cat_command
)

class TestCatFile:
    """Тесты основной функции cat_file"""
    
    def test_cat_file_success(self, capsys):
        """Тест успешного чтения файла"""
        test_content = "Hello, World!\nThis is test content."
        
        with patch('src.cat.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('builtins.open', mock_open(read_data=test_content)), \
             patch('src.cat.logger') as mock_logger:
            
            mock_expand.return_value = '/path/to/file.txt'
            mock_exists.return_value = True
            mock_isdir.return_value = False
            
            result = cat_file('/path/to/file.txt')
            
            assert result is None
            captured = capsys.readouterr()
            assert "Hello, World!" in captured.out
            assert "This is test content" in captured.out
            mock_logger.error.assert_not_called()
    
    def test_cat_file_empty(self, capsys):
        """Тест чтения пустого файла"""
        with patch('src.cat.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('builtins.open', mock_open(read_data='')), \
             patch('src.cat.logger') as mock_logger:
            
            mock_expand.return_value = '/path/to/empty.txt'
            mock_exists.return_value = True
            mock_isdir.return_value = False
            
            result = cat_file('/path/to/empty.txt')
            
            assert result is None
            captured = capsys.readouterr()
            assert "(файл пустой)" in captured.out
            mock_logger.error.assert_not_called()
    
    def test_cat_file_nonexistent(self, capsys):
        """Тест несуществующего файла"""
        with patch('src.cat.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('src.cat.logger') as mock_logger:
            
            mock_expand.return_value = '/nonexistent.txt'
            mock_exists.return_value = False
            
            result = cat_file('/nonexistent.txt')
            
            assert result is False
            captured = capsys.readouterr()
            assert "No such file or directory" in captured.out
            mock_logger.error.assert_called_once()
    
    def test_cat_file_directory(self, capsys):
        """Тест попытки чтения директории"""
        with patch('src.cat.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('src.cat.logger') as mock_logger:
            
            mock_expand.return_value = '/some/directory'
            mock_exists.return_value = True
            mock_isdir.return_value = True
            
            result = cat_file('/some/directory')
            
            assert result is False
            captured = capsys.readouterr()
            assert "Is a directory" in captured.out
            mock_logger.error.assert_called_once()
    
    def test_cat_file_permission_error(self, capsys):
        """Тест ошибки прав доступа"""
        with patch('src.cat.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('builtins.open') as mock_open_file, \
             patch('src.cat.logger') as mock_logger:
            
            mock_expand.return_value = '/protected/file.txt'
            mock_exists.return_value = True
            mock_isdir.return_value = False
            mock_open_file.side_effect = PermissionError("Access denied")
            
            result = cat_file('/protected/file.txt')
            
            assert result is False
            captured = capsys.readouterr()
            assert "Access denied" in captured.out or "Permission" in captured.out
            mock_logger.error.assert_called_once()
    
    def test_cat_file_generic_error(self, capsys):
        """Тест общей ошибки"""
        with patch('src.cat.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('builtins.open') as mock_open_file, \
             patch('src.cat.logger') as mock_logger:
            
            mock_expand.return_value = '/problematic/file.txt'
            mock_exists.return_value = True
            mock_isdir.return_value = False
            mock_open_file.side_effect = Exception("Unexpected error")
            
            result = cat_file('/problematic/file.txt')
            
            assert result is False
            captured = capsys.readouterr()
            assert "Unexpected error" in captured.out
            mock_logger.error.assert_called_once()

class TestParseCatCommand:
    """Тесты парсинга команды cat"""
    
    def test_parse_cat_command_valid(self):
        """Тест корректного парсинга команды"""
        assert parse_cat_command("cat file.txt") == "file.txt"
        assert parse_cat_command("cat /path/to/file.txt") == "/path/to/file.txt"
        assert parse_cat_command("cat  file_with_spaces.txt") == "file_with_spaces.txt"