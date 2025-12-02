from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSplitter, 
                               QTableWidget, QHeaderView, QAbstractItemView, QScrollArea, 
                               QFrame, QLabel, QGridLayout, QTableWidgetItem)
from PySide6.QtCore import Qt, Signal
from constants import PROGRESS_ITEMS
from utils import create_card

class ManagementTab(QWidget):
    request_add_signal = Signal()
    request_edit_signal = Signal(int)
    request_track_signal = Signal(int)
    request_delete_signal = Signal(int)

    def __init__(self):
        super().__init__()
        self.records = []
        self.current_selected_row = -1
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        toolbar = QHBoxLayout()
        btn_add = QPushButton(" + เพิ่มนักศึกษา")
        btn_add.clicked.connect(self.request_add_signal.emit)
        btn_add.setFixedHeight(40)
        btn_add.setStyleSheet("background-color: #2563EB; color: white;")
        toolbar.addWidget(btn_add)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(2)
        splitter.setStyleSheet("QSplitter::handle { background-color: #E5E7EB; }")
        
        # Left Panel
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 10, 5, 0)
        
        self.list_table = QTableWidget()
        self.list_table.setColumnCount(2)
        self.list_table.setHorizontalHeaderLabels(["รหัส", "ชื่อ-นามสกุล"])
        self.list_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list_table.setShowGrid(False)
        self.list_table.verticalHeader().setVisible(False)
        self.list_table.cellClicked.connect(self.on_student_selected)
        left_layout.addWidget(self.list_table)
        
        # Right Panel
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(5, 10, 0, 0)

        self.detail_scroll = QScrollArea()
        self.detail_scroll.setWidgetResizable(True)
        self.detail_scroll.setFrameShape(QFrame.NoFrame)
        self.detail_scroll.setStyleSheet("background: transparent;")

        self.detail_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.show_placeholder_detail()
        
        right_layout.addWidget(self.detail_scroll)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 6)

        layout.addWidget(splitter)

    def update_list(self, records):
        self.records = records
        self.list_table.setRowCount(0)
        for row_idx, data in enumerate(records):
            self.list_table.insertRow(row_idx)
            self.list_table.setItem(row_idx, 0, QTableWidgetItem(data["student_id"]))
            self.list_table.setItem(row_idx, 1, QTableWidgetItem(data["name"]))
        
        self.current_selected_row = -1
        self.show_placeholder_detail()

    def on_student_selected(self, row, col):
        self.current_selected_row = row
        self.show_student_detail(row)

    def show_placeholder_detail(self):
        p = QWidget()
        l = QVBoxLayout(p)
        l.setAlignment(Qt.AlignCenter)
        lbl = QLabel("เลือกรายชื่อด้านซ้ายเพื่อดูรายละเอียด")
        lbl.setStyleSheet("color:#9CA3AF; font-size:16px; font-weight:500;")
        l.addWidget(lbl)
        self.detail_scroll.setWidget(p)

    def show_student_detail(self, row_idx):
        data = self.records[row_idx]
        
        content = QWidget()
        content.setStyleSheet(".QWidget { background: transparent; }") 
        layout = QVBoxLayout(content)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(5, 0, 5, 20)
        layout.setSpacing(15)

        # Header
        header_card = create_card()
        header_card.setStyleSheet("QFrame#CardFrame { background-color: #EFF6FF; border: 1px solid #DBEAFE; }")
        h_layout = QVBoxLayout(header_card)
        
        lbl_n = QLabel(data.get("name","-"))
        lbl_n.setStyleSheet("font-size:24px; font-weight:800; color:#1E3A8A; border:none;")
        lbl_id = QLabel(f"รหัส: {data.get('student_id','-')}")
        lbl_id.setStyleSheet("font-size:14px; color:#60A5FA; font-weight:600; border:none;")
        
        h_layout.addWidget(lbl_n)
        h_layout.addWidget(lbl_id)
        layout.addWidget(header_card)

        # Info
        info_card = create_card()
        gl = QGridLayout(info_card)
        gl.setVerticalSpacing(10)
        
        def add_item(r, c, title, val):
            t = QLabel(title)
            t.setStyleSheet("color:#64748B; font-size:12px; font-weight:bold; text-transform:uppercase; border:none;")
            v = QLabel(val)
            v.setWordWrap(True)
            v.setStyleSheet("color:#1F2937; font-size:14px; border:none;")
            gl.addWidget(t, r, c)
            gl.addWidget(v, r+1, c)

        add_item(0, 0, "ประเภท", data.get("sector", "-"))
        add_item(0, 1, "สถานที่ฝึกงาน", data.get("location", "-"))
        add_item(2, 0, "แผนก", data.get("department", "-"))
        add_item(2, 1, "ที่ตั้ง", data.get("address", "-"))
        layout.addWidget(info_card)

        # Scope (FIXED ERROR HERE)
        scope_card = create_card()
        sl = QVBoxLayout(scope_card)
        
        lbl_scope_title = QLabel("ขอบเขตงาน (Job Scope)")
        lbl_scope_title.setStyleSheet("color:#64748B; font-size:12px; font-weight:bold; border:none;")
        sl.addWidget(lbl_scope_title)
        
        scope_val = QLabel(data.get("scope", "-"))
        scope_val.setWordWrap(True)
        scope_val.setStyleSheet("color:#1F2937; margin-top:5px; font-size:14px; border:none;")
        sl.addWidget(scope_val)
        layout.addWidget(scope_card)

        # Progress (FIXED ERROR HERE)
        prog_card = create_card()
        pl = QVBoxLayout(prog_card)
        
        lbl_prog_title = QLabel("ความคืบหน้า (Progress)")
        lbl_prog_title.setStyleSheet("color:#64748B; font-size:12px; font-weight:bold; margin-bottom:10px; border:none;")
        pl.addWidget(lbl_prog_title)
        
        progress = data.get("progress", {})
        for i, (key, label) in enumerate(PROGRESS_ITEMS):
            item = progress.get(key, {})
            done = item.get("status", False) if isinstance(item, dict) else item
            note = item.get("note", "") if isinstance(item, dict) else ""
            grade = item.get("grade", "-") if isinstance(item, dict) else "-"
            
            row_w = QFrame()
            bg_color = "#ECFDF5" if done else "#FEF2F2"
            border_c = "#10B981" if done else "#EF4444"
            row_w.setStyleSheet(f"""
                QFrame {{
                    background-color: {bg_color}; 
                    border-radius: 6px; 
                    border-left: 4px solid {border_c};
                }}
            """)
            
            rl = QVBoxLayout(row_w)

            


            rl.setContentsMargins(10, 8, 10, 8)
            
            top_line = QHBoxLayout()
            lbl_title = QLabel(label)
            lbl_title.setStyleSheet("font-weight: bold; font-size: 14px; border:none; background:transparent;")
            
            icon = "✅ เรียบร้อย" if done else "❌ ยังไม่ทำ"
            color = "#059669" if done else "#DC2626"
            lbl_icon = QLabel(icon)
            lbl_icon.setStyleSheet(f"color: {color}; font-weight:bold; border:none; background:transparent;")
            
            top_line.addWidget(lbl_title)
            top_line.addStretch()
            top_line.addWidget(lbl_icon)
            rl.addLayout(top_line)
            
            if grade != "-":
                lbl_g = QLabel(f"⭐ เกรด: {grade}")
                lbl_g.setStyleSheet("color: #D97706; font-weight:bold; font-size: 13px; margin-top: 4px; border:none; background:transparent;")
                rl.addWidget(lbl_g)

            if note:
                lbl_n = QLabel(f"📝 {note}")
                lbl_n.setWordWrap(True)
                lbl_n.setStyleSheet("color: #4B5563; font-size: 13px; margin-top: 4px; border:none; background:transparent;")
                rl.addWidget(lbl_n)
            
            pl.addWidget(row_w)
            pl.addSpacing(5)

           

        layout.addWidget(prog_card)

        # Buttons
        btn_layout = QHBoxLayout()
        
        b_edit = QPushButton("แก้ไขข้อมูล")
        b_edit.clicked.connect(lambda _, r=row_idx: self.request_edit_signal.emit(r))
        b_edit.setFixedHeight(40)
        b_edit.setStyleSheet("background-color: #F59E0B; color: black;") 
        
        b_track = QPushButton("บันทึก/ติดตามงาน")
        b_track.clicked.connect(lambda _, r=row_idx: self.request_track_signal.emit(r))
        b_track.setFixedHeight(40)
        b_track.setStyleSheet("background-color: #8B5CF6; color: white;") 
        
        b_del = QPushButton("ลบ")
        b_del.clicked.connect(lambda _, r=row_idx: self.request_delete_signal.emit(r))
        b_del.setFixedHeight(40)
        b_del.setStyleSheet("background-color: #EF4444; color: white;")

        btn_layout.addWidget(b_edit)
        btn_layout.addWidget(b_track)
        btn_layout.addStretch()
        btn_layout.addWidget(b_del)
        
        layout.addSpacing(15)
        layout.addLayout(btn_layout)
        layout.addStretch()

        self.detail_scroll.setWidget(content)
