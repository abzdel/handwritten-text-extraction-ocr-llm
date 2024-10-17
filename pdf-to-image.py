import pdf2image
import os


def create_image_path_if_not_exist(new_folder_path: str) -> str:
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    return new_folder_path


def convert_pdf_to_image(pdf_path: str) -> None:
    """Converts PDF to image

    Args:
        pdf_path (str): path to PDF

    Returns:
        None
    """

    image_folder_path = create_image_path_if_not_exist("handwritten_docs/images")

    # open handwritten_docs/handwriting_20241017_100546_via_10015_io.pdf and convert to jpg
    with open(pdf_path, "rb") as pdf_file:
        images = pdf2image.convert_from_bytes(pdf_file.read())

        # get name of file, before the .pdf
        file_name = os.path.splitext(os.path.basename(pdf_path))[0]

        for img in images:
            img.save(
                f"{image_folder_path}/{file_name}.jpg",
                "JPEG",
            )


def convert_all_pdf_to_image(folder_path: str) -> None:
    """Converts all PDFs in folder to image

    Args:
        folder_path (str): path to folder

    Returns:
        None
    """

    for pdf_file in os.listdir(folder_path):
        if pdf_file.endswith(".pdf"):
            convert_pdf_to_image(f"{folder_path}/{pdf_file}")


if __name__ == "__main__":
    convert_all_pdf_to_image("handwritten_docs/")
