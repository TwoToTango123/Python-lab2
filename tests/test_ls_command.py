import pytest
import sys
import os
from unittest.mock import Mock, patch
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
from src.ls import (
    get_file_type,
    get_permissions,
    format_size,
    get_detailed_info,
    list_directory,
    parse_ls_command
)

class TestCoreFunctionality:
    """Тесты основной функциональности"""
    
    def test_get_file_type_basic(self):
        """Тест определения основных типов файлов"""
        with patch('os.path.islink') as mock_islink, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.path.isfile') as mock_isfile:
            
            mock_islink.return_value = False
            mock_isdir.return_value = False
            mock_isfile.return_value = True
            assert get_file_type('/file.txt') == '-'
            
            mock_isdir.return_value = True
            mock_isfile.return_value = False
            assert get_file_type('/dir') == 'd'
            
            mock_islink.return_value = True
            mock_isdir.return_value = False
            assert get_file_type('/link') == 'l'
    
    def test_get_permissions_basic(self):
        """Тест получения прав доступа"""
        mock_stat = Mock()
        mock_stat.st_mode = 0o644
        
        with patch('os.stat', return_value=mock_stat):
            permissions = get_permissions('/file.txt')
            assert permissions == 'rw-r--r--'
    
    def test_format_size_basic(self):
        """Тест форматирования размеров"""
        assert "B" in format_size(100)
        assert "K" in format_size(2048)
        assert "M" in format_size(1572864)

class TestListDirectory:
    """Тесты функции list_directory"""
    
    def test_list_directory_file(self, capsys):
        """Тест вывода информации о файле"""
        with patch('os.path.abspath', return_value='/file.txt'), \
             patch('os.path.exists', return_value=True), \
             patch('os.path.isfile', return_value=True), \
             patch('os.path.basename', return_value='file.txt'):
            
            list_directory('/file.txt', detailed=False)
            captured = capsys.readouterr()
            assert 'file.txt' in captured.out
    
    def test_list_directory_nonexistent(self, capsys):
        """Тест несуществующего пути"""
        with patch('os.path.exists', return_value=False):
            list_directory('/nonexistent')
            captured = capsys.readouterr()
            assert 'No such file or directory' in captured.out
    
    def test_list_directory_simple(self, capsys):
        """Тест простого вывода директории"""
        with patch('os.path.abspath', return_value='/test'), \
             patch('os.path.exists', return_value=True), \
             patch('os.path.isfile', return_value=False), \
             patch('os.listdir', return_value=['file1.txt', 'file2.py']):
            
            list_directory('/test', detailed=False)
            captured = capsys.readouterr()
            assert 'file1.txt' in captured.out
            assert 'file2.py' in captured.out

class TestParseLsCommand:
    """Тесты парсинга команды ls"""
    
    def test_basic_commands(self):
        """Тест базовых команд"""
        assert parse_ls_command('ls') == ('.', False)
        assert parse_ls_command('ls /home') == ('/home', False)
        assert parse_ls_command('ls -l') == ('.', True)
        assert parse_ls_command('ls /home -l') == ('/home', True)
    
    def test_unknown_flag(self):
        """Тест неизвестного флага"""
        with pytest.raises(Exception, match="Неизвестная опция"):
            parse_ls_command('ls -a')

class TestErrorHandling:
    """Тесты обработки ошибок"""
    
    def test_permission_error(self, capsys):
        """Тест ошибки прав доступа"""
        with patch('os.path.abspath', return_value='/protected'), \
             patch('os.path.exists', return_value=True), \
             patch('os.path.isfile', return_value=False), \
             patch('os.listdir', side_effect=PermissionError):
            
            list_directory('/protected')
            captured = capsys.readouterr()
            assert 'Permission denied' in captured.out
    
    def test_generic_error(self, capsys):
        """Тест общей ошибки"""
        with patch('os.path.abspath', return_value='/test'), \
             patch('os.path.exists', return_value=True), \
             patch('os.path.isfile', return_value=False), \
             patch('os.listdir', side_effect=Exception("Unexpected")):
            
            list_directory('/test')
            captured = capsys.readouterr()
            assert 'cannot access' in captured.out