
# AI generated test cases for create_invoice.py

import unittest
from fpdf import FPDF
from utils.create_invoice import PDF

class TestPDF(unittest.TestCase):
    def setUp(self):
        self.pdf = PDF()

    def test_header(self):
        self.pdf.add_page()
        self.pdf.header()
        self.assertIn('LASKU / INVOICE', self.pdf.pages[0])

    def test_add_invoice_details(self):
        details = ["Invoice Number: 12345", "Date: 2023-10-01"]
        self.pdf.add_page()
        self.pdf.add_invoice_details(details)
        for detail in details:
            self.assertIn(detail, self.pdf.pages[0])

    def test_add_customer_details(self):
        details = ["Customer Name: John Doe", "Address: 123 Main St"]
        self.pdf.add_page()
        self.pdf.add_customer_details(details)
        for detail in details:
            self.assertIn(detail, self.pdf.pages[0])

    def test_add_seller_details(self):
        details = ["Seller Name: ABC Corp", "Address: 456 Market St"]
        self.pdf.add_page()
        self.pdf.add_seller_details(details)
        for detail in details:
            self.assertIn(detail, self.pdf.pages[0])

    def test_add_table(self):
        data = [
            ["Item", "Description", "Quantity", "Price"],
            ["001", "Widget", "10", "$5.00"],
            ["002", "Gadget", "5", "$10.00"],
            ["Total", "", "", "$75.00"]
        ]
        col_widths = [30, 50, 30, 30]
        self.pdf.add_page()
        self.pdf.add_table(data, col_widths)
        for row in data:
            for item in row:
                self.assertIn(item, self.pdf.pages[0])

if __name__ == '__main__':
    unittest.main()
