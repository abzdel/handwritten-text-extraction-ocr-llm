import json
import os
from src.logging_config import logging


def llm_to_json(text_input: str, replicate_api, image_file_path: str) -> list:
    """Converts text to JSON using LLM.

    Args:
        text_input (str): Text to pass to LLM - output of our OCR model's reading of the image.

    Returns:
        list: List of patient records in JSON format.

    Raises:
        FileNotFoundError: If the image file does not exist.
        Exception: If there is an error in the API call or JSON parsing.
    """
    input_data = {
        "top_p": 0.9,
        "prompt": f"""
        Process the following text file and extract information to JSON format: 
        The text contains veterinary records for a single pet. Each record includes details such as:
        - original_filename (this is important - include it for every record, even if other fields are missing)
        - Patient name
        - Species
        - Breed
        - Age
        - Owner name
        - Visit date
        - Notes
        - Procedures with costs
        - Total costs
        - Veterinarian name
        
        Please ensure the JSON output includes fields for each of the above details and handle variations in formatting or potential typos.
        If a field cannot be found, fill it in with null. Here is the text: {text_input}. Only return the JSON output - there should be absolutely
        no other commentary as part of your response.
        """,
        "min_tokens": 0,
        "temperature": 0.6,
        "presence_penalty": 1.15,
    }

    if not os.path.isfile(image_file_path):
        logging.error(f"The file {image_file_path} does not exist.")
        raise FileNotFoundError(f"The file {image_file_path} does not exist.")

    llm_output_parts = []
    try:
        with open(image_file_path, "rb") as image_file:
            for event in replicate_api.stream(
                "meta/meta-llama-3-70b-instruct",
                input={**input_data, "image": image_file},
            ):
                llm_output_parts.append(str(event))

        llm_output = "".join(llm_output_parts)

        try:
            return json.loads(llm_output)
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON output: {e}")
            raise ValueError("Failed to parse JSON output from LLM.")
    except Exception as e:
        logging.error(f"Error processing image file {image_file_path}: {e}")
        raise
