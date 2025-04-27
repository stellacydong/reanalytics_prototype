# models/portfolio_aggregator.py

import os
import json
from models.treaty_term_extractor import TreatyTermExtractor

class PortfolioAggregator:
    """
    Aggregates multiple treaty term extracts into a portfolio structure.
    """

    def __init__(self, treaties_folder="data/treaties", portfolio_folder="data/portfolios"):
        self.treaties_folder = treaties_folder
        self.portfolio_folder = portfolio_folder
        self.extractor = TreatyTermExtractor()

        # Create portfolio folder if missing
        os.makedirs(self.portfolio_folder, exist_ok=True)

    def build_portfolio(self):
        """
        Process all treaties in the treaties_folder and build a portfolio.

        Returns:
        - list: Portfolio data [{treaty_name, retention, limit, reinstatements, exclusions}, ...]
        """
        portfolio = []

        for filename in os.listdir(self.treaties_folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.treaties_folder, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()

                terms = self.extractor.extract_terms(text)
                terms["treaty_name"] = filename.replace(".txt", "")
                portfolio.append(terms)

        # Save portfolio JSON
        self._save_portfolio(portfolio)
        return portfolio

    def _save_portfolio(self, portfolio):
        """
        Save the portfolio to a JSON file.
        """
        save_path = os.path.join(self.portfolio_folder, "original_portfolio.json")
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(portfolio, f, indent=4)

# Example Usage
if __name__ == "__main__":
    aggregator = PortfolioAggregator()
    portfolio = aggregator.build_portfolio()
    print(json.dumps(portfolio, indent=2))
