from app.parser.extractor import extract_pdf_text
from app.parser.hierarchy import build_hierarchy

pages = extract_pdf_text("data/ct200_manual.pdf")
sections = build_hierarchy(pages)

print(f"Total Sections: {len(sections)}")
print("=" * 60)

for s in sections:
    print(f"{s['section_number']} | {s['title']} | Level {s['level']} | Page {s['page']}")