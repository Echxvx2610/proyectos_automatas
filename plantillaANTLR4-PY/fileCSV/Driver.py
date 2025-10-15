import sys
from antlr4 import *
from CSVLexer import CSVLexer
from CSVParser import CSVParser
from FileCSVVisitorImpl import FileCSVVisitorImpl

# funcion auxiliar para analisar las calificaciones
def analisis_calif(result):
    print("\n...:: ANALISIS DE CALIFICACIONES ::...")
    
    if not result or not result['header']:
        print("No se puede realizar analisis: falta encabezado")
        return None
    
    header = result['header']
    
    try:
        pa_indices = [i for i, h in enumerate(header) if h.upper() == 'PA']
        q1_index = next((i for i, h in enumerate(header) if h.upper() == 'Q1'), None)
        q2_index = next((i for i, h in enumerate(header) if h.upper() == 'Q2'), None)
        lab_index = next((i for i, h in enumerate(header) if h.upper() == 'LAB'), None)
        exa_index = next((i for i, h in enumerate(header) if h.upper() == 'EXA'), None)
        cal_index = next((i for i, h in enumerate(header) if h.upper() == 'CAL'), None)
        red_index = next((i for i, h in enumerate(header) if h.upper() == 'RED'), None)
        
        if not pa_indices or q1_index is None or q2_index is None or lab_index is None or exa_index is None:
            print("Advertencia: No se encontraron todas las columnas necesarias para el analisis")
            return None
        
        print(f"Columnas PA encontradas en indices: {pa_indices}")
        print(f"Q1: {q1_index}, Q2: {q2_index}, LAB: {lab_index}, EXA: {exa_index}")
        
        processed_rows = []
        
        for row in result['rows']:
            new_row = row.copy()
            
            pa_values = []
            for idx in pa_indices:
                if idx < len(row) and row[idx]:
                    try:
                        pa_values.append(float(row[idx]))
                    except ValueError:
                        pass
            

            # calculos de promedios y calificaciones
            promedio_pa = sum(pa_values) / len(pa_values) if pa_values else 0
            
            q1 = float(row[q1_index]) if q1_index < len(row) and row[q1_index] else 0
            q2 = float(row[q2_index]) if q2_index < len(row) and row[q2_index] else 0
            promedio_q = (q1 + q2) / 2
            
            lab = float(row[lab_index]) if lab_index < len(row) and row[lab_index] else 0
            exa = float(row[exa_index]) if exa_index < len(row) and row[exa_index] else 0
            
            cal = (promedio_pa * 0.10) + (promedio_q * 0.20) + (lab * 0.40) + (exa * 0.30)
            
            # reglas de redondeo
            if cal < 7:
                red = 0.0
            else:
                fractional_part = cal - int(cal)
                if fractional_part >= 0.5:
                    red = float(int(cal) + 1)
                else:
                    red = float(int(cal))
            
            if cal_index is not None and cal_index < len(new_row):
                new_row[cal_index] = f"{cal:.2f}"
            elif cal_index is not None:
                while len(new_row) <= cal_index:
                    new_row.append("")
                new_row[cal_index] = f"{cal:.2f}"
            
            if red_index is not None and red_index < len(new_row):
                new_row[red_index] = f"{red:.1f}"
            elif red_index is not None:
                while len(new_row) <= red_index:
                    new_row.append("")
                new_row[red_index] = f"{red:.1f}"
            
            processed_rows.append(new_row)
        
        print("\n--- RESULTADOS CON CALIFICACIONES CALCULADAS ---")
        print(f"Encabezado: {header}")
        for i, row in enumerate(processed_rows, 1):
            print(f"Fila {i}: {row}")
        
        return {
            'header': header,
            'rows': processed_rows
        }
        
    except Exception as e:
        print(f"Error en analisis de calificaciones: {str(e)}")
        return None

def save_csv_option(result):
    print("\n...:: GUARDAR ARCHIVO CSV ::...")
    print("¿Desea guardar el resultado en un archivo CSV? (s/n): ", end="")
    
    try:
        response = input().strip().lower()
        if response == 's':
            print("Nombre del archivo (sin extension): ", end="")
            filename = input().strip()
            if not filename:
                filename = "resultado" # nombre default
            
            filepath = f"{filename}.csv"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(','.join(result['header']) + '\n')
                for row in result['rows']:
                    f.write(','.join(str(field) for field in row) + '\n')
            
            print(f"Archivo guardado exitosamente: {filepath}")
        else:
            print("Archivo no guardado")
    except Exception as e:
        print(f"Error al guardar archivo: {str(e)}")

def validate_csv_structure(input_text):
    lines = input_text.split('\n')
    non_empty_lines = [line for line in lines if line.strip() or ',' in line]
    
    if not non_empty_lines:
        return False, "Archivo vacio"
    
    return True, "Estructura valida de CSV"

def analyze_csv(input_text):
    print(f"\n... ANALIZANDO CSV ...\n")
    
    is_valid, message = validate_csv_structure(input_text)
    if not is_valid:
        print(f"..:: FORMATO INVALIDO ::.. \n")
        print(f"Razon: {message}")
        return None
    
    try:
        # configurar el antlr4
        input_stream = InputStream(input_text)
        lexer = CSVLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = CSVParser(token_stream)
        parser.removeErrorListeners()
        tree = parser.csvFile()
        
        # Visita el arbol para extraer datos ( visitor personalizado )
        visitor = FileCSVVisitorImpl()
        # resultados del analisis
        result = visitor.visit(tree)
        #print(result)
        #print("..:: CSV VALIDO ::.. \n")
        
        total_rows = len(result['rows']) + (1 if result['header'] else 0)
        num_columns = len(result['header']) if result['header'] else 0
        total_fields = result['total_fields']
        empty_fields = sum(1 for row in result['rows'] for field in row if field == "")
        if result['header']:
            empty_fields += sum(1 for field in result['header'] if field == "")
        
        print(f"Total de filas: {total_rows}") # segun filas contadas
        print(f"Total de columnas: {num_columns}") # segun encabezado
        print(f"Total de campos: {total_fields}")
        #print(f"Campos vacios detectados: {empty_fields}")
        
        if result['header']:
            print(f"\nEncabezados: {result['header']}")
        
        print("\n--- DATOS ---")
        if result['header']:
            print(f"Fila 1 (encabezado): {result['header']}")
        for i, row in enumerate(result['rows'], 2 if result['header'] else 1):
            print(f"Fila {i}: {row}")
        
        #usamos la funcion auxiliar para las calificaciones
        calif_result = analisis_calif(result)
        if calif_result:
            save_csv_option(calif_result)

        return result
        
    except Exception as error:
        print(f"..:: ERROR DE PARSEO ::.. ")
        print(f"Error: {str(error)}")
        return None

def main(argv):
    if len(argv) > 1:
        try:
            with open(argv[1], 'r', encoding='utf-8') as file:
                content = file.read()
            
            print(f"... PROCESANDO ARCHIVO: {argv[1]} ...")
            analyze_csv(content)
            print("\n... FIN DEL ANALISIS ...")
            
        except FileNotFoundError:
            print(f"Error: no se encontro el archivo '{argv[1]}'")
        except Exception as e:
            print(f"Error al procesar archivo: {str(e)}")
    
    else:
        print("... ANALIZADOR CSV ANTLR4 (Python) ...\n")

        print("\n--- EJEMPLO 1: CSV de calificaciones ---")
        csv1 = """,,PA,Q1,Q2,PA,PA,LAB,EXA,PA,CAL,RED
        1,ANAYA CERVANTES DAVID FELIPE,0,2,0,0,10,0,7.0,0,,
        2,APARICIO VIVAR SAUL ELISEO,10,3,5.3,10,10,10,7.24,10,,
        3,ARIAS FLORES RAFAEL,10,6,4.6,10,10,10,6.75,10,,
        4,ARIAS HERNÁNDEZ MARIO DE JESÚS,0,0,4,10,10,10,7.0,10,,
        5,ARMENTA FUENTES LOBSANG LEONARDO,10,3,3,10,10,10,7.0,10,,"""
        analyze_csv(csv1)

        print("\n\n--- EJEMPLO 2: CSV Simple ---")
        csv2 = """nombre,edad,estado
        Cristian Echevarria,24,Nayarit
        Oscar Teran,28,"""
        analyze_csv(csv2)

        print("\n\n--- ERROR: Archivo vacio ---")
        empty_file = ""
        analyze_csv(empty_file)

        print("\n\n--- ERROR: Solo espacios en blanco ---")
        whitespace_only = """   
        
        """
        analyze_csv(whitespace_only)

        print("\n\n--- ERROR: Comillas mal escapadas ---")
        bad_escape = """nombre,comentario
        Cristian,"Dijo: "hola" y se fue"
        Oscar,Normal"""
        analyze_csv(bad_escape)

        print("\n\n--- ERROR: HTML (no es CSV) ---")
        html_invalid = """<!DOCTYPE html>
        <html>
        <head><title>Test</title></head>
        <body>
        <table>
        <tr><td>Cristian</td><td>24</td></tr>
        </table>
        </body>
        </html>"""
        analyze_csv(html_invalid)

        print("\n\n--- ERROR: Caracteres especiales sin comillas ---")
        special_chars = """nombre,edad
        Cristian@#$%,24
        Oscar,27"""
        analyze_csv(special_chars)

        print("\n\n--- ERROR: Estructura de Python (no es CSV) ---")
        python_dict = """data = {
            'nombre': 'Cristian',
            'edad': 24,
            'estado': 'Nayarit'
        }"""
        analyze_csv(python_dict)

        print("\n... FIN DE PRUEBAS ...")

if __name__ == '__main__':
    main(sys.argv)