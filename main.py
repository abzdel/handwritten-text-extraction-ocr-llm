import os
import json
import replicate
from src.image_utils import convert_image_to_data_uri
from src.ocr import call_tesseract_api, get_data_from_all_files
from src.llm import llm_to_json


def main() -> None:
    """Driver function"""
    replicate_api = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])

    # Get data from all files in folder
    full_json_data = get_data_from_all_files("handwritten_docs/images", replicate_api)

    # Write the full JSON file to disk
    with open("output_pet_records.json", "w") as json_file:
        json.dump(full_json_data, json_file, indent=4)


if __name__ == "__main__":
    main()
