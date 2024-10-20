import os
import pytest
from unittest.mock import patch, mock_open
from src.pdf_to_image import (
    create_image_path_if_not_exist,
    convert_pdf_to_image,
    convert_all_pdf_to_image,
)


@pytest.fixture
def mock_pdf_file():
    return "mock_pdf.pdf"


@pytest.fixture
def mock_image_folder():
    return "handwritten_docs/images"


def test_create_image_path_if_not_exist_creates_folder(mocker, mock_image_folder):
    mocker.patch("os.makedirs")
    mocker.patch("os.path.exists", return_value=False)

    result = create_image_path_if_not_exist(mock_image_folder)

    os.makedirs.assert_called_once_with(mock_image_folder)
    assert result == mock_image_folder


def test_create_image_path_if_not_exist_does_not_create_folder_if_exists(
    mocker, mock_image_folder
):
    mocker.patch("os.makedirs")
    mocker.patch("os.path.exists", return_value=True)

    result = create_image_path_if_not_exist(mock_image_folder)

    os.makedirs.assert_not_called()
    assert result == mock_image_folder


@patch("src.pdf_to_image.convert_pdf_to_image")
def test_convert_all_pdf_to_image(mock_convert_pdf_to_image, mock_pdf_file):
    # Arrange
    mock_folder_path = "handwritten_docs/"
    mock_files = [mock_pdf_file, "not_a_pdf.txt"]

    with patch("os.listdir", return_value=mock_files):
        # Act
        convert_all_pdf_to_image(mock_folder_path)

    # Assert
    mock_convert_pdf_to_image.assert_called_once_with(
        f"{mock_folder_path}/{mock_pdf_file}"
    )


if __name__ == "__main__":
    pytest.main()
