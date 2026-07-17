import re


def build_hierarchy(pages):
    """
    Build hierarchy from extracted PDF pages.
    """

    sections = []

    current_section = None

    for page in pages:

        for line in page["text"].split("\n"):

            line = line.strip()

            if not line:
                continue

            # Match headings:
            # 1. Device Overview
            # 1.1 Intended Use
            # 2.1.1 Battery Life
            heading = re.match(r"^(\d+(?:\.\d+)*)\.?\s+(.+)$", line)

            if heading:

                number = heading.group(1)
                title = heading.group(2)

                # Ignore numbered list items like:
                # 1. Normal:
                # 2. Elevated:
                if ":" in title:
                    if current_section:
                        current_section["content"] += line + "\n"
                    continue

                if current_section:
                    current_section["content"] = current_section["content"].strip()
                    sections.append(current_section)

                level = len(number.split("."))

                current_section = {
                    "section_number": number,
                    "title": title,
                    "level": level,
                    "page": page["page"],
                    "content": ""
                }

            else:
                if current_section:
                    current_section["content"] += line + "\n"

    if current_section:
        current_section["content"] = current_section["content"].strip()
        sections.append(current_section)

    return sections