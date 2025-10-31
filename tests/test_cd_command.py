import os
import sys
from unittest.mock import patch
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.cd import (
    expand_path,
    change_directory,
    parse_cd_command,
    format_date
)

class TestExpandPath:
    """Тесты функции расширения путей"""
    
    def test_expand_path_current_directory(self):
        """Тест текущей директории"""
        with patch('os.getcwd') as mock_cwd:
            mock_cwd.return_value = '/current/path'
            
            assert expand_path('.') == '/current/path'
    
    def test_expand_path_absolute(self):
        """Тест абсолютных путей"""
        assert expand_path('/absolute/path') == '/absolute/path'
        assert expand_path('relative') == 'relative'


class TestChangeDirectory:
    """Тесты функции смены директории"""
    
    def test_change_directory_success(self):
        """Тест успешной смены директории"""
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.chdir') as mock_chdir, \
             patch('src.cd.expand_path') as mock_expand, \
             patch('src.cd.logger') as mock_logger:
            
            mock_expand.return_value = '/valid/path'
            mock_exists.return_value = True
            mock_isdir.return_value = True
            
            result = change_directory('/valid/path')
            
            assert result is True
            mock_chdir.assert_called_once_with('/valid/path')
            mock_logger.error.assert_not_called()
    
    def test_change_directory_nonexistent(self):
        """Тест несуществующей директории"""
        with patch('src.cd.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('src.cd.logger') as mock_logger:
            
            mock_expand.return_value = '/nonexistent'
            mock_exists.return_value = False
            
            result = change_directory('/nonexistent')
            
            assert result is False
            mock_logger.error.assert_called_once()
    
    def test_change_directory_not_a_directory(self):
        """Тест попытки перейти в файл"""
        with patch('src.cd.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('src.cd.logger') as mock_logger:
            
            mock_expand.return_value = '/some/file.txt'
            mock_exists.return_value = True
            mock_isdir.return_value = False
            
            result = change_directory('/some/file.txt')
            
            assert result is False
            mock_logger.error.assert_called_once()
    
    def test_change_directory_permission_denied(self):
        """Тест ошибки прав доступа"""
        with patch('src.cd.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.chdir') as mock_chdir, \
             patch('src.cd.logger') as mock_logger:
            
            mock_expand.return_value = '/protected'
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_chdir.side_effect = PermissionError("Access denied")
            
            result = change_directory('/protected')
            
            assert result is False
            mock_logger.error.assert_called_once()
    
    def test_change_directory_generic_error(self):
        """Тест общей ошибки"""
        with patch('src.cd.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.chdir') as mock_chdir, \
             patch('src.cd.logger') as mock_logger:
            
            mock_expand.return_value = '/problematic'
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_chdir.side_effect = Exception("Unexpected error")
            
            result = change_directory('/problematic')
            
            assert result is False
            mock_logger.error.assert_called_once()


class TestParseCdCommand:
    """Тесты парсинга команды cd"""
    
    def test_parse_cd_command_with_path(self):
        """Тест парсинга команды с путем"""
        assert parse_cd_command('cd /home/user') == '/home/user'
        assert parse_cd_command('cd ..') == '..'
        assert parse_cd_command('cd ~/documents') == '~/documents'
    
    def test_parse_cd_command_no_path(self):
        """Тест парсинга команды без пути"""
        assert parse_cd_command('cd') == '~'
        assert parse_cd_command('cd ') == '~'
        assert parse_cd_command('cd     ') == '~'