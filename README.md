[![Makefile CI](https://github.com/abzdel/vet-data-text-extraction/actions/workflows/makefile.yml/badge.svg)](https://github.com/abzdel/vet-data-text-extraction/actions/workflows/makefile.yml)

# Handwritten Vet Notes - Text Extraction


Example of using OCR model and LLM to parse out unstructured notes into JSON format.


## Architectural Diagram
![vet-architectural-diagram](https://github.com/user-attachments/assets/8ef79bdc-424b-4640-9233-7df2ff2df0bd)

## Using the program

1. Clone the repo
   ```bash
   git clone https://github.com/abzdel/vet-data-text-extraction.git
   ```

1. (optional) Create virtual environment, activate it
   ```python
   python -m venv venv
   ```

   activating on Windows:
   ```bash
   venv/Scripts/activate
   ```

   activating on Linux/MacOS:
   ```bash
   source venv/bin/activate
   ```

1. Install requirements
   ```bash
   pip install -r requirements.txt
   ```

1. Set up an account on [Replicate](https://replicate.com/). This is where we host our OCR model and LLM.

1. export your API key as
   ```bash
   export REPLICATE_API_TOKEN=r8_xxxxxxxxx
   ```

1. If you have a folder of pdfs (if they haven't been converted to images yet), you need to run pdf_to_image first.
   ```python
   python src/pdf_to_image.py
   ```

1. Once you have a folder of images in your **handwritten_docs/images** folder, we can run the driver function
   ```python
   python src/main.py
   ```
