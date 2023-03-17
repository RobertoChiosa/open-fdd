# Author:       Roberto Chiosa
# Copyright:    Roberto Chiosa, © 2023
# Email:        roberto.chiosa@polito.it
#
# Created:      16/03/23
# Script Name:  pdf_demo.py
# Path:         air_handling_unit/reports
#
# Script Description:
#
# https://pyfpdf.github.io/fpdf2/Tutorial.html
# Notes:

import time

from fpdf import FPDF


class PDF(FPDF):
    def __init__(self, title):
        super().__init__()
        self.title = title

    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Title
        pdf.cell(40, 10, self.title)
        self.ln(5)
        # date
        self.set_font('Arial', 'I', 8)
        pdf.cell(40, 10, f"Report generated: {time.ctime()}")
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def add_heading(self, text, num=""):
        # Arial 12
        self.set_font('Arial', 'B', 12)
        # Title
        pdf.cell(40, 10, f'{num}. {text}')
        # Line break
        self.ln(10)

    def add_paragraph(self, text):
        # Read text file
        # Times 12
        self.set_font('Helvetica', '', 11)
        # Output justified text
        self.multi_cell(0, 5, text)
        # Line break
        self.ln()

    def add_run(self, items_list):
        # Read text file
        # Times 12
        self.set_font('Helvetica', '', 11)
        for item in items_list:
            # Output justified text
            self.cell(0, 5, "   " + item)
            self.ln()
        self.ln()

    def add_picture(self, path):
        # Read text file
        # Times 12
        self.image(path, x=10, y=pdf.get_y(), w=170)
        # Line break
        self.ln(pdf.get_y())


if __name__ == '__main__':
    pdf = PDF(
        title="Fault Condition One Report"
    )
    pdf.add_page()
    pdf.add_heading(1, 'Fault definition')
    pdf.add_paragraph(
        """Fault condition one of ASHRAE Guideline 36 is related to flagging poor performance of a AHU variable 
        supply fan attempting to control to a duct pressure setpoint. Fault condition equation as defined by  ASHRAE:"""
    )

    # add image
    pdf.add_picture('../images/fc1_definition.png')
    pdf.add_heading(1, 'Dataset Plot')
    pdf.add_heading(1, 'Dataset Statistics')
    # create a bullet point
    pdf.add_run(["- This outputs correctly", "- This outputs correctly"])

    pdf.add_heading(1, 'Summary Statistics filtered for when the AHU is running')
    pdf.add_heading(1, 'Suggestions based on data analysis')
    pdf.add_heading(1, 'Fault definition')

    # pdf.print_chapter(1, 'A RUNAWAY REEF', '20k_c1.txt')
    # pdf.print_chapter(2, 'THE PROS AND CONS', '20k_c2.txt')
    pdf.output(name='../final_report/tutorial_pdf.pdf', dest='F')
