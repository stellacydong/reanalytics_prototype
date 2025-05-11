# app/components/treaty_parser.py

import os

def parse_treaty_text(file_path: str) -> str:
    """
    Reads the full content of a treaty file.

    Args:
        file_path (str): Path to the uploaded .txt treaty file.

    Returns:
        str: Raw treaty text content.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Treaty file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    return text


def extract_treaty_metadata(text: str) -> dict:
    """
    Naively extract metadata (for demo purposes only).
    Future: Use NER, regex, or LLMs for structured extraction.

    Args:
        text (str): Raw treaty text content.

    Returns:
        dict: Dictionary with placeholder treaty metadata.
    """
    metadata = {
        "cedent_name": "Unknown",
        "effective_date": "Unknown",
        "coverage_type": "Excess of Loss",
        "currency": "USD",
        "document_length": f"{len(text.split())} words"
    }

    # You can expand this logic using regex or NLP techniques

    return metadata

