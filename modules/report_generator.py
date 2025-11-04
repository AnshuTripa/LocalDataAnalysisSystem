import os
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

class ReportGenerator:
    def __init__(self, df, output_dir="reports"):
        self.df = df
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.pdf_path = os.path.join(output_dir, "Data_Report.pdf")

    def generate_summary(self):
        """Generate text summary of dataset"""
        total_rows = len(self.df)
        total_cols = len(self.df.columns)
        missing = self.df.isna().sum().sum()

        numeric_cols = self.df.select_dtypes(include='number').columns
        stats = self.df[numeric_cols].describe().to_string() if not numeric_cols.empty else "No numeric data."

        summary_text = (
            f"📄 DATA SUMMARY REPORT\n\n"
            f"Total Rows: {total_rows}\n"
            f"Total Columns: {total_cols}\n"
            f"Missing Values: {missing}\n\n"
            f"📊 Numeric Summary:\n{stats}\n"
        )
        return summary_text

    def generate_pdf(self):
        """Create a PDF report"""
        c = canvas.Canvas(self.pdf_path, pagesize=A4)
        width, height = A4

        # --- Add title ---
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 50, "Local Data Analysis Report")

        # --- Add summary text ---
        summary = self.generate_summary()
        text_object = c.beginText(50, height - 100)
        text_object.setFont("Helvetica", 10)
        for line in summary.split("\n"):
            text_object.textLine(line)
        c.drawText(text_object)

        # --- Add charts from output folder ---
        chart_folder = "output"
        y_pos = 300
        if os.path.exists(chart_folder):
            for img in os.listdir(chart_folder):
                if img.endswith(".png"):
                    img_path = os.path.join(chart_folder, img)
                    try:
                        c.drawImage(ImageReader(img_path), 50, y_pos, width=500, height=200, preserveAspectRatio=True)
                        y_pos -= 220
                        if y_pos < 100:
                            c.showPage()
                            y_pos = height - 250
                    except Exception as e:
                        print(f"⚠️ Skipping image {img}: {e}")

        # --- Save PDF ---
        c.showPage()
        c.save()
        print(f"✅ PDF Report generated: {self.pdf_path}")
