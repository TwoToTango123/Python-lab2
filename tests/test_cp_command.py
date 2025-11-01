import os
import sys
from unittest.mock import patch
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.cp import copy_item, parse_cp_command

class TestCopyItem:
    """Тесты copy_item с использованием моков"""
     
    def test_copy_nonexistent_source(self, capsys):
        """Копирование несуществующего файла"""
        with patch('src.cp.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists:
            
            mock_expand.side_effect = lambda x: f"/expanded/{x}"
            mock_exists.return_value = False
            
            result = copy_item("nonexistent.txt", "target")
            
            assert result == False
            captured = capsys.readouterr()
            assert "No such file or directory" in captured.out
    
    def test_copy_directory_with_recursive(self):
        """Рекурсивное копирование директории"""
        with patch('src.cp.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.path.isfile') as mock_isfile, \
             patch('shutil.copytree') as mock_copytree, \
             patch('os.path.basename') as mock_basename, \
             patch('os.path.join') as mock_join:
            
            mock_expand.side_effect = lambda x: f"/expanded/{x}"
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_isfile.return_value = False
            mock_basename.return_value = "source_dir"
            mock_join.return_value = "/expanded/target/source_dir"
            
            result = copy_item("source_dir", "target", recursive_copy=True)
            
            assert result == True
            mock_copytree.assert_called_once_with("/expanded/source_dir", "/expanded/target/source_dir")
    
    def test_copy_to_existing_directory(self, capsys):
        """Копирование в существующую директорию"""
        with patch('src.cp.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.path.isfile') as mock_isfile, \
             patch('shutil.copytree') as mock_copytree:
            
            mock_expand.side_effect = lambda x: f"/expanded/{x}"
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_isfile.return_value = False
            mock_copytree.side_effect = FileExistsError("Directory exists")
            
            result = copy_item("source_dir", "target", recursive_copy=True)
            
            assert result == False
            captured = capsys.readouterr()
            assert "Directory already exists" in captured.out
    
    def test_copy_file_permission_error(self, capsys):
        """Ошибка прав доступа при копировании файла"""
        with patch('src.cp.expand_path') as mock_expand, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.path.isfile') as mock_isfile, \
             patch('shutil.copy2') as mock_copy:
            
            mock_expand.side_effect = lambda x: f"/expanded/{x}"
            mock_exists.return_value = True
            mock_isdir.return_value = False
            mock_isfile.return_value = True
            mock_copy.side_effect = PermissionError("Access denied")
            
            result = copy_item("source.txt", "target.txt")
            
            assert result == False
            captured = capsys.readouterr()
            assert "Permission denied" in captured.out

class TestParseCpCommand:
    """Тесты parse_cp_command с использованием моков"""
    
    def test_parse_valid_command(self):
        """Корректный парсинг команды без флагов"""
        source, target, recursive = parse_cp_command("cp file.txt destination/")
        
        assert source == "file.txt"
        assert target == "destination/"
        assert recursive == False
    
    def test_parse_recursive_command(self):
        """Корректный парсинг команды с флагом -r"""
        source, target, recursive = parse_cp_command("cp -r dir/ destination/")
        
        assert source == "dir/"
        assert target == "destination/"
        assert recursive == True
    
    def test_parse_insufficient_arguments(self, capsys):
        """Парсинг команды с недостаточным количеством аргументов"""
        result = parse_cp_command("cp file.txt")
        
        assert result == (None, None, False)
        captured = capsys.readouterr()
        assert "Команда cp требует указания что копировать и куда" in captured.out
    
    def test_parse_empty_command(self, capsys):
        """Парсинг пустой команды"""
        result = parse_cp_command("cp")
        
        assert result == (None, None, False)
        captured = capsys.readouterr()
        assert "Команда cp требует указания что копировать и куда" in captured.out