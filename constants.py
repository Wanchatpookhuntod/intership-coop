DEFAULT_FILENAME = "db_students.json"

PROGRESS_ITEMS = [
    ("report_2m", "1. รายงาน 2 เดือน"),
    ("supervision_1", "2. นิเทศ #1"),
    ("supervision_2", "3. นิเทศ #2"),
    ("project", "4. โครงงาน"),
    ("report_send", "5. ส่งเล่ม"),
    ("final_present", "6. ปัจฉิมฯ")
]

GRADES = ["-", "A+", "A", "B+", "B", "C+", "C", "D+", "D", "F"]

MODERN_STYLESHEET = """
    QMainWindow, QDialog, QWidget#CentralWidget { background-color: #F3F4F6; }
    QWidget { font-family: "Sarabun", "Helvetica Neue", Arial, sans-serif; font-size: 14px; color: #1F2937; }
    QFrame#CardFrame { background-color: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 10px; }
    QLineEdit, QTextEdit, QComboBox { background-color: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 6px; padding: 8px; }
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus { border: 2px solid #2563EB; }
    QPushButton { border-radius: 6px; padding: 8px 12px; font-weight: bold; border: none; }
    QPushButton:hover { opacity: 0.9; }
    QPushButton:pressed { opacity: 0.8; }
    QTableWidget { background-color: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 8px; gridline-color: transparent; selection-background-color: #EFF6FF; selection-color: #1E3A8A; }
    QHeaderView::section { background-color: #F9FAFB; padding: 10px; border: none; border-bottom: 2px solid #E5E7EB; font-weight: bold; color: #4B5563; text-transform: uppercase; font-size: 12px; }
    QTableWidget::item { padding: 8px; border-bottom: 1px solid #F3F4F6; }
    QTabWidget::pane { border: 1px solid #E5E7EB; background: #FFFFFF; border-radius: 8px; }
    QTabBar::tab { background: #E5E7EB; color: #6B7280; padding: 10px 20px; border-top-left-radius: 6px; border-top-right-radius: 6px; margin-right: 2px; font-weight: bold; }
    QTabBar::tab:selected { background: #FFFFFF; color: #2563EB; border-bottom: 3px solid #2563EB; }
"""
