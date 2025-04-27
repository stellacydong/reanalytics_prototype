# models/treaty_term_extractor.py

import re

class TreatyTermExtractor:
    """
    A simple rule-based Treaty Term Extractor (MVP version).
    Parses treaties (text) to find Retention, Limit, Reinstatements, and Exclusions.
    """

    def __init__(self):
        pass

    def extract_terms(self, treaty_text):
        """
        Extracts important treaty terms from the text.

        Args:
        - treaty_text (str): Full text of a treaty.

        Returns:
        - dict: Extracted structured information.
        """
        extracted = {
            "retention": self._find_retention(treaty_text),
            "limit": self._find_limit(treaty_text),
            "reinstatements": self._find_reinstatements(treaty_text),
            "exclusions": self._find_exclusions(treaty_text)
        }
        return extracted

    def _find_retention(self, text):
        match = re.search(r"Retention: \$?([0-9,]+)", text)
        if match:
            return int(match.group(1).replace(",", ""))
        return None

    def _find_limit(self, text):
        match = re.search(r"Limit: \$?([0-9,]+)", text)
        if match:
            return int(match.group(1).replace(",", ""))
        return None

    def _find_reinstatements(self, text):
        match = re.search(r"Reinstatements: (\d+)", text)
        if match:
            return int(match.group(1))
        if "None" in text or "Not Applicable" in text:
            return 0
        return None

    def _find_exclusions(self, text):
        exclusions = []
        match = re.search(r"Exclusions: (.+)", text)
        if match:
            exclusions_text = match.group(1)
            exclusions = [e.strip() for e in exclusions_text.split(",")]
        return exclusions

# Example Usage
if __name__ == "__main__":
    extractor = TreatyTermExtractor()
    sample_text = """
    Reinsurance Treaty Agreement

    - Type: Quota Share
    - Retention: $2,000,000 per occurrence
    - Limit: $10,000,000 per occurrence
    - Reinstatements: 1 automatic at 100% additional premium
    - Territory: Worldwide excluding sanctioned countries
    - Exclusions: War, Nuclear, Terrorism
    - Effective Date: January 1, 2024
    - Ceding Commission: 30%
    """
    result = extractor.extract_terms(sample_text)
    print(result)
