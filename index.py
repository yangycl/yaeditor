from PyQt6.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt6.QtGui import QShortcut, QKeySequence
import sys
# 建立 QApplication
app = QApplication(sys.argv)

current_file_path = None
# 建立主視窗
window = QWidget()
window.setWindowTitle('yaeditor')
window.setGeometry(100, 100, 800, 600)

# 建立布局
layout = QVBoxLayout()
window.setLayout(layout)

# 建立 QTextEdit
editor = QTextEdit()
layout.addWidget(editor)

# 開啟檔案按鈕
open_button = QPushButton("開啟檔案")
layout.addWidget(open_button)

def open_file():
    file_path, _ = QFileDialog.getOpenFileName(window, "開啟檔案", "", "所有檔案 (*.*);;文字檔 (*.txt)")
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            editor.setText(file.read())
        global current_file_path
        current_file_path = file_path

open_button.clicked.connect(open_file)

# 儲存檔案按鈕
save_button = QPushButton("儲存檔案")
layout.addWidget(save_button)

def save_file():
    global current_file_path
    if current_file_path:
        with open(current_file_path, 'w', encoding='utf-8') as file:
            file.write(editor.toPlainText())
        return
    file_path, _ = QFileDialog.getSaveFileName(window, "儲存檔案", "", "所有檔案 (*.*);;文字檔 (*.txt)")

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(editor.toPlainText())

save_button.clicked.connect(save_file)

if len(sys.argv) > 1:
    file_path = sys.argv[1]
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            editor.setText(file.read())
    except Exception as e:
        print(f"無法開啟檔案: {e}")
QShortcut(QKeySequence("Ctrl+O"), window).activated.connect(open_file)
QShortcut(QKeySequence("Ctrl+S"), window).activated.connect(save_file)# 顯示主視窗
window.show()

# 啟動事件迴圈
sys.exit(app.exec())
