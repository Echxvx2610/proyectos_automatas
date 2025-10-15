from CSVVisitor import CSVVisitor
from CSVParser import CSVParser


class FileCSVVisitorImpl(CSVVisitor):
    """
    Implementacion del visitor para procesar archivos CSV
    """
    def __init__(self):
        self.data = {
            'header': None,
            'rows': [],
            'total_fields': 0
        }
    
    def visitCsvFile(self, ctx: CSVParser.CsvFileContext):
        """
        Visita el archivo CSV completo
        """
        all_rows = []
        
        # Procesar todas las filas
        for i, row_ctx in enumerate(ctx.row()):
            row_data = self.visit(row_ctx)
            all_rows.append(row_data)
            
            # La primera fila se considera encabezado
            if i == 0:
                self.data['header'] = row_data
            else:
                self.data['rows'].append(row_data)
        
        # Contar el total de campos
        self.data['total_fields'] = sum(len(row) for row in all_rows)
        
        return self.data
    
    def visitRow(self, ctx: CSVParser.RowContext):
        """
        Visita una fila (sin importar si tiene newline o no)
        """
        fields = []
        field_contexts = ctx.field()
        
        for field_index, field_ctx in enumerate(field_contexts):
            # Obtener el valor del campo usando el visitor apropiado
            field_value = self.visit(field_ctx)
            
            # Validacion opcional para calificaciones (columnas numéricas)
            if field_value and len(field_value) > 0:
                # Si estamos en una columna que podria ser calificacion (a partir de la columna 2)
                if field_index >= 2:  # Las columnas de numeros empiezan en indice 2
                    try:
                        grade = float(field_value)
                        if not (0 <= grade <= 10):
                            print(f"Advertencia: Calificación inválida '{field_value}' en columna {field_index + 1}")
                    except ValueError:
                        # No es un numero, no hay problema (puede ser texto)
                        pass
            
            fields.append(field_value)
        
        return fields
    
    def visitField(self, ctx: CSVParser.FieldContext):
        """
        Visita un campo generico - este metodo delega a los metodos especificos
        """
        # Este metodo se llama automaticamente y delega a los metodos especificos
        return self.visitChildren(ctx)
    
    def visitTextField(self, ctx: CSVParser.TextFieldContext):
        """
        Visita un campo de texto simple
        """
        return ctx.TEXT().getText().strip()
    
    def visitQuotedField(self, ctx: CSVParser.QuotedFieldContext):
        """
        Visita un campo entre comillas
        """
        text = ctx.STRING().getText()
        # Remover las comillas externas
        text = text[1:-1]
        # Convertir "" a " (comillas escapadas)
        text = text.replace('""', '"')
        return text
    
    def visitEmptyField(self, ctx: CSVParser.EmptyFieldContext):
        """
        Visita un campo vacío
        """
        return ""