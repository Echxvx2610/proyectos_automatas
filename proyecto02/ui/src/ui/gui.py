"""
Editor de texto en PySide6.

Mantiene:
- Menú 'Archivo' (Abrir, Guardar, Salir)
- Menú 'Herramientas' (Analizar y Crear Factura)
- Editor de texto, barra de estado y estilos oscuros.
"""

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTextEdit, QFileDialog, QMessageBox, QSplitter, QDialog
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QSize, Qt

from .dialogs import ClientDataDialog

class TextEditorGUI(QMainWindow):
    """"
    Ventana principal con menús y estilo.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Editor de textos - PySide6')

        # Icono de la aplicación
        self.setWindowIcon(QIcon('ui/assets/icons/buy-cart-market.svg'))

        # Archivo actualmente abierto
        self.current_file = None

        # Widget central y layout
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

        # Editor de texto principal
        self.text_edit = QTextEdit()

        # Textbox para análisis (1/3 del tamaño)
        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        self.analysis_text.setPlaceholderText("Detalles del análisis aparecerán aquí...")

        # Splitter para dividir la pantalla
        splitter = QSplitter()
        splitter.setOrientation(Qt.Vertical)
        splitter.addWidget(self.text_edit)
        splitter.addWidget(self.analysis_text)
        splitter.setSizes([400, 200])  # Aproximadamente 2/3 y 1/3

        layout.addWidget(splitter)

        # Crear acciones y menú
        self._create_actions()
        self._create_menu()

        # Barra de estado
        self.statusBar().showMessage('Listo')

        # Estilo simple
        self._apply_styles()

        # Tamaño inicial
        self.resize(900, 650)

    def _create_actions(self):
        """"
        Crear acciones reutilizables para el menú.
        """
        self.open_action = QAction(QIcon('ui/assets/icons/open-a-file.svg'), 'Abrir', self)
        self.open_action.setShortcut('Ctrl+O')
        self.open_action.triggered.connect(self.open_file)

        self.save_action = QAction(QIcon('ui/assets/icons/save-file.svg'), 'Guardar', self)
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.triggered.connect(self.save_file)

        self.exit_action = QAction(QIcon('ui/assets/icons/exit.svg'), 'Salir', self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.triggered.connect(self.close)

        self.analyze_action = QAction(QIcon('ui/assets/icons/analyze.svg'), 'Analizar', self)
        self.analyze_action.triggered.connect(self.analyze)

        self.create_invoice_action = QAction(QIcon('ui/assets/icons/invoice-receipt.svg'), 'Crear Factura', self)
        self.create_invoice_action.triggered.connect(self.create_invoice)

    def _create_menu(self):
        """"
        Crear menú principal con Archivo y Herramientas.
        """
        menu = self.menuBar()
        file_menu = menu.addMenu('Archivo')
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        tools_menu = menu.addMenu('Herramientas')
        tools_menu.addAction(self.analyze_action)
        tools_menu.addAction(self.create_invoice_action)

    def _apply_styles(self):
        """"
        Aplicar estilos básicos (oscuro) a la UI.
        """
        style = """
        QWidget { background-color: #1e1e2f; color: #e6eef8; font-family: Segoe UI, Arial, sans-serif; }
        QTextEdit { background-color: #0f1724; color: #e6eef8; border: 1px solid #2b2b44; font-size: 14px; }
        QMenuBar { background-color: #161622; color: #cfe3ff; }
        QMenuBar::item { icon-size: 16px; }
        QMenuBar::item:selected { background: #2b2b44; }
        """
        self.setStyleSheet(style)

    def open_file(self):
        """"
        Abrir un archivo .txt y mostrar su contenido.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, 'Abrir archivo', os.getcwd(), 'Text Files (*.txt);;All Files (*)')
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_edit.setPlainText(content)
                self.current_file = file_path
                self.statusBar().showMessage(f'Abierto: {self.current_file}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'No se pudo abrir el archivo:\n{e}')

    def save_file(self):
        """"
        Guardar el contenido actual; preguntar ruta si no hay archivo abierto.
        """
        if not self.current_file:
            file_path, _ = QFileDialog.getSaveFileName(self, 'Guardar archivo', os.getcwd(), 'Text Files (*.txt);;All Files (*)')
            if not file_path:
                return
            self.current_file = file_path

        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(self.text_edit.toPlainText())
            QMessageBox.information(self, 'Guardado', 'Archivo guardado correctamente.')
            self.statusBar().showMessage(f'Guardado: {self.current_file}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'No se pudo guardar el archivo:\n{e}')

    def analyze(self):
        """"
        Acción de análisis (en construcción).
        Aquí iría la lógica de análisis.
        """
        self.analysis_text.setPlainText("Función de análisis: En construcción.\n\nAquí aparecerán los detalles del análisis del texto.")

    def create_invoice(self):
        """
        Acción de crear factura: abre diálogo para datos del cliente.
        """
        dialog = ClientDataDialog(self)
        if dialog.exec() == QDialog.Accepted:
            client_data = dialog.get_client_data()
            # Aquí iría la lógica para generar la factura usando client_data
            # Por ahora, mostrar los datos en el área de análisis
            data_str = "\n".join([f"{k}: {v}" for k, v in client_data.items()])
            self.analysis_text.setPlainText(f"Datos del cliente capturados:\n\n{data_str}\n\nFactura generada (en construcción).")
        else:
            self.statusBar().showMessage('Creación de factura cancelada')