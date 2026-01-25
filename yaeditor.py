from PyQt6.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import QWidget, QHBoxLayout 
from pathlib import Path

import sys
# 建立 QApplication
app = QApplication(sys.argv)

current_file_path = None
# 建立主視窗
window = QWidget()
window.setWindowTitle('yaeditor')
window.setGeometry(100, 100, 800, 600)

# 建立布局（左右）
layout = QHBoxLayout()
window.setLayout(layout)

# 左邊（上下）
left_bar = QWidget()
left_layout = QVBoxLayout()
left_bar.setLayout(left_layout)
layout.addWidget(left_bar, stretch=1)

# 建立 QTextEdit（最大）
editor = QTextEdit()
left_layout.addWidget(editor, stretch=1)

# 下方按鈕
#開啟檔案按鈕
open_button = QPushButton("開啟檔案")
left_layout.addWidget(open_button)

# 儲存檔案按鈕
save_button = QPushButton("儲存檔案")
left_layout.addWidget(save_button)

# 開啟資料夾按鈕
open_folder_button = QPushButton("開啟資料夾")
left_layout.addWidget(open_folder_button)

# 建立側邊欄（右側）
side_bar = QWidget()
side_layout = QVBoxLayout()
side_bar.setLayout(side_layout)
layout.addWidget(side_bar)
side_bar.hide()

side_bar.setFixedWidth(200)


def open_file():
    file_path, _ = QFileDialog.getOpenFileName(window, "開啟檔案", "", "所有檔案 (*.*);;文字檔 (*.txt)")
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            editor.setText(file.read())
        global current_file_path
        current_file_path = file_path

open_button.clicked.connect(open_file)

def save_file():
    global current_file_path
    if current_file_path:
        with open(current_file_path, 'w', encoding='utf-8') as file:
            file.write(editor.toPlainText())
        return
    file_path, _ = QFileDialog.getSaveFileName(window, "儲存檔案", "", "所有檔案 (*.*);;文字檔 (*.txt)")

    if file_path:
        current_file_path = file_path
    else:
        return
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(editor.toPlainText())

save_button.clicked.connect(save_file)


# 開啟資料夾功能(遞迴開啟資料夾內所有檔案)
def open_folder():
    folder_path = QFileDialog.getExistingDirectory(window, "開啟資料夾")
    if folder_path:
        show_folder_contents(folder_path)
        
def show_folder_contents(folder_path):
    """顯示資料夾內容"""
    global current_folder_path
    current_folder_path = folder_path

    side_bar.show()
    
    # 清空側邊欄
    for i in reversed(range(side_layout.count())):
        widget = side_layout.itemAt(i).widget()
        if widget:
            widget.deleteLater()
    
    # 列出檔案和資料夾
    for item in sorted(Path(folder_path).iterdir()):
        if item.is_dir():
            btn = QPushButton(f"[{item.name}]")
            btn.clicked.connect(lambda c, p=item: show_folder_contents(str(p)))
        else:
            btn = QPushButton(item.name)
            btn.clicked.connect(lambda c, p=item: open_file_from_path(p))
        side_layout.addWidget(btn)

def open_file_from_path(file_path):
    """從側邊欄開啟檔案"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            editor.setText(f.read())
        global current_file_path
        current_file_path = str(file_path)
    except Exception as e:
        print(f"無法開啟檔案: {e}")

open_folder_button.clicked.connect(open_folder)# 如果有提供檔案路徑參數，則自動開啟該檔案
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
