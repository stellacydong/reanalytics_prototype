# app/components/report_generator.py

from fpdf import FPDF
import os

class PortfolioReportGenerator:
    """
    Generate a simple PDF report comparing original and optimized portfolios.
    """

    def __init__(self, output_folder="data/reports"):
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)

    def generate_report(self, original_portfolio, optimized_portfolio, output_filename="portfolio_optimization_report.pdf"):
        pdf = FPDF()
        pdf.add_page()

        # Title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Treaty Portfolio Optimization Report", ln=True, align="C")
        pdf.ln(10)

        # Original Portfolio Summary
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Original Portfolio", ln=True)
        pdf.set_font("Arial", '', 11)
        for treaty in original_portfolio:
            treaty_line = f"{treaty['treaty_name']}: Retention ${treaty['retention']:,.0f}, Limit ${treaty['limit']:,.0f}"
            pdf.cell(0, 8, treaty_line, ln=True)

        pdf.ln(8)

        # Optimized Portfolio Summary
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Optimized Portfolio", ln=True)
        pdf.set_font("Arial", '', 11)
        for treaty in optimized_portfolio:
            treaty_line = f"{treaty['treaty_name']}: Retention ${treaty['retention']:,.0f}, Limit ${treaty['limit']:,.0f}"
            pdf.cell(0, 8, treaty_line, ln=True)

        pdf.ln(10)

        # Save the PDF
        report_path = os.path.join(self.output_folder, output_filename)
        pdf.output(report_path)

        return report_path

# Example Usage
if __name__ == "__main__":
    from models.portfolio_aggregator import PortfolioAggregator

    aggregator = PortfolioAggregator()
    portfolio = aggregator.build_portfolio()

    generator = PortfolioReportGenerator()
    generator.generate_report(portfolio, portfolio, output_filename="example_report.pdf")
    print("Example report generated!")
