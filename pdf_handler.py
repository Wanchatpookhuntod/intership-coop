from PySide6.QtGui import QTextDocument, QPageSize, QPageLayout
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtCore import QMarginsF, QDate
from constants import PROGRESS_ITEMS

class PDFHandler:
    @staticmethod
    def export_pdf(records, path):
        try:
            # สร้าง HTML Content
            html = """
            <html>
            <head>
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap');
                    body { font-family: 'Sarabun', sans-serif; font-size: 9px; }
                    h3 { text-align: center; color: #1E3A8A; margin-bottom: 10px; }
                    table { width: 100%; border-collapse: collapse; margin-top: 10px; }
                    th { background-color: #F3F4F6; color: #1F2937; font-weight: bold; padding: 8px; border: 1px solid #E5E7EB; font-size: 10px; }
                    td { padding: 6px; border: 1px solid #E5E7EB; color: #374151; text-align: center; }
                    td.left { text-align: left; }
                    tr:nth-child(even) { background-color: #F9FAFB; }
                    .status-done { color: #059669; font-weight: bold; }
                    .status-pending { color: #DC2626; }
                    .grade { color: #D97706; font-weight: bold; font-size: 9px; display: block; }
                </style>
            </head>
            <body>
                <h3>รายงานข้อมูลนักศึกษาฝึกงาน</h3>
                <table>
                    <thead>
                        <tr>
                            <th width="10%">รหัสนักศึกษา</th>
                            <th width="18%">ชื่อ-นามสกุล</th>
                            <th width="28%">สถานที่ฝึกงาน</th>
            """
            
            # Add headers for progress items
            for _, label in PROGRESS_ITEMS:
                html += f"<th>{label}</th>"
            
            html += """
                        </tr>
                    </thead>
                    <tbody>
            """

            for student in records:
                sid = student.get("student_id", "-")
                name = student.get("name", "-")
                loc = student.get("location", "-")
                
                html += f"""
                        <tr>
                            <td class="left">{sid}</td>
                            <td class="left">{name}</td>
                            <td class="left">{loc}</td>
                """
                
                # Progress Items
                progress = student.get("progress", {})
                for key, _ in PROGRESS_ITEMS:
                    item = progress.get(key, {})
                    is_done = item.get("status", False) if isinstance(item, dict) else item
                    grade = item.get("grade", "-") if isinstance(item, dict) else "-"
                    
                    if is_done:
                        status_icon = "✓"
                        status_class = "status-done"
                        grade_text = f'<span class="grade">{grade}</span>' if grade != "-" else ""
                        html += f'<td class="{status_class}">{status_icon}{grade_text}</td>'
                    else:
                        html += '<td class="status-pending">-</td>'
                
                html += "</tr>"

            html += """
                    </tbody>
                </table>
                <p style="text-align: right; margin-top: 20px; color: #6B7280; font-size: 10px;">สร้างเมื่อ: {}</p>
            </body>
            </html>
            """.format(QDate.currentDate().toString("dd/MM/yyyy"))

            # สร้าง PDF
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(path)
            printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
            printer.setPageOrientation(QPageLayout.Orientation.Landscape)
            printer.setPageMargins(QMarginsF(10, 10, 10, 10), QPageLayout.Unit.Millimeter)

            document = QTextDocument()
            document.setHtml(html)
            document.setPageSize(printer.pageRect(QPrinter.Unit.Point).size())
            document.print_(printer)
            
            return True, "บันทึก PDF เรียบร้อย"

        except Exception as e:
            return False, str(e)
