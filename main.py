import sys
import os
from PyQt6.QtWidgets import QApplication
from src.gui.main_window import MainWindow


def main():
    # Добавляем путь к модулям
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    app = QApplication(sys.argv)
    app.setApplicationName("Дискретные случайные величины")
    
    main_window = MainWindow()
    main_window.show()
    
    try:
        sys.exit(app.exec())
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()