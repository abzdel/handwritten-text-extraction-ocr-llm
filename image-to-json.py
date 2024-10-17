import replicate
import os
import base64


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


def get_data_from_all_files(folder_path: str, replicate_api: str) -> str:
    """Calls Tesseract API for all files in folder

    Args:
        folder_path (str): path to folder

    Returns:
        str: text
    """

    full_text_file = ""

    for pdf in os.listdir(folder_path):
        print(f"here is our pdf: {pdf}")
        text = call_tesseract_api(f"{folder_path}/{pdf}", replicate_api)

        full_text_file += text

    return full_text_file


# convert full_text_file to pdf


def main() -> None:
    """Driver function"""

    # instantiate replicate object with API token
    replicate_api = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])

    # get data from all files in folder
    full_text_file = get_data_from_all_files("handwritten_docs/images", replicate_api)

    with open("full_text.txt", "w") as text_file:
        text_file.write(full_text_file)


if __name__ == "__main__":
    main()
