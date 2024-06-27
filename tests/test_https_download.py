# import os
# import requests
# import mock

# from foundry.https_download import download_file


# def test_download_file(tmp_path):
#     item = {
#         "path": tmp_path,
#         "name": "example_file.txt"
#     }
#     data_directory = tmp_path
#     https_config = {
#         "base_url": "https://example.com/",
#         "source_id": "12345"
#     }

#     # Mock the requests.get function to return a response with content
#     with mock.patch.object(requests, "get") as mock_get:
#         mock_get.return_value.content = b"Example file content"

#         # Call the function
#         result = download_file(item, data_directory, https_config)

#         # Assert that the file was downloaded and written correctly
#         assert os.path.exists(str(tmp_path) + "/12345/example_file.txt")
#         with open(str(tmp_path) + "/12345/example_file.txt", "rb") as f:
#             assert f.read() == b"Example file content"

#         # Assert that the result is as expected
#         assert result == {str(tmp_path) + "/12345/example_file.txt status": True}


# def test_download_file_with_existing_directories(tmp_path):
#     temp_path_to_file = str(tmp_path) + '/file'
#     os.mkdir(temp_path_to_file)
#     temp_path_to_data = str(tmp_path) + '/data'
#     os.mkdir(temp_path_to_data)

#     item = {
#         "path": temp_path_to_file,
#         "name": "example_file.txt"
#     }
#     data_directory = temp_path_to_data
#     https_config = {
#         "base_url": "https://example.com/",
#         "source_id": "12345"
#     }

#     # Create the parent directories
#     os.makedirs(temp_path_to_data + "12345")

#     # Mock the requests.get function to return a response with content
#     with mock.patch.object(requests, "get") as mock_get:
#         mock_get.return_value.content = b"Example file content"

#         # Call the function
#         result = download_file(item, data_directory, https_config)

#         # Assert that the file was downloaded and written correctly
#         assert os.path.exists(temp_path_to_data + "/12345/example_file.txt")
#         with open(temp_path_to_data + "/12345/example_file.txt", "rb") as f:
#             assert f.read() == b"Example file content"

#         # Assert that the result is as expected
#         assert result == {temp_path_to_data + "/12345/example_file.txt status": True}
