import re
from typing import List

CPT_PATTERN = re.compile(r"\b\d{5}\b")
HCPCS_PATTERN = re.compile(r"\b[A-Z]\d{4}\b")
ICD10_PATTERN = re.compile(r"\b[A-Z]\d{2}\.?\d*\b")

def extract_cpt_codes(text: str) -> List[str]:
    cpt = CPT_PATTERN.findall(text)
    hcpcs = HCPCS_PATTERN.findall(text)
    return list(set(cpt + hcpcs))

def extract_icd10_codes(text: str) -> List[str]:
    return list(set(ICD10_PATTERN.findall(text)))
