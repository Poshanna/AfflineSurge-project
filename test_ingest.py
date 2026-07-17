from app.parser.extractor import extract_pdf_text
from app.parser.hierarchy import build_hierarchy
from app.parser.ingest import ingest_document

pages = extract_pdf_text("data/ct200_manual.pdf")
sections = build_hierarchy(pages)

ingest_document(
    document_name="CT200 Manual",
    version_number=1,
    file_name="ct200_manual.pdf",
    sections=sections
)