import os
import json
import csv
from PySide6.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QStackedWidget, QTabWidget, 
                               QMessageBox, QFileDialog, QFrame, QDialog)
from PySide6.QtCore import Qt, QMarginsF, QDate
from PySide6.QtGui import QIcon, QPixmap, QTextDocument, QPageSize, QPageLayout, QAction
from PySide6.QtPrintSupport import QPrinter

from constants import DEFAULT_FILENAME, MODERN_STYLESHEET, PROGRESS_ITEMS
from ui.management_tab import ManagementTab
from ui.overview_tab import OverviewTab
from ui.progress_page import ProgressPage
from ui.dialogs import AddStudentDialog
from pdf_handler import PDFHandler

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title_window = "ระบบจัดการข้อมูลนักศึกษาฝึกงานและสหกิจศึกษา"
        self.records = []
        self.current_filename = DEFAULT_FILENAME
        
        app = QApplication.instance()
        app.setStyleSheet(MODERN_STYLESHEET)
        
        self.init_ui()
        self.load_initial_data()


    def init_ui(self):
        # กำหนด Flag เพื่อซ่อนไอคอนสำหรับหน้าต่างหลัก
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)
        
        # ใช้ไอคอนโปร่งใส
        p = QPixmap(1, 1)
        p.fill(Qt.transparent)
        self.setWindowIcon(QIcon(p))

        self.setWindowTitle(f"{self.title_window} *{self.current_filename}")
        self.resize(1200, 850)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("ไฟล์ (File)")
        
        act_new = QAction("สร้างไฟล์ใหม่", self); act_new.setShortcut("Ctrl+N"); act_new.triggered.connect(self.new_file)
        act_open = QAction("เปิดไฟล์", self); act_open.setShortcut("Ctrl+O"); act_open.triggered.connect(self.open_file)
        act_save = QAction("บันทึก", self); act_save.setShortcut("Ctrl+S"); act_save.triggered.connect(self.save_file)
        act_save_as = QAction("บันทึกเป็น...", self); act_save_as.setShortcut("Ctrl+Shift+S"); act_save_as.triggered.connect(self.save_file_as)
        
        file_menu.addAction(act_new)
        file_menu.addAction(act_open)
        file_menu.addAction(act_save)
        file_menu.addAction(act_save_as)
        file_menu.addSeparator()
        file_menu.addAction(QAction("Export CSV", self, triggered=self.export_csv))
        file_menu.addAction(QAction("Export PDF", self, triggered=self.export_pdf))
        file_menu.addSeparator()
        file_menu.addAction(QAction("ออก", self, triggered=self.close))

        main_toolbar = QHBoxLayout()
        main_toolbar.setContentsMargins(15, 10, 15, 5)
        
        lbl_brand = QLabel("Internship Manager")
        lbl_brand.setStyleSheet("font-size: 18px; font-weight: bold; color: #2563EB;")
        
        btn_save = QPushButton("บันทึก"); btn_save.clicked.connect(self.save_file)
        btn_save.setStyleSheet("background-color: #2563EB; color: white; width: 100px;")
        
        btn_export = QPushButton("Export CSV"); btn_export.clicked.connect(self.export_csv)
        btn_export.setStyleSheet("background-color: #2563EB; color: white; width: 100px;")

        btn_pdf = QPushButton("Export PDF"); btn_pdf.clicked.connect(self.export_pdf)
        btn_pdf.setStyleSheet("background-color: #2563EB; color: white; width: 100px;")
        
        main_toolbar.addWidget(lbl_brand)
        main_toolbar.addStretch()
        main_toolbar.addWidget(btn_save)
        main_toolbar.addWidget(btn_export)
        main_toolbar.addWidget(btn_pdf)

        central = QWidget(); self.setCentralWidget(central)
        main_vbox = QVBoxLayout(central)
        main_vbox.setContentsMargins(0, 0, 0, 0)
        
        # Wrap toolbar in a widget to prevent overlapping
        toolbar_wrapper = QWidget()
        toolbar_wrapper.setLayout(main_toolbar)
        toolbar_wrapper.setStyleSheet("background-color: white;")
        main_vbox.addWidget(toolbar_wrapper)

        self.stack = QStackedWidget()
        
        # Tab Container
        self.tabs = QTabWidget()
        self.tab_mgmt = ManagementTab()
        self.tab_view = OverviewTab()
        self.tabs.addTab(self.tab_mgmt, " จัดการข้อมูล ")
        self.tabs.addTab(self.tab_view, " ภาพรวมความคืบหน้า ")
        self.tabs.currentChanged.connect(self.on_tab_changed)
        
        self.stack.addWidget(self.tabs) # Index 0

        # Progress Form
        self.page_progress = ProgressPage()
        self.stack.addWidget(self.page_progress) # Index 1
        
        main_vbox.addWidget(self.stack)

        # Connections
        self.tab_mgmt.request_add_signal.connect(self.add_record)
        self.tab_mgmt.request_edit_signal.connect(self.edit_record)
        self.tab_mgmt.request_delete_signal.connect(self.delete_record)
        self.tab_mgmt.request_track_signal.connect(self.switch_to_progress_page)

        self.page_progress.go_back_signal.connect(self.switch_to_tabs_page)
        self.page_progress.save_completed_signal.connect(self.on_progress_saved)

        self.status_label = QLabel("พร้อมทำงาน")
        self.status_label.setStyleSheet("padding: 5px; color: #666;")
        self.statusBar().addWidget(self.status_label)

    def switch_to_progress_page(self, row_idx):
        student = self.records[row_idx]
        self.page_progress.load_data(student)
        self.stack.setCurrentIndex(1)
        self.status_label.setText(f"กำลังบันทึกข้อมูลของ: {student['name']}")

    def switch_to_tabs_page(self):
        self.stack.setCurrentIndex(0)
        self.status_label.setText("หน้าหลัก")

    def on_tab_changed(self, index):
        if index == 1:
            self.tab_view.update_table(self.records)

    def on_progress_saved(self):
        self.tab_mgmt.update_list(self.records)
        if self.tab_mgmt.current_selected_row != -1:
             self.tab_mgmt.show_student_detail(self.tab_mgmt.current_selected_row)

    def load_initial_data(self):
        if os.path.exists(DEFAULT_FILENAME):
            self.load_json(DEFAULT_FILENAME)
    
    def load_json(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.records = json.load(f)
            self.current_filename = filename
            self.tab_mgmt.update_list(self.records)
            self.tab_view.update_table(self.records)
            self.setWindowTitle(f"{self.title_window} *{self.current_filename}")
        except: pass

    def new_file(self):
        if QMessageBox.question(self, "สร้างใหม่", "ข้อมูลที่ยังไม่บันทึกจะหายไป ยืนยัน?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            self.records = []; self.current_filename = "Untitled.json"
            self.tab_mgmt.update_list(self.records)
            self.tab_view.update_table(self.records)
            self.setWindowTitle(f"- {self.current_filename}")

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open", "", "JSON (*.json)")
        if path: self.load_json(path)

    def save_file(self):
        if self.current_filename == "Untitled.json": self.save_file_as()
        else: self.save_to_path(self.current_filename)

    def save_file_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save As", "", "JSON (*.json)")
        if path: self.save_to_path(path)

    def save_to_path(self, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, ensure_ascii=False, indent=4)
            self.current_filename = filename
            self.setWindowTitle(f"ระบบจัดการข้อมูล - {self.current_filename}")
            QMessageBox.information(self, "สำเร็จ", "บันทึกเรียบร้อย")
        except Exception as e: QMessageBox.critical(self, "Error", str(e))

    def add_record(self):
        dialog = AddStudentDialog(self, "เพิ่มข้อมูล")
        if dialog.exec() == QDialog.Accepted:
            new_d = dialog.get_data(); new_d["progress"] = {}
            self.records.append(new_d)
            self.tab_mgmt.update_list(self.records)
            self.status_label.setText("เพิ่มข้อมูลแล้ว")

    def edit_record(self, row_idx):
        d = self.records[row_idx]
        dialog = AddStudentDialog(self, "แก้ไขข้อมูล")
        dialog.set_data(d)
        if dialog.exec() == QDialog.Accepted:
            new_d = dialog.get_data()
            new_d["progress"] = d.get("progress", {})
            self.records[row_idx] = new_d
            self.tab_mgmt.update_list(self.records)
            self.tab_mgmt.show_student_detail(row_idx)

    def delete_record(self, row_idx):
        name = self.records[row_idx]['name']
        if QMessageBox.question(self, "ลบ", f"ลบ {name}?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            del self.records[row_idx]
            self.tab_mgmt.update_list(self.records)

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export", "", "CSV (*.csv)")
        if path:
            try:
                with open(path, 'w', encoding='utf-8-sig', newline='') as f:
                    cols = ["student_id", "name", "location", "sector", "department", "address", "scope"]
                    for k,_ in PROGRESS_ITEMS: cols.extend([f"Status_{k}", f"Note_{k}"])
                    writer = csv.DictWriter(f, fieldnames=cols); writer.writeheader()
                    for r in self.records:
                        row = {c: r.get(c,"") for c in ["student_id", "name", "location", "sector", "department", "address", "scope"]}
                        prog = r.get("progress", {})
                        for k,_ in PROGRESS_ITEMS:
                            item = prog.get(k, {})
                            done = item.get("status", False) if isinstance(item, dict) else item
                            note = item.get("note", "") if isinstance(item, dict) else ""
                            row[f"Status_{k}"] = "1" if done else "0"
                            row[f"Note_{k}"] = note
                        writer.writerow(row)
                QMessageBox.information(self, "สำเร็จ", "Export CSV แล้ว")
            except Exception as e: QMessageBox.critical(self, "Error", str(e))

    def export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export PDF", "", "PDF (*.pdf)")
        if not path:
            return

        success, message = PDFHandler.export_pdf(self.records, path)
        if success:
            QMessageBox.information(self, "สำเร็จ", message)
        else:
            QMessageBox.critical(self, "Error", f"เกิดข้อผิดพลาด: {message}")