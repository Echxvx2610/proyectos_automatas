import re
from collections import defaultdict

def search_fruits(content, fruit_list):
    fruit_counts = {fruit: 0 for fruit in fruit_list}
    fruits_per_month = defaultdict(list)
    
    try:
        # asumimos que content ya es una cadena de texto ( agregar validacion o manejo de errores )
        # lectura de archivo para pruebas ( deshabilitado para gui, usar content directo )
        # with open(file_path, 'r', encoding='utf-8') as file:
        #     content = file.read()
            
        # Contar las veces aparece cada fruta (case-insensitive)
        content_lower = content.lower()
        for fruit in fruit_list:
            pattern = get_fruit_pattern(fruit)
            matches = re.findall(pattern, content_lower)
            fruit_counts[fruit] = len(matches)
        
        # Dividir por meses - buscar titulos de secciones ( tendencia  Mes: )
        month_pattern = r'(Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Octubre|Noviembre|Diciembre):\s*(.+?)(?=(?:Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Octubre|Noviembre|Diciembre):|Y así,|$)'
        
        month_sections = re.finditer(month_pattern, content, re.DOTALL)
        
        for match in month_sections:
            month = match.group(1)
            month_text = match.group(2).lower()
            
            for fruit in fruit_list:
                pattern = get_fruit_pattern(fruit)
                if re.search(pattern, month_text):
                    fruits_per_month[month].append(fruit)

    except FileNotFoundError:
        print(f"El archivo {file_path} no fue encontrado.")
        return None, None
    
    return fruit_counts, fruits_per_month

def get_fruit_pattern(fruit):
    fruit_lower = fruit.lower()
    
    # Casos especiales para plurales irregulares
    if fruit_lower.endswith('ón'):
        # limón -> limón/limones, melón -> melón/melones
        base = fruit_lower[:-2]
        return rf'\b{base}(ón|ones)\b'
    elif fruit_lower.endswith('z'):
        return rf'\b{fruit_lower}(|es)\b'
    else:
        # Plurales regulares: fresa -> fresas
        return rf'\b{fruit_lower}(|s)\b'

# def main():
#     fruits = [
#         'naranja', 'mandarina', 'toronja', 
#         'fresa', 'guayaba', 'limón',
#         'piña', 'mango', 'papaya', 
#         'melón', 'sandía', 'ciruela', 
#         'durazno', 'higo', 'pera', 
#         'tuna', 'manzana', 'uva', 
#         'granada'
#     ]
    
#     file_path = r'fruitLoops\frutas_magicas.txt'
#     fruit_counts, fruits_per_month = search_fruits(file_path, fruits)
    
#     if fruit_counts is None:
#         return
    
#     # Cantidad de frutas sin repetir
#     frutas_encontradas = [f for f, c in fruit_counts.items() if c > 0]
#     print(f"Frutas encontradas sin repetir: {len(frutas_encontradas)}")
#     print(f"   {', '.join(sorted(frutas_encontradas))}\n")
    
#     # Frutas por mes
#     print("Frutas por mes:")
#     print("-" * 60)
    
#     meses_orden = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
#                    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    
#     for mes in meses_orden:
#         if mes in fruits_per_month:
#             lista = fruits_per_month[mes]
#             print(f"{mes:12} → {len(lista)} frutas: {', '.join(lista)}")
#         else:
#             print(f"{mes:12} → 0 frutas")
    
#     # Veces que aparece cada fruta
#     print("\nFrecuencia de aparicion:")
#     print("-" * 60)
#     for fruit, count in sorted(fruit_counts.items(), key=lambda x: -x[1]):
#         if count > 0:
#             print(f"{fruit.capitalize():12} → {count} vez{'es' if count != 1 else ''}")

# if __name__ == "__main__":
#     main()