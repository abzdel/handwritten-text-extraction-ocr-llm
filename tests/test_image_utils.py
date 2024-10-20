import os
import pytest
from src.image_utils import (
    validate_image_path,
    read_image_file,
    convert_image_to_data_uri,
)


def test_validate_image_path_valid_file():
    """Test that valid image paths do not raise exceptions."""
    valid_image_path = "test_image.jpg"
    open(valid_image_path, "a").close()  # create dummy file

    try:
        validate_image_path(valid_image_path)
    finally:
        os.remove(valid_image_path)


def test_validate_image_path_invalid_extension():
    """Test that an invalid file extension raises a ValueError."""
    with pytest.raises(ValueError):
        validate_image_path("invalid_file.txt")


def test_read_image_file_valid():
    """Test reading a valid image file."""
    valid_image_path = "test_image.jpg"
    with open(valid_image_path, "wb") as f:
        f.write(b"\xFF\xD8\xFF")  # write JPEG magic number

    try:
        result = read_image_file(valid_image_path)
        assert result == b"\xFF\xD8\xFF"  # check content
    finally:
        os.remove(valid_image_path)


def test_read_image_file_not_found():
    """Test that reading a nonexistent file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        read_image_file("nonexistent_file.jpg")


def test_convert_image_to_data_uri_jpg():
    """Test conversion of JPG image to data URI format."""
    valid_image_path = "test_image.jpg"
    with open(valid_image_path, "wb") as f:
        f.write(b"\xFF\xD8\xFF")

    try:
        result = convert_image_to_data_uri(valid_image_path)
        assert result.startswith("data:image/jpeg;base64,")
    finally:
        os.remove(valid_image_path)


def test_convert_image_to_data_uri_png():
    """Test conversion of PNG image to data URI format."""
    valid_image_path = "test_image.png"
    with open(valid_image_path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1A\n")  # PNG magic number

    try:
        result = convert_image_to_data_uri(valid_image_path)
        assert result.startswith("data:image/png;base64,")
    finally:
        os.remove(valid_image_path)


def test_convert_image_to_data_uri_invalid_file_type():
    """Test behavior when an invalid file type is passed."""
    with pytest.raises(ValueError):
        convert_image_to_data_uri("invalid_file.txt")


def test_read_image_file_empty():
    """Test reading an empty file raises ValueError."""
    valid_image_path = "test_image.jpg"
    open(valid_image_path, "wb").close()  # create empty file

    try:
        with pytest.raises(ValueError):
            read_image_file(valid_image_path)
    finally:
        os.remove(valid_image_path)
