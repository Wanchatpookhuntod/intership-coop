from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, 
                               QTextEdit, QHBoxLayout, QPushButton)
from utils import create_card

class AddStudentDialog(QDialog):
    def __init__(self, parent=None, title="เพิ่มข้อมูล"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(500, 650)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        form_frame = create_card()
        form = QFormLayout(form_frame)
        form.setSpacing(15)
        
        self.i_id = QLineEdit()
        self.i_name = QLineEdit()
        self.i_name.setFixedWidth(260)
        self.i_loc = QLineEdit()
        self.i_loc.setFixedWidth(260)
        self.i_sec = QComboBox()
        self.i_sec.setFixedWidth(100)
        self.i_sec.addItems(["เอกชน", "ภาครัฐ"])
        self.i_dept = QLineEdit()
        self.i_dept.setFixedWidth(260)
        self.i_addr = QTextEdit()
        self.i_addr.setFixedHeight(70)
        self.i_scope = QTextEdit()
        self.i_scope.setFixedHeight(90)

        form.addRow("รหัสนักศึกษา:", self.i_id)
        form.addRow("ชื่อ-นามสกุล:", self.i_name)
        form.addRow("สถานที่:", self.i_loc)
        form.addRow("ประเภท:", self.i_sec)
        form.addRow("แผนก:", self.i_dept)
        form.addRow("ที่ตั้ง:", self.i_addr)
        form.addRow("ขอบเขต:", self.i_scope)
        
        layout.addWidget(form_frame)

        btns = QHBoxLayout()
        b_ok = QPushButton("บันทึก")
        b_ok.setStyleSheet("background-color: #2563EB; color: white; height: 35px;")
        b_ok.clicked.connect(self.accept)
        
        b_no = QPushButton("ยกเลิก")
        b_no.setStyleSheet("height: 35px; background-color: #E5E7EB; color: #374151;")
        b_no.clicked.connect(self.reject)
        
        btns.addWidget(b_ok)
        btns.addWidget(b_no)
        layout.addLayout(btns)

    def set_data(self, d):
        self.i_id.setText(d.get("student_id",""))
        self.i_name.setText(d.get("name",""))
        self.i_loc.setText(d.get("location",""))
        self.i_sec.setCurrentText(d.get("sector","เอกชน"))
        self.i_dept.setText(d.get("department",""))
        self.i_addr.setText(d.get("address",""))
        self.i_scope.setText(d.get("scope",""))

    def get_data(self):
        return {
            "student_id": self.i_id.text(), "name": self.i_name.text(),
            "location": self.i_loc.text(), "sector": self.i_sec.currentText(),
            "department": self.i_dept.text(), "address": self.i_addr.toPlainText(),
            "scope": self.i_scope.toPlainText()
        }
