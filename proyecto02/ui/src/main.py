"""
Punto de entrada de la aplicación.
"""

import sys
from PySide6.QtWidgets import QApplication

from ui.gui import TextEditorGUI


def main():
    app = QApplication(sys.argv)
    window = TextEditorGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()