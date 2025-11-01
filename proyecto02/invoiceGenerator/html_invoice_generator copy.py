from datetime import datetime
import os
import base64
from pathlib import Path
# from invoiceGenerator.main import procesar_texto_compra # para usar desde gui
# from main import procesar_texto_compra # para probar individualmente

class HTMLInvoiceGenerator:
    def __init__(self, template_path="invoiceGenerator/factura.html"):
        self.template_path = template_path
        
    def encode_image_to_base64(self, image_path):
        """Convierte una imagen a base64 para embeber en HTML"""
        try:
            with open(image_path, 'rb') as image_file:
                encoded = base64.b64encode(image_file.read()).decode('utf-8')
                # Detectar el tipo de imagen
                ext = Path(image_path).suffix.lower()
                mime_types = {
                    '.png': 'image/png',
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.gif': 'image/gif',
                    '.svg': 'image/svg+xml'
                }
                mime_type = mime_types.get(ext, 'image/png')
                return f"data:{mime_type};base64,{encoded}"
        except Exception as e:
            print(f"⚠️ Error al cargar logo: {e}")
            return None
    
    def calculate_totals(self, items):
        """Calcula subtotal, IVA y total"""
        subtotal = sum(item['quantity'] * item['unit_price'] for item in items)
        descuento = 0
        iva = subtotal * 0.16
        total = subtotal - descuento + iva
        return {
            'subtotal': subtotal,
            'descuento': descuento,
            'iva': iva,
            'total': total
        }
    
    def format_currency(self, amount):
        """Formatea cantidad como moneda mexicana"""
        return f"${amount:,.2f}"
    
    def generate_items_html(self, items):
        """Genera las filas HTML para los items de la factura"""
        rows_html = ""
        for item in items:
            importe = item['quantity'] * item['unit_price']
            rows_html += f"""
            <tr>
                <td class="text-center">{item['quantity']:.2f}</td>
                <td class="text-center">{item['unit']}</td>
                <td>{item['description']}</td>
                <td class="text-right">{self.format_currency(item['unit_price'])}</td>
                <td class="text-right">{self.format_currency(importe)}</td>
            </tr>
            """
        return rows_html
    
    def generate_invoice_html(self, company_data, client_data, items, logo_path=None):
        """
        Genera el HTML completo de la factura
        
        Args:
            company_data: Datos de la empresa emisora
            client_data: Datos del cliente receptor
            items: Lista de items de la factura
            logo_path: Ruta al archivo del logo (opcional)
        """
        totals = self.calculate_totals(items)
        fecha_actual = datetime.now()
        folio_fiscal = fecha_actual.strftime("%Y%m%d%H%M%S")
        
        items_html = self.generate_items_html(items)
        
        logo_html = ""
        if logo_path is None:
            # Intentar cargar logo.png desde el mismo directorio del script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(script_dir, "logo.png")
        
        if logo_path and os.path.exists(logo_path):
            logo_base64 = self.encode_image_to_base64(logo_path)
            if logo_base64:
                logo_html = f'<img src="{logo_base64}" alt="Logo" class="company-logo">'
            else:
                print(f"No se pudo cargar el logo desde: {logo_path}")
        else:
            print(f"Logo no encontrado en: {logo_path}")
        
        html_content = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Factura {folio_fiscal}</title>
                <style>
                    * {{
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}
                    
                    body {{
                        font-family: Arial, sans-serif;
                        font-size: 10pt;
                        line-height: 1.4;
                        color: #333;
                        padding: 20px;
                        background: white;
                        -webkit-print-color-adjust: exact !important;
                        print-color-adjust: exact !important;
                        color-adjust: exact !important;
                    }}
                    
                    .invoice-container {{
                        max-width: 800px;
                        margin: 0 auto;
                        border: 2px solid #333;
                        padding: 15px;
                        background: white;
                    }}
                    
                    /* Header usando tabla para mejor compatibilidad PDF */
                    .header-table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 15px;
                        border-bottom: 2px solid #333;
                    }}
                    
                    .header-table td {{
                        vertical-align: top;
                        padding: 10px;
                    }}
                    
                    .company-logo-cell {{
                        width: 110px;
                        text-align: center;
                    }}
                    
                    .company-logo {{
                        width: 100px;
                        height: 100px;
                        object-fit: contain;
                        display: block;
                    }}
                    
                    .company-details-cell {{
                        padding-left: 15px;
                    }}
                    
                    .company-details h1 {{
                        font-size: 16pt;
                        color: #2c5f2d;
                        margin-bottom: 5px;
                    }}
                    
                    .company-details p {{
                        margin: 2px 0;
                        font-size: 9pt;
                    }}
                    
                    .invoice-info-cell {{
                        width: 220px;
                        background-color: #97c93d !important;
                        padding: 10px !important;
                        text-align: center;
                        -webkit-print-color-adjust: exact !important;
                        print-color-adjust: exact !important;
                    }}
                    
                    .invoice-info h2 {{
                        font-size: 14pt;
                        margin-bottom: 5px;
                        font-weight: bold;
                    }}
                    
                    .invoice-info p {{
                        margin: 3px 0;
                        font-size: 9pt;
                    }}
                    
                    /* Secciones de emisor/receptor usando tabla */
                    .parties-table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 15px;
                    }}
                    
                    .parties-table td {{
                        width: 50%;
                        border: 1px solid #333;
                        padding: 0;
                        vertical-align: top;
                    }}
                    
                    .party-header {{
                        background-color: #97c93d !important;
                        padding: 5px 10px;
                        font-size: 11pt;
                        font-weight: bold;
                        -webkit-print-color-adjust: exact !important;
                        print-color-adjust: exact !important;
                    }}
                    
                    .party-content {{
                        padding: 10px;
                    }}
                    
                    .party-content p {{
                        margin: 3px 0;
                        font-size: 9pt;
                    }}
                    
                    .party-content strong {{
                        display: inline-block;
                        width: 120px;
                    }}
                    
                    /* Tabla de items */
                    .items-table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 15px;
                    }}
                    
                    .items-table th {{
                        background-color: #97c93d !important;
                        padding: 8px;
                        text-align: left;
                        font-size: 10pt;
                        border: 1px solid #333;
                        font-weight: bold;
                        -webkit-print-color-adjust: exact !important;
                        print-color-adjust: exact !important;
                    }}
                    
                    .items-table td {{
                        padding: 6px 8px;
                        border: 1px solid #333;
                        font-size: 9pt;
                    }}
                    
                    .text-center {{
                        text-align: center;
                    }}
                    
                    .text-right {{
                        text-align: right;
                    }}
                    
                    /* Totales usando tabla */
                    .totals-container {{
                        width: 100%;
                        margin-bottom: 15px;
                    }}
                    
                    .totals-table {{
                        width: 320px;
                        float: right;
                        border-collapse: collapse;
                        border: 1px solid #333;
                    }}
                    
                    .totals-table td {{
                        padding: 5px 10px;
                        border-bottom: 1px solid #ddd;
                        font-size: 9pt;
                    }}
                    
                    .totals-table tr:last-child td {{
                        border-bottom: none;
                        background-color: #97c93d !important;
                        font-weight: bold;
                        font-size: 11pt;
                        -webkit-print-color-adjust: exact !important;
                        print-color-adjust: exact !important;
                    }}
                    
                    .totals-label {{
                        font-weight: bold;
                        width: 60%;
                    }}
                    
                    .totals-value {{
                        text-align: right;
                        width: 40%;
                    }}
                    
                    .clear {{
                        clear: both;
                    }}
                    
                    /* Footer */
                    .footer-section {{
                        border-top: 2px solid #333;
                        padding-top: 10px;
                        font-size: 8pt;
                        clear: both;
                    }}
                    
                    .footer-section h4 {{
                        font-size: 9pt;
                        margin-bottom: 5px;
                        margin-top: 8px;
                    }}
                    
                    .stamp-line {{
                        margin: 3px 0;
                        word-break: break-all;
                    }}
                    
                    /* Estilos específicos para impresión y PDF */
                    @media print {{
                        body {{
                            padding: 0;
                            margin: 0;
                            -webkit-print-color-adjust: exact !important;
                            print-color-adjust: exact !important;
                        }}
                        .invoice-container {{
                            border: 2px solid #333;
                            max-width: 100%;
                        }}
                        .invoice-info-cell,
                        .party-header,
                        .items-table th,
                        .totals-table tr:last-child td {{
                            background-color: #97c93d !important;
                            -webkit-print-color-adjust: exact !important;
                            print-color-adjust: exact !important;
                        }}
                    }}
                    
                    @page {{
                        size: Letter;
                        margin: 0.5cm;
                    }}
                </style>
            </head>
            <body>
                <div class="invoice-container">
                    <!-- Header usando tabla -->
                    <table class="header-table">
                        <tr>
                            <td class="company-logo-cell">
                                {logo_html}
                            </td>
                            <td class="company-details-cell">
                                <div class="company-details">
                                    <h1>{company_data.get('name', 'NOMBRE DE LA EMPRESA')}</h1>
                                    <p><strong>Razón Social:</strong> {company_data.get('fiscal_name', 'Razón social')}</p>
                                    <p><strong>Dirección:</strong> {company_data.get('address', 'Dirección')}</p>
                                    <p><strong>Teléfono:</strong> {company_data.get('phone', 'Teléfono')}</p>
                                    <p><strong>Página Web:</strong> {company_data.get('website', 'www.ejemplo.com')}</p>
                                </div>
                            </td>
                            <td class="invoice-info-cell">
                                <div class="invoice-info">
                                    <h2>FACTURA</h2>
                                    <p><strong>Folio Fiscal:</strong></p>
                                    <p>{folio_fiscal}</p>
                                    <p><strong>Fecha:</strong> {fecha_actual.strftime("%d/%m/%Y")}</p>
                                    <p><strong>Hora:</strong> {fecha_actual.strftime("%H:%M:%S")}</p>
                                </div>
                            </td>
                        </tr>
                    </table>
                    
                    <!-- Emisor y Receptor usando tabla -->
                    <table class="parties-table">
                        <tr>
                            <td>
                                <div class="party-header">Datos del Emisor</div>
                                <div class="party-content">
                                    <p><strong>Nombre Fiscal:</strong> {company_data.get('fiscal_name', 'Emisor')}</p>
                                    <p><strong>RFC:</strong> {company_data.get('rfc', 'RFC')}</p>
                                    <p><strong>Dirección:</strong> {company_data.get('address', 'Dirección')}</p>
                                </div>
                            </td>
                            <td>
                                <div class="party-header">Datos del Receptor</div>
                                <div class="party-content">
                                    <p><strong>Nombre Fiscal:</strong> {client_data.get('fiscal_name', 'Receptor')}</p>
                                    <p><strong>RFC:</strong> {client_data.get('rfc', 'RFC')}</p>
                                    <p><strong>Dirección:</strong> {client_data.get('address', 'Dirección')}</p>
                                </div>
                            </td>
                        </tr>
                    </table>
                    
                    <!-- Tabla de items -->
                    <table class="items-table">
                        <thead>
                            <tr>
                                <th class="text-center">Cantidad</th>
                                <th class="text-center">U. de medida</th>
                                <th>Descripción</th>
                                <th class="text-right">Precio unitario</th>
                                <th class="text-right">Importe</th>
                            </tr>
                        </thead>
                        <tbody>
                            {items_html}
                        </tbody>
                    </table>
                    
                    <!-- Totales -->
                    <div class="totals-container">
                        <table class="totals-table">
                            <tr>
                                <td class="totals-label">SUBTOTAL:</td>
                                <td class="totals-value">{self.format_currency(totals['subtotal'])}</td>
                            </tr>
                            <tr>
                                <td class="totals-label">DESCUENTO:</td>
                                <td class="totals-value">{self.format_currency(totals['descuento'])}</td>
                            </tr>
                            <tr>
                                <td class="totals-label">IVA 16%:</td>
                                <td class="totals-value">{self.format_currency(totals['iva'])}</td>
                            </tr>
                            <tr>
                                <td class="totals-label">TOTAL:</td>
                                <td class="totals-value">{self.format_currency(totals['total'])}</td>
                            </tr>
                        </table>
                        <div class="clear"></div>
                    </div>
                    
                    <!-- Footer -->
                    <div class="footer-section">
                        <h4>SELLO DIGITAL:</h4>
                        <p class="stamp-line">{'~' * 100}</p>
                        
                        <h4>SELLO DEL SAT:</h4>
                        <p class="stamp-line">{'~' * 100}</p>
                        
                        <h4>CADENA ORIGINAL DE CERTIFICACIÓN DEL SAT:</h4>
                        <p class="stamp-line">{'~' * 100}</p>
                        
                        <p style="margin-top: 10px; text-align: center;">
                            <strong>RÉGIMEN FISCAL:</strong> {company_data.get('tax_regime', 'Régimen General de Ley')}
                        </p>
                    </div>
                </div>
            </body>
            </html>
        """
        return html_content
    
    def save_html(self, html_content, output_path="factura.html"):
        """Guarda el HTML en un archivo"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML generado: {output_path}")
        return output_path
    
    def convert_to_pdf_weasyprint(self, html_path, pdf_path):
        """Convierte HTML a PDF usando WeasyPrint (recomendado para mejor fidelidad)"""
        try:
            from weasyprint import HTML, CSS
            
            print_css = CSS(string='''
                @page {{
                    size: Letter;
                    margin: 0.5cm;
                }}
                body {{
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                    color-adjust: exact !important;
                }}
                .invoice-info-cell,
                .party-header,
                .items-table th,
                .totals-table tr:last-child td {{
                    background-color: #97c93d !important;
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                }}
            ''')
            
            HTML(html_path).write_pdf(pdf_path, stylesheets=[print_css])
            print(f"PDF generado con WeasyPrint: {pdf_path}")
            return pdf_path
        except ImportError:
            print("WeasyPrint no está instalado. Instala con: pip install weasyprint")
            return None
        except Exception as e:
            print(f"Error al generar PDF: {e}")
            return None
    
    def convert_to_pdf_pdfkit(self, html_path, pdf_path):
        """Convierte HTML a PDF usando pdfkit con opciones mejoradas"""
        try:
            import pdfkit
            
            options = {
                'page-size': 'Letter',
                'margin-top': '0.5cm',
                'margin-right': '0.5cm',
                'margin-bottom': '0.5cm',
                'margin-left': '0.5cm',
                'encoding': 'UTF-8',
                'no-outline': None,
                'enable-local-file-access': None,
                'print-media-type': None,
                'disable-smart-shrinking': None,
                'dpi': 300,
                'image-quality': 100,
                'background': None,
                'zoom': 1.0,  # Sin zoom
                'enable-javascript': None,  # Habilitar JS si es necesario
                'javascript-delay': 1000,  # Esperar 1 segundo para renderizado
            }
            
            pdfkit.from_file(html_path, pdf_path, options=options)
            print(f"PDF generado con pdfkit: {pdf_path}")
            return pdf_path
        except ImportError:
            print("pdfkit no está instalado. Instala con: pip install pdfkit")
            print("También necesitas wkhtmltopdf: https://wkhtmltopdf.org/downloads.html")
            return None
        except Exception as e:
            print(f"Error al generar PDF: {e}")
            return None

    def generate_invoice(self, company_data, client_data, items, 
                        output_html="factura.html", 
                        generate_pdf=True,
                        pdf_method="weasyprint",
                        logo_path=None):
        """
        Genera la factura completa en HTML y opcionalmente en PDF
        
        Args:
            company_data: Datos de la empresa emisora
            client_data: Datos del cliente receptor
            items: Lista de items de la factura
            output_html: Ruta del archivo HTML de salida
            generate_pdf: Si se debe generar PDF
            pdf_method: 'weasyprint' o 'pdfkit'
            logo_path: Ruta al archivo del logo (opcional)
        """
        # Generar HTML con logo
        html_content = self.generate_invoice_html(company_data, client_data, items, logo_path)
        html_path = self.save_html(html_content, output_html)
        
        # Generar PDF si se solicita
        pdf_path = None
        if generate_pdf:
            pdf_path = output_html.replace('.html', '.pdf')
            if pdf_method == "weasyprint":
                pdf_path = self.convert_to_pdf_weasyprint(html_path, pdf_path)
            elif pdf_method == "pdfkit":
                pdf_path = self.convert_to_pdf_pdfkit(html_path, pdf_path)
        
        totals = self.calculate_totals(items)
        
        return {
            'html': html_path,
            'pdf': pdf_path,
            'totals': totals
        }


# # Ejemplo de uso mejorado
# if __name__ == "__main__":
#     # Datos de ejemplo
#     company_data = {
#         'name': 'FRUTAS MÁGICAS S.A. DE C.V.',
#         'fiscal_name': 'Frutas Mágicas Sociedad Anónima de Capital Variable',
#         'rfc': 'FMA123456ABC',
#         'address': 'Av. Principal #123, Col. Centro, Ciudad, CP 12345',
#         'phone': '555-1234-5678',
#         'website': 'www.frutasmagicas.com',
#         'tax_regime': 'Régimen General de Ley'
#     }
    
#     client_data = {
#         'fiscal_name': 'Juan Pérez García',
#         'rfc': 'PEGJ850101XYZ',
#         'address': 'Calle Secundaria #456, Col. Norte, Ciudad, CP 54321'
#     }
    
#     # Items de ejemplo
#     items = [
#         {
#             'quantity': 2.0,
#             'unit': 'kg',
#             'description': 'Naranjas frescas',
#             'unit_price': 25.00
#         },
#         {
#             'quantity': 3.0,
#             'unit': 'pza',
#             'description': 'Mango manila',
#             'unit_price': 15.00
#         },
#         {
#             'quantity': 1.5,
#             'unit': 'kg',
#             'description': 'Uvas rojas sin semilla',
#             'unit_price': 80.00
#         },
#         {
#             'quantity': 5.0,
#             'unit': 'pza',
#             'description': 'Limón persa',
#             'unit_price': 3.50
#         }
#     ]
    
#     # Generar factura con logo
#     generator = HTMLInvoiceGenerator()
    
#     print("Generando factura con logo...")
#     print("="*70)
    
#     result = generator.generate_invoice(
#         company_data=company_data,
#         client_data=client_data,
#         items=items,
#         output_html="factura_con_logo.html",
#         generate_pdf=True,
#         pdf_method="weasyprint",  # Cambia a "pdfkit" si prefieres
#         logo_path="logo.png"  # Coloca tu logo aquí
#     )
    
#     if result:
#         print("\n" + "="*70)
#         print("FACTURA GENERADA EXITOSAMENTE")
#         print("="*70)
#         print(f"HTML: {result['html']}")
#         print(f"PDF: {result['pdf']}")
#         print(f"\nSubtotal: {generator.format_currency(result['totals']['subtotal'])}")
#         print(f"IVA (16%): {generator.format_currency(result['totals']['iva'])}")
#         print(f"Total: {generator.format_currency(result['totals']['total'])}")
