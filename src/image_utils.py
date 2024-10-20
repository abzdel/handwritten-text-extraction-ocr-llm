import base64
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def validate_image_path(image_path: str) -> None:
    """Validates the existence and format of the image file.

    Args:
        image_path (str): Path to the image.

    Raises:
        FileNotFoundError: If the image file does not exist.
        IsADirectoryError: If the path is a directory.
        ValueError: If the image format is unsupported.
    """
    if not image_path.lower().endswith((".jpg", ".jpeg", ".png")):
        logging.error(f"Unsupported image format for file {image_path}.")
        raise ValueError(f"Unsupported image format for file {image_path}.")

    if not os.path.exists(image_path):
        logging.error(f"The file {image_path} does not exist.")
        raise FileNotFoundError(f"The file {image_path} does not exist.")

    if os.path.isdir(image_path):
        logging.error(f"The path {image_path} is a directory, not a file.")
        raise IsADirectoryError(f"The path {image_path} is a directory, not a file.")


def read_image_file(image_path: str) -> bytes:
    """Reads the image file content.

    Args:
        image_path (str): Path to the image file.

    Returns:
        bytes: Image file content.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty.
    """
    if not os.path.exists(image_path):
        logging.error(f"The file {image_path} does not exist.")
        raise FileNotFoundError(f"The file {image_path} does not exist.")

    with open(image_path, "rb") as f:
        data = f.read()
        if not data:
            logging.error(f"The file {image_path} is empty.")
            raise ValueError(f"The file {image_path} is empty.")
        return data


def get_mime_type(image_path: str) -> str:
    """Gets the MIME type based on the file extension.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: MIME type of the image.
    """
    if image_path.lower().endswith((".jpg", ".jpeg")):
        return "image/jpeg"
    elif image_path.lower().endswith(".png"):
        return "image/png"
    else:
        logging.error(f"Unsupported image format for file {image_path}.")
        raise ValueError(f"Unsupported image format for file {image_path}.")


def convert_image_to_data_uri(image_path: str) -> str:
    """Converts image to data URI for the replicate API.

    Args:
        image_path (str): Path to image.

    Returns:
        str: Data URI.

    Raises:
        FileNotFoundError: If the image file does not exist.
        ValueError: If the image format is unsupported.
    """
    validate_image_path(image_path)
    mime_type = get_mime_type(image_path)
    image_data = read_image_file(image_path)

    base64_encoded_data = base64.b64encode(image_data).decode("utf-8")
    return f"data:{mime_type};base64,{base64_encoded_data}"
