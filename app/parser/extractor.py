import fitz  # PyMuPDF


def extract_pdf_text(pdf_path: str):
    """
    Extract text from a PDF page by page.

    Returns:
        List of dictionaries:
        [
            {
                "page": 1,
                "text": "...page text..."
            },
            ...
        ]
    """

    document = fitz.open(pdf_path)
    pages = []

    for page_number in range(len(document)):
        page = document.load_page(page_number)
        text = page.get_text("text")

        pages.append(
            {
                "page": page_number + 1,
                "text": text.strip()
            }
        )

    document.close()

    return pages