import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.mv import move_file_or_directory, parse_mv_command


class TestMoveFileOrDirectory:
    """Тесты функции move_file_or_directory"""
    
    def test_move_file_to_directory(self):
        """Перемещение файла в директорию"""
        with patch('src.mv.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.path.basename') as mock_basename, \
             patch('os.access') as mock_access, \
             patch('shutil.move') as mock_move:
            
            mock_expand.side_effect = lambda x: f"/expanded/{x}"
            mock_exists.return_value = True
            mock_isdir.side_effect = lambda x: x == '/expanded/dir'
            mock_basename.return_value = 'file.txt'
            mock_access.return_value = True
            
            result = move_file_or_directory('file.txt', 'dir')
            
            assert result is True
            mock_move.assert_called_once()
    
    def test_move_source_not_found(self, capsys):
        """Источник не существует"""
        with patch('src.mv.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists:
            
            mock_expand.side_effect = lambda x: f"/expanded/{x}"
            mock_exists.return_value = False
            
            result = move_file_or_directory('nonexistent.txt', 'dest')
            
            assert result is False
            captured = capsys.readouterr()
            assert "No such file or directory" in captured.out
    
    def test_move_permission_denied_read(self, capsys):
        """Нет прав на чтение источника"""
        with patch('src.mv.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.access') as mock_access:
            
            mock_expand.side_effect = lambda x: f"/expanded/{x}"
            mock_exists.return_value = True
            mock_isdir.return_value = False
            mock_access.return_value = False
            
            result = move_file_or_directory('protected.txt', 'dest')
            
            assert result is False
            captured = capsys.readouterr()
            assert "Permission denied" in captured.out
    
    def test_move_file_already_exists(self, capsys):
        """Файл назначения уже существует"""
        with patch('src.mv.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.access') as mock_access, \
             patch('shutil.move') as mock_move:
            
            mock_expand.side_effect = lambda x: f"/expanded/{x}"
            mock_exists.return_value = True
            mock_isdir.return_value = False
            mock_access.return_value = True
            mock_move.side_effect = OSError("File already exists")
            
            result = move_file_or_directory('file.txt', 'existing.txt')
            
            assert result is False
            captured = capsys.readouterr()
            assert "already exists" in captured.out

class TestParseMvCommand:
    """Тесты функции parse_mv_command"""
    
    def test_parse_mv_command_valid(self):
        """Корректный парсинг команды"""
        source, dest = parse_mv_command("mv file.txt newfile.txt")
        assert source == "file.txt"
        assert dest == "newfile.txt"
        
        source, dest = parse_mv_command("mv /path/src /path/dest")
        assert source == "/path/src"
        assert dest == "/path/dest"