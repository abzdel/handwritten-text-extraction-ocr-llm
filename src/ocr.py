import os
import logging
from image_utils import convert_image_to_data_uri
from llm import llm_to_json

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def call_tesseract_api(image_path: str, replicate_api) -> str:
    """Calls Tesseract API.

    Args:
        image_path (str): Path to image.

    Returns:
        str: Extracted text.

    Raises:
        Exception: If there is an error in the API call.
    """
    try:
        image_uri = convert_image_to_data_uri(image_path)
        input_data = {"image": image_uri}
        logging.info(f"Calling Tesseract API for image: {image_path}")
        return replicate_api.run(
            "abiruyt/text-extract-ocr:a524caeaa23495bc9edc805ab08ab5fe943afd3febed884a4f3747aa32e9cd61",
            input=input_data,
        )
    except Exception as e:
        logging.error(f"Error calling Tesseract API for {image_path}: {e}")
        raise


def get_data_from_all_files(folder_path: str, replicate_api) -> list:
    """Calls Tesseract API for all files in folder.

    Args:
        folder_path (str): Path to folder.

    Returns:
        list: List of patient records in JSON format.

    Raises:
        FileNotFoundError: If the folder path does not exist.
    """
    if not os.path.exists(folder_path):
        logging.error(f"The folder path {folder_path} does not exist.")
        raise FileNotFoundError(f"The folder path {folder_path} does not exist.")

    full_output = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            try:
                text = f"original_filename: {file_name}\n"
                text += call_tesseract_api(file_path, replicate_api)
                llm_output = llm_to_json(text, replicate_api, file_path)
                full_output.append(llm_output)
            except Exception as e:
                logging.error(f"Error processing file {file_name}: {e}")
                continue  # Optionally skip this file and continue

    return full_output
