import re
from typing import Dict, List, Optional, Tuple
import pdfplumber

SECTION_HEADERS = {
    "coverage_rationale": r"Coverage Rationale",
    "applicable_codes": r"Applicable Procedure Codes|CPT|HCPCS",
    "description": r"Description of Services|Description",
    "clinical_evidence": r"Clinical Evidence|Clinical Review Criteria",
    "definitions": r"Definitions",
    "references": r"References",
    "exclusions": r"Exclusions|Limitations",
}

def parse_pdf(pdf_path: str) -> Dict:
    sections: Dict[str, str] = {}
    full_text_pages = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            full_text_pages.append(text)

    full_text = "\n".join(full_text_pages)

    if not full_text.strip():
        return {"ocr_required": True, "sections": {}, "policy_name": "", "policy_number": None, "effective_date": None}

    # Extract policy name from first page
    # UHC PDFs follow the pattern: line 0 = insurer header, line 1 = "Medical Policy" / "Drug Policy",
    # line 2 = actual policy name. Skip known header lines and grab the first substantive title line.
    first_page = full_text_pages[0] if full_text_pages else ""
    lines = [l.strip() for l in first_page.splitlines() if l.strip()]
    SKIP_PATTERNS = re.compile(
        r"^(UnitedHealthcare|Medical Policy|Drug Policy|Community Plan|Oxford|Individual Exchange|Instructions for Use)",
        re.IGNORECASE,
    )
    policy_name = ""
    STOP_PATTERNS = re.compile(
        r"^(Policy Number|Policy No|Effective Date|Table of Contents|Application\s*\.)",
        re.IGNORECASE,
    )
    for idx, line in enumerate(lines):
        if not SKIP_PATTERNS.match(line):
            # Collect continuation lines (multi-line titles end mid-sentence)
            name_parts = [line]
            for next_line in lines[idx + 1:]:
                if SKIP_PATTERNS.match(next_line) or STOP_PATTERNS.match(next_line):
                    break
                # Stop if next line looks like a new independent item (starts with capital, not conjunction)
                if re.match(r"^(Policy|Effective|Table|Application|Coverage|Description|Definitions|References)", next_line):
                    break
                name_parts.append(next_line)
            policy_name = " ".join(name_parts)
            break
    if not policy_name:
        policy_name = lines[0] if lines else ""

    # Extract effective date
    date_match = re.search(
        r"Effective\s*Date:\s*(\w+ \d{1,2},?\s*\d{4}|\d{1,2}/\d{1,2}/\d{4})",
        full_text,
    )
    effective_date = date_match.group(1) if date_match else None

    # Extract policy number
    num_match = re.search(r"Policy (?:No\.?|Number):?\s*([\w\-\.]+)", full_text)
    policy_number = num_match.group(1) if num_match else None

    # Split into sections
    header_pattern = "|".join(f"({v})" for v in SECTION_HEADERS.values())
    splits = re.split(f"(?m)^({header_pattern})\\s*$", full_text)

    current_section = "preamble"
    sections[current_section] = ""
    i = 0
    while i < len(splits):
        chunk = splits[i]
        if chunk is None:
            i += 1
            continue
        matched_section = None
        for section_key, pattern in SECTION_HEADERS.items():
            if re.fullmatch(pattern, chunk.strip(), re.IGNORECASE):
                matched_section = section_key
                break
        if matched_section:
            current_section = matched_section
            sections[current_section] = ""
        else:
            sections[current_section] = sections.get(current_section, "") + chunk
        i += 1

    return {
        "ocr_required": False,
        "sections": sections,
        "policy_name": policy_name,
        "policy_number": policy_number,
        "effective_date": effective_date,
    }
