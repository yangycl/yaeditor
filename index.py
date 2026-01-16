from PyQt6.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout, QPushButton, QFileDialog
import sys

# 建立 QApplication
app = QApplication(sys.argv)

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

open_button.clicked.connect(open_file)

# 儲存檔案按鈕
save_button = QPushButton("儲存檔案")
layout.addWidget(save_button)

def save_file():
    file_path, _ = QFileDialog.getSaveFileName(window, "儲存檔案", "", "所有檔案 (*.*);;文字檔 (*.txt)")
    if file_path:
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
# 顯示主視窗
window.show()

# 啟動事件迴圈
sys.exit(app.exec())
