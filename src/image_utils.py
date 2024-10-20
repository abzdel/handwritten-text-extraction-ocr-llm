import base64
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


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
    if not os.path.isfile(image_path):
        logging.error(f"The file {image_path} does not exist.")
        raise FileNotFoundError(f"The file {image_path} does not exist.")

    mime_type = None
    if image_path.lower().endswith((".jpg", ".jpeg")):
        mime_type = "image/jpeg"
    elif image_path.lower().endswith(".png"):
        mime_type = "image/png"
    else:
        logging.error(f"Unsupported image format for file {image_path}.")
        raise ValueError(f"Unsupported image format for file {image_path}.")

    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            base64_encoded_data = base64.b64encode(image_data).decode("utf-8")
            data_uri = f"data:{mime_type};base64,{base64_encoded_data}"
            return data_uri
    except Exception as e:
        logging.error(f"Error reading file {image_path}: {e}")
        raise
