from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                               QScrollArea, QFrame, QGroupBox, QGridLayout, QCheckBox, 
                               QComboBox, QTextEdit, QMessageBox)
from PySide6.QtCore import Qt, Signal
from constants import PROGRESS_ITEMS, GRADES

class ProgressPage(QWidget):
    go_back_signal = Signal()
    save_completed_signal = Signal()

    def __init__(self):
        super().__init__()
        self.student_data = {}
        self.widgets = {}
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 1. Header Area
        header_layout = QHBoxLayout()

        btn_back = QPushButton("บันทึกและย้อนกลับ") # เปลี่ยนชื่อปุ่มให้ชัดเจน
        btn_back.setStyleSheet("""
            QPushButton {
                background-color: #64748B; 
                color: white; 
                font-size: 14px; 
                padding: 8px 8px;
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #475569; }
        """)
        btn_back.setFixedWidth(180)
        btn_back.clicked.connect(self.go_back_with_save) # เปลี่ยนฟังก์ชันเชื่อมต่อ
        
        lbl_title = QLabel("บันทึกการติดตามงาน")
        lbl_title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1E293B;")
        
        header_layout.addWidget(btn_back)
        header_layout.addSpacing(15)
        header_layout.addWidget(lbl_title)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # 2. Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        

        content_widget.setStyleSheet("background: transparent;")
        self.content_layout = QVBoxLayout(content_widget)

        # 2.1 Info Card
        self.info_group = QGroupBox("ข้อมูลนักศึกษา")
        self.info_layout = QGridLayout()
        self.info_layout.setVerticalSpacing(10)
        self.info_group.setLayout(self.info_layout)
        self.content_layout.addWidget(self.info_group)

        # 2.2 Progress Checklist Card
        prog_group = QGroupBox("รายการตรวจสอบ (Checklist)")
        self.prog_grid = QGridLayout()
        self.prog_grid.setColumnStretch(1, 1)
        self.prog_grid.setVerticalSpacing(15)
        
        # Header ของตาราง
        lbl_status = QLabel("สถานะ")
        lbl_status.setStyleSheet("font-weight:bold; color:#6B7280; font-size:14px;")
        self.prog_grid.addWidget(lbl_status, 0, 0)

        lbl_grade = QLabel("ผลการประเมิน")
        lbl_grade.setStyleSheet("font-weight:bold; color:#6B7280; font-size:14px;")
        self.prog_grid.addWidget(lbl_grade, 0, 1)

        lbl_note = QLabel("บันทึกเพิ่มเติม / หมายเหตุ")
        lbl_note.setStyleSheet("font-weight:bold; color:#6B7280; font-size:14px;")
        self.prog_grid.addWidget(lbl_note, 0, 2)

        for i, (key, label) in enumerate(PROGRESS_ITEMS):
            row = i + 1
            
            # สร้าง Checkbox พร้อม Style ชัดเจน
            chk = QCheckBox(label)
            chk.setStyleSheet("""
                QCheckBox {
                    font-weight: bold; 
                    color: #374151; 
                    font-size: 15px;
                    padding: 5px;
                }
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                    border: 2px solid #9CA3AF;
                    border-radius: 4px;
                    background: white;
                }
                QCheckBox::indicator:checked {
                    background: #2563EB;
                    border: 2px solid #2563EB;
                    image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIzIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwb2x5bGluZSBwb2ludHM9IjIwIDYgOSAxNyA0IDEyIi8+PC9zdmc+);
                }
                QCheckBox::indicator:hover {
                    border-color: #2563EB;
                }
            """)
            
            combo = QComboBox()
            combo.addItems(GRADES)
            combo.setFixedWidth(80)
            combo.setEnabled(False)  # เริ่มต้นปิดการใช้งาน

            txt = QTextEdit()
            txt.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            txt.setStyleSheet("background-color: white; font-size: 14px; color: #333;")
            txt.setPlaceholderText("ระบุรายละเอียด...")
            txt.setFixedHeight(50)
            txt.setEnabled(False)  # เริ่มต้นปิดการใช้งาน
            
            # เชื่อมต่อสัญญาณ stateChanged ของ Checkbox
            # ใช้ functools.partial หรือ lambda ที่จับค่าตัวแปรให้ถูกต้อง
            chk.stateChanged.connect(lambda state, c=combo, t=txt: self.toggle_fields(state, c, t))
            
            self.prog_grid.addWidget(chk, row, 0, Qt.AlignTop)
            self.prog_grid.addWidget(combo, row, 1, Qt.AlignTop)
            self.prog_grid.addWidget(txt, row, 2)
            self.widgets[key] = (chk, combo, txt)

        prog_group.setLayout(self.prog_grid)
        self.content_layout.addWidget(prog_group)
        self.content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        # 3. Footer Save Button
        btn_save = QPushButton("บันทึกข้อมูล")
        btn_save.setFixedHeight(50)
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #2563EB; 
                color: white; 
                font-size: 16px; 
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #1D4ED8; }
        """)
        btn_save.clicked.connect(self.save_data_manual)
        main_layout.addWidget(btn_save)

    def toggle_fields(self, state, combo, txt):
        """เปิด/ปิดการใช้งาน ComboBox และ TextEdit ตามสถานะของ Checkbox"""
        # stateChanged ส่งค่า int: 0 (Unchecked), 2 (Checked)
        is_checked = (state == 2) 
        combo.setEnabled(is_checked)
        txt.setEnabled(is_checked)
        
        # ถ้าไม่ได้เช็ค ให้รีเซ็ตค่ากลับเป็นค่าเริ่มต้น
        if not is_checked:
            combo.setCurrentIndex(0)  # รีเซ็ตเกรดเป็น "-"
            txt.clear()  # ล้างข้อความ

    def load_data(self, data):
        self.student_data = data
        progress_data = data.get("progress", {})

        # Clear Info Layout
        for i in reversed(range(self.info_layout.count())): 
            self.info_layout.itemAt(i).widget().setParent(None)

        def add_info(r, c, label, value, colspan=1):
            lbl_t = QLabel(label)
            lbl_t.setStyleSheet("color: #64748B; font-size: 12px; font-weight: bold; text-transform: uppercase;")
            lbl_v = QLabel(value)
            lbl_v.setStyleSheet("color: #111827; font-weight: 500; font-size: 15px;")
            lbl_v.setWordWrap(True)
            self.info_layout.addWidget(lbl_t, r, c)
            self.info_layout.addWidget(lbl_v, r+1, c, 1, colspan)

        add_info(0, 0, "รหัสนักศึกษา", data.get("student_id", "-"))
        add_info(0, 1, "ชื่อ-นามสกุล", data.get("name", "-"))
        add_info(0, 2, "ประเภท", data.get("sector", "-"))
        add_info(2, 0, "สถานที่ฝึกงาน", data.get("location", "-"))
        add_info(2, 1, "แผนก", data.get("department", "-"))

        for key, (chk, combo, txt) in self.widgets.items():
            item_data = progress_data.get(key, {})
            # โหลดสถานะ Checkbox ให้ถูกต้อง
            if isinstance(item_data, bool):
                chk.setChecked(item_data)
                combo.setCurrentIndex(0)
                txt.setPlainText("")
                combo.setEnabled(item_data)
                txt.setEnabled(item_data)
            else:
                is_checked = item_data.get("status", False)
                chk.setChecked(is_checked)
                combo.setCurrentText(item_data.get("grade", "-"))
                txt.setPlainText(item_data.get("note", ""))
                combo.setEnabled(is_checked)
                txt.setEnabled(is_checked)

    def perform_save(self):
        """ฟังก์ชันบันทึกข้อมูลจริง"""
        new_progress = {}
        for key, (chk, combo, txt) in self.widgets.items():
            new_progress[key] = {
                "status": chk.isChecked(),
                "grade": combo.currentText(),
                "note": txt.toPlainText().strip()
            }
        self.student_data["progress"] = new_progress
        self.save_completed_signal.emit()

    def save_data_manual(self):
        """กดปุ่มบันทึกด้านล่าง"""
        self.perform_save()
        QMessageBox.information(self, "สำเร็จ", "บันทึกข้อมูลเรียบร้อย")
        self.go_back_signal.emit()

    def go_back_with_save(self):
        """กดปุ่มย้อนกลับด้านบน (Auto Save)"""
        self.perform_save()
        self.go_back_signal.emit()
