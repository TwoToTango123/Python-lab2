import os
import sys
from unittest.mock import patch
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.rm import remove_file_or_directory, parse_rm_command

class TestRemoveFileOrDirectory:
    """Тесты функции remove_file_or_directory"""
    
    def test_remove_directory_without_recursive(self, capsys):
        """Попытка удалить директорию без рекурсивного флага"""
        with patch('src.rm.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.access') as mock_access, \
             patch('os.path.isfile') as mock_isfile, \
             patch('os.path.isdir') as mock_isdir:
            
            mock_expand.return_value = '/path/to/dir'
            mock_exists.return_value = True
            mock_access.return_value = True
            mock_isfile.return_value = False
            mock_isdir.return_value = True
            
            result = remove_file_or_directory('dir', recursive=False)
            
            assert result is False
            captured = capsys.readouterr()
            assert "Is a directory" in captured.out
            assert "use -r" in captured.out
    
    def test_remove_nonexistent_path(self, capsys):
        """Удаление несуществующего пути"""
        with patch('src.rm.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists:
            
            mock_expand.return_value = '/nonexistent'
            mock_exists.return_value = False
            
            result = remove_file_or_directory('nonexistent')
            
            assert result is False
            captured = capsys.readouterr()
            assert "No such file or directory" in captured.out
    
    def test_remove_file_permission_error(self, capsys):
        """Ошибка прав при удалении файла"""
        with patch('src.rm.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.access') as mock_access, \
             patch('os.path.isfile') as mock_isfile, \
             patch('os.remove') as mock_remove:
            
            mock_expand.return_value = '/protected/file.txt'
            mock_exists.return_value = True
            mock_access.return_value = True
            mock_isfile.return_value = True
            mock_remove.side_effect = PermissionError("Delete denied")
            
            result = remove_file_or_directory('protected.txt')
            
            assert result is False
            captured = capsys.readouterr()
            assert "Permission denied" in captured.out
    
    def test_remove_directory_permission_error(self, capsys):
        """Ошибка прав при удалении директории"""
        with patch('src.rm.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.access') as mock_access, \
             patch('os.path.isfile') as mock_isfile, \
             patch('os.path.isdir') as mock_isdir, \
             patch('shutil.rmtree') as mock_rmtree:
            
            mock_expand.return_value = '/protected/dir'
            mock_exists.return_value = True
            mock_access.return_value = True
            mock_isfile.return_value = False
            mock_isdir.return_value = True
            mock_rmtree.side_effect = PermissionError("Delete denied")
            
            result = remove_file_or_directory('protected', recursive=True)
            
            assert result is False
            captured = capsys.readouterr()
            assert "Permission denied" in captured.out
    
    def test_remove_root_directory_protection(self, capsys):
        """Защита от удаления корневой директории"""
        with patch('src.rm.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists:
            
            mock_expand.return_value = '/'
            mock_exists.return_value = True
            
            result = remove_file_or_directory('/')
            
            assert result is False
            captured = capsys.readouterr()
            assert "Cannot remove root directory" in captured.out
    
    def test_remove_parent_directory_protection(self, capsys):
        """Защита от удаления родительской директории"""
        with patch('src.rm.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists:
            
            mock_expand.return_value = '..'
            mock_exists.return_value = True
            
            result = remove_file_or_directory('..')
            
            assert result is False
            captured = capsys.readouterr()
            assert "Cannot remove parent directory" in captured.out

class TestParseRmCommand:
    """Тесты функции parse_rm_command"""
    
    def test_parse_rm_command_file(self):
        """Парсинг команды удаления файла"""
        path, recursive = parse_rm_command("rm file.txt")
        assert path == "file.txt"
        assert recursive is False
    
    def test_parse_rm_command_directory_with_flag(self):
        """Парсинг команды удаления директории с флагом -r"""
        path, recursive = parse_rm_command("rm -r directory")
        assert path == "directory"
        assert recursive is True