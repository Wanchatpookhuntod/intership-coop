from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget, QHeaderView, 
                               QAbstractItemView, QTableWidgetItem, QDialog, QFrame, QTextEdit, QPushButton)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from constants import PROGRESS_ITEMS

class OverviewTab(QWidget):
    def __init__(self):
        super().__init__()
        self.records = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        lbl_head = QLabel("ภาพรวมความคืบหน้า (Overview Dashboard)")
        lbl_head.setStyleSheet("font-size: 18px; font-weight: bold; color: #1E293B; margin-bottom: 10px;")
        layout.addWidget(lbl_head)

        self.table = QTableWidget()
        cols = ["รหัส", "ชื่อ-นามสกุล", "สถานที่"] + [label for _, label in PROGRESS_ITEMS]
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch) 
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch) 
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        
        for i in range(3, len(cols)):
            self.table.setColumnWidth(i, 110)

        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)
        
        layout.addWidget(self.table)

    def update_table(self, records):
        self.records = records
        self.table.setRowCount(0)
        for row_idx, data in enumerate(records):
            self.table.insertRow(row_idx)
            
            self.table.setItem(row_idx, 0, QTableWidgetItem(data.get("student_id", "")))
            self.table.setItem(row_idx, 1, QTableWidgetItem(data.get("name", "")))
            self.table.setItem(row_idx, 2, QTableWidgetItem(data.get("location", "")))

            progress = data.get("progress", {})
            for col_offset, (key, _) in enumerate(PROGRESS_ITEMS):
                item_data = progress.get(key, {})
                is_done = item_data.get("status", False) if isinstance(item_data, dict) else item_data
                grade = item_data.get("grade", "-") if isinstance(item_data, dict) else "-"
                
                if is_done:
                    display_text = grade if grade != "-" else "✓"
                    item = QTableWidgetItem(display_text)
                    item.setTextAlignment(Qt.AlignCenter)
                    
                    if grade != "-":
                        # กำหนดสีตามเกรด
                        if grade in ["A", "A+"]:
                            color = "#00A21E"  # เขียวเข้ม
                        elif grade in ["B+", "B"]:
                            color = "#0038F1"  # เขียว
                        elif grade in ["C+", "C"]:
                            color = "#F7DA00"  # เหลือง/ส้ม
                        elif grade in ["D+", "D"]:
                            color = "#F59E0B"  # ส้ม
                        elif grade == "F":
                            color = "#DC2626"  # แดง
                        else:
                            color = "#000000"  # น้ำเงิน (กรณีอื่นๆ)

                        item.setForeground(QColor(color))
                        item.setBackground(QColor("#050505"))
                        item.setFont(QFont("Arial", 12, QFont.Bold))
                    else:
                        item.setForeground(QColor("#10B981"))
                        item.setFont(QFont("Arial", 16, QFont.Bold))
                else:
                    item = QTableWidgetItem("-")
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setForeground(QColor("#E5E7EB"))

                self.table.setItem(row_idx, 3 + col_offset, item)

    def on_cell_double_clicked(self, row, col):
        if col < 3:
            return
            
        student = self.records[row]
        progress_key = PROGRESS_ITEMS[col - 3][0]
        progress_label = PROGRESS_ITEMS[col - 3][1]
        
        progress_data = student.get("progress", {}).get(progress_key, {})
        
        if isinstance(progress_data, bool):
            status = progress_data
            grade = "-"
            note = ""
        else:
            status = progress_data.get("status", False)
            grade = progress_data.get("grade", "-")
            note = progress_data.get("note", "")

        scope = student.get("scope", "")
        self.show_detail_popup(student["name"], progress_label, status, grade, note, scope)

    def show_detail_popup(self, student_name, title, status, grade, note, scope=""):
        dlg = QDialog(self)
        # กำหนด Flag เพื่อซ่อนไอคอน (เอา Qt.WindowSystemMenuHint ออก)
        dlg.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        dlg.setWindowTitle(" ")
        dlg.setFixedSize(600, 500)
        
        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # นำหัวข้อมาแสดงก่อนชื่อ
        if "." in title:
            title = title.split('.', 1)[1].strip()
            
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1F2937; margin-bottom: 5px;")
        lbl_title.setWordWrap(True)
        layout.addWidget(lbl_title)

        lbl_name = QLabel(f"👤 {student_name}")
        lbl_name.setStyleSheet("font-size: 16px; font-weight: bold; color: #1E3A8A; margin-bottom: 10px;")
        layout.addWidget(lbl_name)

        # แสดงขอบเขตงาน (อยู่นอกกรอบสถานะ)
        lbl_scope_title = QLabel("📌 ขอบเขตงาน:")
        lbl_scope_title.setStyleSheet("font-weight: bold; margin-top: 5px; color: #4B5563;")
        layout.addWidget(lbl_scope_title)

        lbl_scope = QLabel(scope if scope else "- ไม่มีข้อมูล -")
        lbl_scope.setWordWrap(True)
        lbl_scope.setStyleSheet("color: #374151; margin-left: 10px; margin-bottom: 5px;")
        layout.addWidget(lbl_scope)
        
        card = QFrame()
        card.setStyleSheet("background-color: white; border: 1px solid #E5E7EB; border-radius: 8px; margin-top: 10px;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(15, 15, 15, 15)
        
        status_text = "✅ เรียบร้อย" if status else "❌ ยังไม่ทำ"
        status_color = "#059669" if status else "#DC2626"
        lbl_status = QLabel(f"สถานะ: {status_text}")
        lbl_status.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {status_color}; border: none;")
        card_layout.addWidget(lbl_status)
        
        if grade != "-":
            lbl_grade = QLabel(f"ผลการประเมิน: {grade}")
            lbl_grade.setStyleSheet("font-size: 16px; font-weight: bold; color: #D97706; margin-top: 5px; border: none;")
            card_layout.addWidget(lbl_grade)
            
        lbl_note_title = QLabel("บันทึก/หมายเหตุ:")
        lbl_note_title.setStyleSheet("font-weight: bold; margin-top: 5px; color: #4B5563; border: none;")
        card_layout.addWidget(lbl_note_title)
        
        txt_note = QTextEdit()
        txt_note.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        txt_note.setFixedHeight(100)
        txt_note.setPlainText(note if note else "- ไม่มีบันทึก -")
        txt_note.setReadOnly(True)
        txt_note.setStyleSheet("background-color: #F9FAFB; border: 1px solid #D1D5DB; border-radius: 4px; color: #374151;")
        card_layout.addWidget(txt_note)
        
        layout.addWidget(card)
        
        btn_close = QPushButton("ปิด")
        btn_close.clicked.connect(dlg.accept)
        btn_close.setStyleSheet("background-color: #6B7280; color: white; font-weight: bold; padding: 8px; margin-top: 10px;")
        layout.addWidget(btn_close)
        
        dlg.exec()
