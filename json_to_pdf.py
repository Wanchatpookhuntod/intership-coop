import sys
import json
import os
from PySide6.QtWidgets import QApplication
from pdf_handler import PDFHandler

def convert_json_to_pdf(json_path, pdf_path):
    if not os.path.exists(json_path):
        print(f"Error: File not found: {json_path}")
        return

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            records = json.load(f)
        print(f"Loaded {len(records)} records from {json_path}")
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return

    # QApplication is required for QPrinter and QTextDocument
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()

    print(f"Converting {json_path} to {pdf_path}...")
    success, message = PDFHandler.export_pdf(records, pdf_path)
    
    if success:
        print(f"Success: {message}")
        print(f"File saved at: {os.path.abspath(pdf_path)}")
    else:
        print(f"Failed: {message}")

if __name__ == "__main__":
    json_file = "db_students.json"
    pdf_file = "students_report.pdf"
    convert_json_to_pdf(json_file, pdf_file)
