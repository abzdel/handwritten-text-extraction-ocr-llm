import os
import pytest
from unittest.mock import MagicMock, patch
from src.ocr import call_tesseract_api, get_data_from_all_files


def test_call_tesseract_api_success(tmp_path):
    """Test that call_tesseract_api returns extracted text when the API call is successful."""
    # create a temporary image file
    test_image = tmp_path / "test_image.jpg"
    test_image.write_bytes(b"dummy image content")

    # mock Replicate API
    mock_replicate_api = MagicMock()
    mock_replicate_api.run.return_value = "extracted text from image"

    # call the function and check the result
    result = call_tesseract_api(str(test_image), mock_replicate_api)
    assert result == "extracted text from image"


def test_call_tesseract_api_failure(tmp_path):
    """Test that call_tesseract_api raises an exception when the API call fails."""
    test_image = tmp_path / "test_image.jpg"
    test_image.write_bytes(b"dummy image content")

    # mock Replicate API to raise an error
    mock_replicate_api = MagicMock()
    mock_replicate_api.run.side_effect = Exception("API call failed")

    # expect an exception to be raised
    with pytest.raises(Exception, match="API call failed"):
        call_tesseract_api(str(test_image), mock_replicate_api)


def test_get_data_from_all_files_success(tmp_path):
    """Test that get_data_from_all_files processes all files successfully."""
    # create a temporary folder with image files
    os.makedirs(tmp_path, exist_ok=True)
    test_image_1 = tmp_path / "test_image_1.jpg"
    test_image_1.write_bytes(b"dummy image content 1")
    test_image_2 = tmp_path / "test_image_2.jpg"
    test_image_2.write_bytes(b"dummy image content 2")

    # mock Replicate API
    mock_replicate_api = MagicMock()
    mock_replicate_api.run.return_value = "extracted text"
    mock_replicate_api.run.return_value = "extracted text from image"

    # mock llm_to_json
    with patch("src.ocr.llm_to_json") as mock_llm_to_json:
        mock_llm_to_json.return_value = {"result": "mocked json output"}

        # call the function and check the output
        result = get_data_from_all_files(str(tmp_path), mock_replicate_api)
        expected_output = [
            {"result": "mocked json output"},
            {"result": "mocked json output"},
        ]
        assert result == expected_output


def test_get_data_from_all_files_folder_not_found():
    """Test that get_data_from_all_files raises a FileNotFoundError if the folder does not exist."""
    mock_replicate_api = MagicMock()
    non_existent_folder = "non_existent_folder"

    with pytest.raises(
        FileNotFoundError,
        match=f"The folder path {non_existent_folder} does not exist.",
    ):
        get_data_from_all_files(non_existent_folder, mock_replicate_api)
