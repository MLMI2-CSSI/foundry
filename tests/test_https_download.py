# import pytest
# from unittest.mock import patch, MagicMock
# from pathlib import Path
# import os

# from foundry.https_download import download_file, recursive_ls

# def test_download_file(tmp_path):
#     # Create source directory
#     source_dir = tmp_path / "test_id"
#     source_dir.mkdir()
    
#     item = {
#         "path": str(source_dir),
#         "name": "test.txt"
#     }
#     https_config = {
#         "base_url": "https://example.com/",
#         "source_id": "test_id"
#     }
    
#     mock_response = MagicMock()
#     mock_response.content = b"test content"
    
#     with patch('requests.get', return_value=mock_response):
#         result = download_file(item, str(tmp_path), https_config)
        
#         # Check file was created
#         expected_path = source_dir / "test.txt"
#         assert expected_path.exists()
#         with open(expected_path, 'wb') as f:
#             f.write(mock_response.content)
#         assert expected_path.read_bytes() == b"test content"
        
#         # Check return value
#         assert result == {str(expected_path) + " status": True}

# def test_recursive_ls(tmp_path):
#     # Create test directory structure
#     (tmp_path / "dir1").mkdir()
#     file1 = tmp_path / "dir1/file1.txt"
#     file1.touch()
#     (tmp_path / "dir2").mkdir()
#     file2 = tmp_path / "dir2/file2.txt"
#     file2.touch()
    
#     # Create mock endpoint
#     mock_ep = MagicMock()
#     mock_ep.ls.return_value = [
#         {"name": "file1.txt", "path": str(file1)},
#         {"name": "file2.txt", "path": str(file2)}
#     ]
    
#     files = recursive_ls(mock_ep, str(tmp_path), str(tmp_path))
#     assert len(files) == 2
#     file_names = {f["name"] for f in files}
#     assert "file1.txt" in file_names
#     assert "file2.txt" in file_names
