"""
Módulo para diálogos de la aplicación.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit,
    QComboBox, QPushButton
)

class ClientDataDialog(QDialog):
    """
    Diálogo para capturar datos del cliente para la factura.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Datos del Cliente')
        self.setModal(True)
        self.resize(400, 500)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Campos de texto
        self.fiscal_name = QLineEdit()
        form_layout.addRow('Nombre Fiscal:', self.fiscal_name)

        self.rfc = QLineEdit()
        form_layout.addRow('RFC:', self.rfc)

        self.address = QTextEdit()
        self.address.setMaximumHeight(60)
        form_layout.addRow('Dirección:', self.address)

        self.email = QLineEdit()
        form_layout.addRow('Email:', self.email)

        self.phone = QLineEdit()
        form_layout.addRow('Teléfono:', self.phone)

        # Comboboxes
        self.payment_method = QComboBox()
        self.payment_method.addItems(['Efectivo', 'Transferencia bancaria', 'Tarjeta de crédito', 'Tarjeta de débito', 'Cheque'])
        form_layout.addRow('Método de Pago:', self.payment_method)

        self.payment_type = QComboBox()
        self.payment_type.addItems(['Contado', 'Crédito'])
        form_layout.addRow('Tipo de Pago:', self.payment_type)

        self.tax_regime = QComboBox()
        self.tax_regime.addItems([
            'Régimen General de Ley Personas Morales',
            'Régimen de Incorporación Fiscal',
            'Régimen de Actividades Empresariales y Profesionales',
            'Régimen de Arrendamiento',
            'Otro'
        ])
        form_layout.addRow('Régimen Fiscal:', self.tax_regime)

        layout.addLayout(form_layout)

        # Botones
        buttons_layout = QVBoxLayout()
        self.ok_button = QPushButton('Aceptar')
        self.ok_button.setStyleSheet("background-color: lightgreen; color: black;")
        self.ok_button.clicked.connect(self.accept)
        buttons_layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton('Cancelar')
        self.cancel_button.setStyleSheet("background-color: lightcoral; color: black;")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def get_client_data(self):
        """
        Retorna un diccionario con los datos del cliente.
        """
        return {
            'fiscal_name': self.fiscal_name.text(),
            'rfc': self.rfc.text(),
            'address': self.address.toPlainText(),
            'email': self.email.text(),
            'phone': self.phone.text(),
            'payment_method': self.payment_method.currentText(),
            'payment_type': self.payment_type.currentText(),
            'tax_regime': self.tax_regime.currentText()
        }