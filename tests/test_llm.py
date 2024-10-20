import pytest
from unittest.mock import MagicMock, patch
import os
from src.llm import llm_to_json


def test_llm_to_json_success(tmp_path):
    # create temporary image file
    test_image = tmp_path / "test_image.jpg"
    test_image.write_bytes(b"dummy image content")

    # mock Replicate and its stream method
    mock_replicate_api = MagicMock()
    mock_replicate_api.stream.return_value = [
        '{"original_filename": "test_image.jpg", "Patient name": "Buddy", "Species": "Dog"}'
    ]

    # call function with mocked API and test input
    text_input = "Sample veterinary record text"
    result = llm_to_json(text_input, mock_replicate_api, str(test_image))

    # expected output as a dictionary
    expected_output = {
        "original_filename": "test_image.jpg",
        "Patient name": "Buddy",
        "Species": "Dog",
    }

    assert result == expected_output


def test_llm_to_json_file_not_found():
    # mock Replicate API
    mock_replicate_api = MagicMock()

    # call function with a non-existent image file path
    text_input = "Sample text"
    non_existent_file = "non_existent_image.jpg"

    with pytest.raises(FileNotFoundError):
        llm_to_json(text_input, mock_replicate_api, non_existent_file)


def test_llm_to_json_json_decode_error(tmp_path):
    # create temporary image file
    test_image = tmp_path / "test_image.jpg"
    test_image.write_bytes(b"dummy image content")

    # mock Replicate to return invalid JSON
    mock_replicate_api = MagicMock()
    mock_replicate_api.stream.return_value = ["Invalid JSON response"]

    # call the function and expect a ValueError due to JSON decode error
    text_input = "Sample text"
    with pytest.raises(ValueError, match="Failed to parse JSON output from LLM."):
        llm_to_json(text_input, mock_replicate_api, str(test_image))


@patch(
    "os.path.isfile", return_value=True
)  # mock isfile to bypass file existence check
@patch(
    "src.llm.open", side_effect=Exception("Unexpected error")
)  # mock the open function to raise an error
def test_llm_to_json_exception(mock_open, mock_isfile, tmp_path):
    test_image = tmp_path / "test_image.jpg"

    mock_replicate_api = MagicMock()

    # call function and expect a generic exception to be raised
    text_input = "Sample text"
    with pytest.raises(Exception, match="Unexpected error"):
        llm_to_json(text_input, mock_replicate_api, str(test_image))
