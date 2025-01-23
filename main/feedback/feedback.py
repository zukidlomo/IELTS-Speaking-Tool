from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "IELTS Speaking Test Feedback", 0, 1, "C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(10)

    def chapter_body(self, body):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_feedback(self, title, feedback):
        self.add_page()
        self.chapter_title(title)
        self.chapter_body(feedback)


def generate_pdf_report(
    part1_feedback,
    part2_feedback,
    part3_feedback,
):
    pdf = PDF()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    pdf.add_feedback("Part 1: Introduction Feedback", part1_feedback)
    pdf.add_feedback("Part 2: Long Turn Feedback", part2_feedback)
    pdf.add_feedback("Part 3: Two-Way Discussion Feedback", part3_feedback)

    pdf.output("IELTS_Feedback_Report.pdf")
