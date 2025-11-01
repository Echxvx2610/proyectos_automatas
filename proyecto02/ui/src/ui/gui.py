import sys
import os

# Configurar sys.path para importar módulos correctamente
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../"))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTextEdit, QFileDialog, QMessageBox, QSplitter, QDialog
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt

from .dialogs import ClientDataDialog

# Importar desde los módulos correctos
from fruitLoops.main import search_fruits, get_fruit_pattern
from invoiceGenerator.main import procesar_texto_compra

# print(current_dir)
# print(project_root)

class TextEditorGUI(QMainWindow):
    """
    Ventana principal con menús y estilo.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Editor de textos - PySide6')

        # Icono de la aplicación
        icon_path = os.path.join(current_dir, '../assets/icons/buy-cart-market.svg')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

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
        splitter.setSizes([400, 200])

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
        """
        Crear acciones reutilizables para el menú.
        """
        assets_dir = os.path.join(current_dir, '../assets/icons')
        
        self.open_action = QAction(QIcon(os.path.join(assets_dir, 'open-a-file.svg')), 'Abrir', self)
        self.open_action.setShortcut('Ctrl+O')
        self.open_action.triggered.connect(self.open_file)

        self.save_action = QAction(QIcon(os.path.join(assets_dir, 'save-file.svg')), 'Guardar', self)
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.triggered.connect(self.save_file)

        self.exit_action = QAction(QIcon(os.path.join(assets_dir, 'exit.svg')), 'Salir', self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.triggered.connect(self.close)

        self.analyze_action = QAction(QIcon(os.path.join(assets_dir, 'analyze.svg')), 'Analizar', self)
        self.analyze_action.triggered.connect(self.analyze)

        self.create_invoice_action = QAction(QIcon(os.path.join(assets_dir, 'invoice-receipt.svg')), 'Crear Factura', self)
        self.create_invoice_action.triggered.connect(self.create_invoice)

    def _create_menu(self):
        """
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
        """
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
        """
        Abrir un archivo .txt y mostrar su contenido.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            'Abrir archivo', 
            os.getcwd(), 
            'Text Files (*.txt);;All Files (*)'
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_edit.setPlainText(content)
                self.current_file = file_path
                self.statusBar().showMessage(f'Abierto: {self.current_file}')
                self.analysis_text.clear()
                self.analysis_text.insertPlainText(f'Archivo cargado. Use "Analizar" o "Crear Factura".\n')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'No se pudo abrir el archivo:\n{e}')

    def save_file(self):
        """
        Guardar el contenido actual; preguntar ruta si no hay archivo abierto.
        """
        if not self.current_file:
            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                'Guardar archivo', 
                os.getcwd(), 
                'Text Files (*.txt);;All Files (*)'
            )
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

    # parte uno
    def analyze(self):
        """
        Analizar el texto actual y mostrar resultados en el área de análisis.
        """
        fruits = [
            'naranja', 'mandarina', 'toronja', 
            'fresa', 'guayaba', 'limón',
            'piña', 'mango', 'papaya', 
            'melón', 'sandía', 'ciruela', 
            'durazno', 'higo', 'pera', 
            'tuna', 'manzana', 'uva', 
            'granada'
        ]
        
        content = self.text_edit.toPlainText()
        fruits_counts, fruits_per_month = search_fruits(content, fruits)

        if fruits_counts is None:
            return

        unique_fruits = [fruit for fruit, count in fruits_counts.items() if count > 0]

        self.analysis_text.clear()
        self.analysis_text.insertPlainText("[1]. Detectar el número de frutas sin repetir:\n")
        self.analysis_text.insertPlainText("-" * 60 + "\n")
        self.analysis_text.insertPlainText(f"Frutas encontradas sin repetir: {len(unique_fruits)}\n")
        self.analysis_text.insertPlainText(f"   {', '.join(sorted(unique_fruits))}\n\n")

        self.analysis_text.insertPlainText("[2]. Indicar cuántas frutas hay en cada mes:\n") 
        self.analysis_text.insertPlainText("-" * 60 + "\n")
        self.analysis_text.insertPlainText("Frutas por mes:\n")

        meses_orden = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                       'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    
        for mes in meses_orden:
            if mes in fruits_per_month:
                lista = fruits_per_month[mes]
                self.analysis_text.insertPlainText(f"{mes:12} → {len(lista)} frutas: {', '.join(lista)}\n")
            else:
                self.analysis_text.insertPlainText(f"{mes:12} → 0 frutas\n")

        self.analysis_text.insertPlainText("\n[3]. Indicar cuántas veces aparece el nombre de cada fruta:\n")
        self.analysis_text.insertPlainText("-" * 60 + "\n")
        self.analysis_text.insertPlainText("\nFrecuencia de aparición:\n\n")
        for fruit, count in fruits_counts.items():
            if count > 0:
                self.analysis_text.insertPlainText(
                    f"{fruit.capitalize():12} → {count} vez{'es' if count != 1 else ''}\n"
                )

    # parte dos
    def create_invoice(self):
        """
        Acción de crear factura: genera HTML y PDF usando HTMLInvoiceGenerator.
        Procesa el texto del editor para extraer las compras de frutas.
        """
        # Importar el generador de facturas HTML
        try:
            from invoiceGenerator.html_invoice_generator import HTMLInvoiceGenerator
        except ImportError as e:
            QMessageBox.critical(
                self,
                'Error de importación',
                f'No se pudo importar HTMLInvoiceGenerator:\n{str(e)}\n\n'
                f'Verifique la estructura del proyecto.'
            )
            print(str(e))
            return
        
        # ====== PROCESAMIENTO DEL TEXTO PARA EXTRAER COMPRAS ======
        content = self.text_edit.toPlainText()
        
        if not content.strip():
            QMessageBox.warning(
                self,
                'Editor vacío',
                'No hay texto en el editor para procesar.\n\n'
                'Por favor, escriba o cargue un texto con compras de frutas.'
            )
            return
        
        try:
            # Procesar el texto para obtener total y desglose
            resultado = procesar_texto_compra(content)
            
            if resultado is None:
                QMessageBox.warning(
                    self,
                    'Sin compras detectadas',
                    'No se detectaron compras de frutas en el texto.\n\n'
                    'Ejemplo de formato válido:\n'
                    '"Compré 2 kg de naranjas, 3 piezas de mango y 1.5 kg de uvas."'
                )
                return
            
            total, desglose = resultado
            
            if not desglose:
                QMessageBox.warning(
                    self,
                    'Sin compras válidas',
                    'No se pudieron procesar las compras del texto.\n\n'
                    'Verifique que el formato sea correcto.'
                )
                return
            
            # Convertir el desglose a formato de items para la factura
            items = []
            for item in desglose:
                items.append({
                    'quantity': item['cantidad'],
                    'unit': item['unidad'],
                    'description': item['fruta'],
                    'unit_price': item['precio_unitario']
                })
            
            # Mostrar resumen antes de generar
            resumen = f"Total de compra: ${total:.2f}\n\nItems detectados:\n"
            for item in desglose:
                resumen += f"• {item['fruta']}: {item['cantidad']} {item['unidad']} × ${item['precio_unitario']} = ${item['subtotal']:.2f}\n"
            
            self.analysis_text.clear()
            self.analysis_text.insertPlainText("=" * 60 + "\n")
            self.analysis_text.insertPlainText("COMPRAS DETECTADAS\n")
            self.analysis_text.insertPlainText("=" * 60 + "\n\n")
            self.analysis_text.insertPlainText(resumen)
            self.analysis_text.insertPlainText("\n" + "=" * 60 + "\n")
            
        except Exception as e:
            import traceback
            QMessageBox.critical(
                self,
                'Error al procesar texto',
                f'Error al analizar el texto:\n\n{str(e)}\n\n{traceback.format_exc()[:300]}'
            )
            return
        
        # Abrir diálogo para datos del cliente
        dialog = ClientDataDialog(self)
        
        if dialog.exec() == QDialog.Accepted:
            client_data = dialog.get_client_data()
            
            # Pedir ubicación para guardar (HTML)
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                'Guardar Factura',
                'factura.html',
                'HTML Files (*.html);;All Files (*)'
            )
            
            if not file_path:
                self.statusBar().showMessage('Guardado cancelado')
                return
            
            try:
                # Mostrar que está procesando
                self.statusBar().showMessage('Generando factura HTML y PDF...')
                
                # Datos de la empresa (puedes personalizarlos)
                company_data = {
                    'name': 'LA FRUTERIA S.A. DE C.V.',
                    'fiscal_name': 'La Fruteria Sociedad Anónima de Capital Variable',
                    'rfc': 'FMA123456ABC',
                    'address': 'Calle Venustiano Carranza #782, Col. Centro, Ensenada, CP 12345',
                    'phone': '646-245-4452',
                    'website': 'www.lafruteria.com',
                    'tax_regime': 'Régimen General de Ley'
                }
                
                # Generar factura HTML + PDF
                generator = HTMLInvoiceGenerator()
                
                result = generator.generate_invoice(
                    company_data=company_data,
                    client_data=client_data, 
                    items=items,
                    output_html=file_path, 
                    generate_pdf=True,
                    pdf_method='pdfkit'  # alternar entre 'weasyprint' y 'pdfkit'
                )
                
                # Preparar mensaje
                if result['pdf']:
                    mensaje = (
                        f'Factura generada exitosamente\n\n'
                        f'HTML: {os.path.basename(result["html"])}\n'
                        f'PDF:  {os.path.basename(result["pdf"])}\n\n'
                        f'Total: ${result["totals"]["total"]:,.2f}'
                    )
                else:
                    mensaje = (
                        f'Factura HTML generada\n'
                        f'No se pudo generar PDF\n\n'
                        f'HTML: {os.path.basename(result["html"])}\n\n'
                        f'Total: ${result["totals"]["total"]:,.2f}\n\n'
                        f'Nota: Para generar PDF, instale WeasyPrint o pdfkit:\n'
                        f'pip install weasyprint o pip install pdfkit'
                    )
                
                QMessageBox.information(self, 'Factura Generada', mensaje)
                
                # Mostrar resumen completo
                self.analysis_text.clear()
                self.analysis_text.insertPlainText("=" * 60 + "\n")
                self.analysis_text.insertPlainText("FACTURA GENERADA EXITOSAMENTE\n")
                self.analysis_text.insertPlainText("=" * 60 + "\n\n")
                
                self.analysis_text.insertPlainText("ARCHIVOS:\n")
                self.analysis_text.insertPlainText("-" * 60 + "\n")
                self.analysis_text.insertPlainText(f"HTML: {result['html']}\n")
                if result['pdf']:
                    self.analysis_text.insertPlainText(f"PDF:  {result['pdf']}\n")
                else:
                    self.analysis_text.insertPlainText(f"PDF:  No generado (instale WeasyPrint)\n")
                
                self.analysis_text.insertPlainText("\nDATOS DE LA EMPRESA:\n")
                self.analysis_text.insertPlainText("-" * 60 + "\n")
                for key, value in company_data.items():
                    self.analysis_text.insertPlainText(f"{key}: {value}\n")
                
                self.analysis_text.insertPlainText("\nDATOS DEL CLIENTE:\n")
                self.analysis_text.insertPlainText("-" * 60 + "\n")
                for key, value in client_data.items():
                    self.analysis_text.insertPlainText(f"{key}: {value}\n")
                
                self.analysis_text.insertPlainText("\nITEMS FACTURADOS:\n")
                self.analysis_text.insertPlainText("-" * 60 + "\n")
                for item in desglose:
                    self.analysis_text.insertPlainText(
                        f"{item['fruta']:12} → {item['cantidad']:6.2f} {item['unidad']:6} × "
                        f"${item['precio_unitario']:5} = ${item['subtotal']:7.2f}\n"
                    )
                
                self.analysis_text.insertPlainText("\nTOTALES:\n")
                self.analysis_text.insertPlainText("-" * 60 + "\n")
                self.analysis_text.insertPlainText(f"Subtotal:  ${result['totals']['subtotal']:,.2f}\n")
                self.analysis_text.insertPlainText(f"IVA (16%): ${result['totals']['iva']:,.2f}\n")
                self.analysis_text.insertPlainText(f"TOTAL:     ${result['totals']['total']:,.2f}\n")
                
                self.statusBar().showMessage('Factura generada')
                
            except Exception as e:
                import traceback
                error_msg = str(e)
                
                # Mensaje especial si falla WeasyPrint
                if 'weasyprint' in error_msg.lower() or 'no module named' in error_msg.lower():
                    QMessageBox.warning(
                        self,
                        'Dependencia faltante',
                        f'Para generar PDF, necesita instalar WeasyPrint:\n\n'
                        f'pip install weasyprint\n\n'
                        f'La factura HTML se generó correctamente en:\n{file_path}\n\n'
                        f'Puede abrirla en su navegador.'
                    )
                if 'pdfkit' in error_msg.lower() or 'no module named' in error_msg.lower():
                    QMessageBox.warning(
                        self,
                        'Dependencia faltante',
                        f'Para generar PDF, necesita instalar pdfkit:\n\n'
                        f'pip install pdfkit\n\n'
                        f'La factura HTML se generó correctamente en:\n{file_path}\n\n'
                        f'Puede abrirla en su navegador.'
                    )
                else:
                    QMessageBox.critical(
                        self,
                        'Error',
                        f'Error al generar factura:\n\n{error_msg}\n\n{traceback.format_exc()[:500]}'
                    )
        else:
            self.statusBar().showMessage('Creación cancelada')