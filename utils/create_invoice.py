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
        row_height = self.font_size * 1.5  # Base row height

        for row_index, row in enumerate(data):
            wrapped_row = []

            # Wrap text for each cell and calculate maximum lines in the row
            max_lines = 1
            for i, item in enumerate(row):
                wrapped_lines = wrap_text(self, str(item), col_widths[i])
                wrapped_row.append(wrapped_lines)
                max_lines = max(max_lines, len(wrapped_lines))

            # Calculate total row height
            total_row_height = max_lines * row_height
            y_start = self.get_y()  # Starting Y position of the row

             # Check if this is the total row
            is_total_row = row_index >= len(data) - 2  # Assuming totals are the last two rows

            # Set font style for total rows
            if is_total_row:
                self.set_font('DejaVu', 'B', 9)  # Bold font for totals
            else:
                self.set_font('DejaVu', '', 9)  # Regular font for other rows

            # Draw borders for the entire row
            for i, wrapped_lines in enumerate(wrapped_row):
                x_start = self.get_x()  # Starting X position of the cell
                self.rect(x_start, y_start, col_widths[i], total_row_height)  # Single border for the cell

                # Write text line by line within the cell
                for line_num, line in enumerate(wrapped_lines):
                    self.set_xy(x_start, y_start + line_num * row_height)
                    self.cell(col_widths[i], row_height, line, border=0, align='L')

                # Move to the next cell horizontally
                self.set_x(x_start + col_widths[i])

            # Move to the next row vertically
            self.set_y(y_start + total_row_height)
        self.ln()  # Add extra line after the table
