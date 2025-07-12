import os
import pandas as pd
import docx
import re

def process_file(path):
    if path.endswith(".xlsx"):
        return process_excel(path)
    elif path.endswith(".docx"):
        return process_docx(path)
    else:
        return {"error": "Unsupported file type"}

def process_excel(path):
    df = pd.read_excel(path)
    return df.fillna("").to_dict(orient="records")

def process_docx(path):
    doc = docx.Document(path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    results = []
    entry = []

    for line in paragraphs:
        if "Sdn Bhd" in line and entry:
            results.append(parse_entry(entry))
            entry = [line]
        else:
            entry.append(line)
    if entry:
        results.append(parse_entry(entry))

    return results

def parse_entry(lines):
    text = "\n".join(lines)
    result = {}

    match = re.search(r'^(.+Sdn Bhd)', text)
    if match:
        result['company_name'] = match.group(1)

    emails = re.findall(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', text)
    if emails:
        result['email'] = "; ".join(emails)

    phones = re.findall(r'\b(?:Tel[:\s]*)?(\+?6?0\d{1,2}[-\s]?\d{6,8}|\d{2,4}[-\s]?\d{6,8})', text)
    if phones:
        result['phone'] = "; ".join(sorted(set(phones)))

    address_lines = []
    for line in lines[1:]:
        if any(x in line for x in ["Email", "Tel", "Fax", "CEO", "Website"]):
            break
        address_lines.append(line)
    result['address'] = " ".join(address_lines)

    return result