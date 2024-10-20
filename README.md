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


## Limitations

- The handwritten documents used in this project are **computer-generated**, not actual handwritten documents. This could limit the OCR model's effectiveness when applied to real-world handwriting, which tends to be more varied and harder to recognize.
- I only tested the solution on **a small set of documents**, meaning that the results may not generalize well to a broader set of documents with different formats, fonts, or languages.
- The **LLM processing** of the text extracted by OCR is currently based on assumptions about the structure of the data. If documents deviate significantly from these assumptions, the LLM might not produce reliable JSON output.
- **Performance constraints**: The process involves multiple API calls to Replicate, which can introduce latency, especially when dealing with large documents or images.
- The **lack of noise or distortion** in the test documents makes it difficult to assess how well the OCR handles real-world issues like smudges, tears, or poor image quality.

## Next Steps

- **Fine-tuning the OCR model** with a larger, more diverse set of real handwritten documents would improve its accuracy and robustness to real-world scenarios.
- **Developing pre-processing techniques**: Implementing additional image processing techniques (like noise reduction, contrast adjustment, etc.) could help the OCR model perform better with low-quality or noisy images.
- **Adding more test cases**: We could build a more comprehensive suite of tests to cover edge cases and validate different types of input, ensuring both the OCR and LLM can handle unexpected inputs and document formats.
- **Performance optimization**: Looking into optimizing the workflow to reduce the latency caused by multiple API calls, such as by exploring local models or batching API requests, could improve performance.
- **Post-processing the LLM output**: Adding layers of post-processing to the LLM's output could help ensure the output is always structured as expected.

