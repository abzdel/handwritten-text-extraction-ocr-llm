import replicate
import os
import base64
import re
import json


def convert_image_to_data_uri(image_path: str) -> str:
    """Converts image to data uri for replicate API

    Args:
        image_path (str): path to image

    Returns:
        str: data uri
    """

    # open image, convert to base64
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        # encode binary data to base64
        base64_encoded_data = base64.b64encode(image_data).decode("utf-8")
        # determine MIME type based on the file extension
        mime_type = (
            "image/jpeg"
            if image_path.lower().endswith(".jpg")
            or image_path.lower().endswith(".jpeg")
            else "image/png"
        )
        # cnstruct data URI to be passed to replicate
        data_uri = f"data:{mime_type};base64,{base64_encoded_data}"
        return data_uri


def call_tesseract_api(image_path: str, replicate_api: str) -> str:
    """Calls Tesseract API

    Args:
        image_path (str): path to image

    Returns:
        str: text
    """

    # load image
    image_uri = convert_image_to_data_uri(image_path)

    # prepare input for the model
    input_data = {"image": image_uri}

    # call Tesseract API
    # Run the OCR model
    return replicate_api.run(
        "abiruyt/text-extract-ocr:a524caeaa23495bc9edc805ab08ab5fe943afd3febed884a4f3747aa32e9cd61",
        input=input_data,
    )


def get_data_from_all_files(folder_path: str, replicate_api: str) -> tuple[str, list]:
    """Calls Tesseract API for all files in folder

    Args:
        folder_path (str): path to folder

    Returns:
        str: text
        list: list of patient records in JSON format
    """

    full_output = []

    for pdf in os.listdir(folder_path):

        text = f"original_filename: {pdf}\n"
        text += call_tesseract_api(f"{folder_path}/{pdf}", replicate_api)

        # call llm
        llm_output = llm_to_json(text)
        full_output.append(llm_output)

    return full_output


def llm_to_json(text_input: str) -> list:
    """Converts text to JSON using LLM

    Args:
        text_input (str): text to pass to LLM - output of our OCR model's reading of the image

    Returns:
        list: list of patient records in JSON format
    """

    # Define the input with the detailed prompt
    input_data = {
        "top_p": 0.9,
        "prompt": f"""
        Process the following text file and extract information to JSON format: \
        The text contains veterinary records for a single pet. Each record includes details such as:
        \n original_filename (this is important - include it for every record, even if other fields are missing)
        \n- Patient name\n- Species\n- Breed\n- Age\n- Owner name\n- Visit date\n- Notes\n- Procedures with costs\n
        - Total costs\n- Veterinarian name\n\n
        
        Please ensure the JSON output includes fields for each of the above details and handle variations in formatting or potential typos.
        If a field cannot be found, this is okay - just fill it in with null.
        Do not give any commentary or further wording. Nothing like "here is the output" - I only want back the json output of my request.

        Here is the text: {text_input}
        """,
        "min_tokens": 0,
        "temperature": 0.6,
        "presence_penalty": 1.15,
    }

    # Initialize the replicate client with your API token
    api = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])

    # Specify the image file path
    image_file_path = "handwritten_docs/handwriting_20241017_101027_via_10015_io.pdf"

    # Variable to store the entire output from the API
    llm_output = ""

    # Load the image file
    with open(image_file_path, "rb") as image_file:
        # Send the image to the endpoint along with the input
        for event in api.stream(
            "meta/meta-llama-3-70b-instruct", input={**input_data, "image": image_file}
        ):
            # Append each chunk of the event's output to the llm_output string
            llm_output += str(event)

    print(f"here is the output from the LLM: {llm_output}")
    print(f"json.loads: {json.loads(llm_output)}")
    return json.loads(llm_output)


def main() -> None:
    """Driver function"""

    # instantiate replicate object with API token
    replicate_api = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])

    # get data from all files in folder
    full_json_file = get_data_from_all_files("handwritten_docs/images", replicate_api)

    # Optionally write the full text to a file
    # with open("full_text.txt", "w") as text_file:
    #     text_file.write(full_text_file)

    # Write the full JSON file to disk
    with open("output_pet_records.json", "w") as json_file:
        json.dump(full_json_file, json_file, indent=4)


if __name__ == "__main__":
    main()
