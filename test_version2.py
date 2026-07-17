from app.parser.extractor import extract_pdf_text
from app.parser.hierarchy import build_hierarchy
from app.parser.ingest import ingest_document
from app.services.version_compare import compare_versions

# Parse Version 2 PDF
pages = extract_pdf_text("data/ct200_manual_v2.pdf")
sections = build_hierarchy(pages)

# Store Version 2
ingest_document(
    document_name="CT200 Manual",
    version_number=2,
    file_name="ct200_manual_v2.pdf",
    sections=sections
)

print("\nVersion 2 inserted successfully.")

# Compare Version 1 and Version 2
compare_versions(1, 2)