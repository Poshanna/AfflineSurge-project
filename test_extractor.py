from app.parser.extractor import extract_pdf_text

pdf_path = "data/ct200_manual.pdf"

pages = extract_pdf_text(pdf_path)

print(f"Total Pages: {len(pages)}")
print("=" * 50)

print(pages[0]["text"][:1000])