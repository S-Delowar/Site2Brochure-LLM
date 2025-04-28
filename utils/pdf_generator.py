from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Company Brochure', 0, 1, 'C')

def save_brochure_as_pdf(brochure_text, output_path):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in brochure_text.split('\n'):
        pdf.multi_cell(0, 10, line)
    
    pdf.output(output_path)
