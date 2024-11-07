from fpdf import FPDF, XPos, YPos
from utils.index import wrap_text

class PDF(FPDF):
    def header(self):
        self.set_font('DejaVu', 'B', 9)
        self.cell(0, 10, 'LASKU / INVOICE', 0, new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')

    def add_invoice_details(self, details):
        self.set_font('DejaVu', '', 9)
        for line in details:
            self.cell(0, 5, line, 0, new_x=XPos.RIGHT, new_y=YPos.NEXT, align='R')
        self.ln()

    def add_customer_details(self, details):
        self.set_font('DejaVu', '', 9)
        for line in details:
            self.cell(0, 5, line, 0, new_x=XPos.LEFT, new_y=YPos.NEXT, align='R')
        self.ln()

    def add_seller_details(self, details):
        self.set_font('DejaVu', '', 9)
        for line in details:
            self.cell(0, 5, line, 0, new_x=XPos.LEFT, new_y=YPos.NEXT, align='L')
        self.ln()

    def add_table(self, data, col_widths):
        self.set_font('DejaVu', '', 9)
        row_height = self.font_size * 1.5
        for row in data:
            max_lines = 1
            wrapped_row = []
            for i, item in enumerate(row):
                wrapped_lines = wrap_text(self, str(item), col_widths[i])
                max_lines = max(max_lines, len(wrapped_lines))
                wrapped_row.append(wrapped_lines)

            for line in range(max_lines):
                for i, wrapped_lines in enumerate(wrapped_row):
                    if line < len(wrapped_lines):
                        self.multi_cell(
                            col_widths[i], row_height, wrapped_lines[line],
                            border=1, new_x=XPos.RIGHT, new_y=YPos.TOP,
                            max_line_height=self.font_size
                        )
                    else:
                        self.cell(col_widths[i], row_height, "", border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
                self.ln(row_height)
        self.ln()  # Add extra line after the table
