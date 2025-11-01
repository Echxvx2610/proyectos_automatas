import re
from fractions import Fraction

# Tabla de costos de frutas (precios por kg y por pieza)
costos_frutas = {
    "Naranja": {"precio_kg": 15, "precio_pieza": 2, "nota": "Precios por kg y pieza"},
    "Mandarina": {"precio_kg": 20, "precio_pieza": 1.5, "nota": "Precios por kg y pieza"},
    "Toronja": {"precio_kg": 25, "precio_pieza": 3, "nota": "Precios por kg y pieza"},
    "Fresa": {"precio_kg": 60, "precio_pieza": None, "nota": "Solo por kg"},
    "Guayaba": {"precio_kg": 35, "precio_pieza": 2.5, "nota": "Precios por kg y pieza"},
    "Limón": {"precio_kg": 20, "precio_pieza": 1, "nota": "Precios por kg y pieza"},
    "Piña": {"precio_kg": 30, "precio_pieza": 10, "nota": "Precios por kg y pieza"},
    "Mango": {"precio_kg": 35, "precio_pieza": 5, "nota": "Precios por kg y pieza"},
    "Papaya": {"precio_kg": 20, "precio_pieza": 6, "nota": "Precios por kg y pieza"},
    "Melón": {"precio_kg": 30, "precio_pieza": 8, "nota": "Precios por kg y pieza"},
    "Melon": {"precio_kg": 30, "precio_pieza": 8, "nota": "Precios por kg y pieza"},
    "Sandía": {"precio_kg": 15, "precio_pieza": 12, "nota": "Precios por kg y pieza"},
    "Ciruela": {"precio_kg": 45, "precio_pieza": None, "nota": "Solo por kg"},
    "Durazno": {"precio_kg": 50, "precio_pieza": 4, "nota": "Precios por kg y pieza"},
    "Higo": {"precio_kg": 70, "precio_pieza": None, "nota": "Solo por kg"},
    "Pera": {"precio_kg": 40, "precio_pieza": 3, "nota": "Precios por kg y pieza"},
    "Tuna": {"precio_kg": 20, "precio_pieza": 2, "nota": "Precios por kg y pieza"},
    "Manzana": {"precio_kg": 35, "precio_pieza": 3, "nota": "Precios por kg y pieza"},
    "Uva": {"precio_kg": 60, "precio_pieza": None, "nota": "Solo por kg"},
    "Granada": {"precio_kg": 80, "precio_pieza": 5, "nota": "Precios por kg y pieza"}
}

def get_fruit_pattern(fruit):
    """Genera un patron regex para detectar variaciones de la fruta"""
    fruit_lower = fruit.lower()
    if fruit_lower.endswith('ón'):
        base = fruit_lower[:-2]
        return rf'{base}(?:ón|ones)'
    elif fruit_lower.endswith('z'):
        return rf'{fruit_lower}(?:es)?'
    elif fruit_lower.endswith('as'):
        return rf'{fruit_lower}(?:as)?'
    else:
        return rf'{fruit_lower}s?'

# def extraer_compras(texto):
#     """
#     Extrae las frutas, cantidades y unidades del texto de compra
#     Retorna una lista de tuplas (fruta, cantidad, unidad)
#     """
#     compras = []
#     texto_lower = texto.lower()

#     for fruta_original, info in costos_frutas.items():
#         fruta_pattern = get_fruit_pattern(fruta_original)

#         # patron para detectar kg
#         kg_pattern = rf'(\d+(?:/\d+)?|\d+\.?\d*)\s*(?:kg|kilogramos?)\s*(?:de\s+)?{fruta_pattern}'
#         # patron para detectar piezas
#         pieza_pattern = rf'(\d+(?:/\d+)?|\d+\.?\d*)\s*(?:piezas?|pieza)?\s*(?:de\s+)?{fruta_pattern}'

#         # Buscar coincidencias para kg
#         kg_matches = re.findall(kg_pattern, texto_lower)
#         if kg_matches:
#             try:
#                 cantidad = float(Fraction(kg_matches[0])) if '/' in kg_matches[0] else float(kg_matches[0])
#                 if info["precio_kg"] is not None:  # Verificar si la fruta se vende por kg
#                     compras.append((fruta_original, cantidad, "kg"))
#             except ValueError:
#                 continue

#         # Buscar coincidencias para piezas
#         pieza_matches = re.findall(pieza_pattern, texto_lower)
#         if pieza_matches:
#             try:
#                 cantidad = float(Fraction(pieza_matches[0])) if '/' in pieza_matches[0] else float(pieza_matches[0])
#                 if info["precio_pieza"] is not None:  # Verificar si la fruta se vende por pieza
#                     compras.append((fruta_original, cantidad, "pieza"))
#             except ValueError:
#                 continue

#     return compras

def extraer_compras(texto):
    """
    Extrae las frutas, cantidades y unidades del texto de compra
    Retorna una lista de tuplas (fruta, cantidad, unidad)
    """
    compras = []
    texto_lower = texto.lower()

    for fruta_original, info in costos_frutas.items():
        fruta_pattern = get_fruit_pattern(fruta_original)

        # Patrón para detectar kg
        kg_pattern = rf'(\d+(?:/\d+)?|\d+\.?\d*)\s*(?:kg|kilogramos?)\s*(?:de\s+)?{fruta_pattern}'
        
        # Patrón para detectar piezas (con o sin la palabra "pieza")
        pieza_pattern = rf'(\d+(?:/\d+)?|\d+\.?\d*)\s*(?:piezas?|pieza)?\s*(?:de\s+)?{fruta_pattern}'

        # Buscar coincidencias para kg
        kg_matches = re.findall(kg_pattern, texto_lower)
        if kg_matches:
            try:
                cantidad = float(Fraction(kg_matches[0])) if '/' in kg_matches[0] else float(kg_matches[0])
                if info["precio_kg"] is not None:
                    compras.append((fruta_original, cantidad, "kg"))
                    continue  # Evitar duplicados
            except ValueError:
                pass

        # Buscar coincidencias para piezas
        pieza_matches = re.findall(pieza_pattern, texto_lower)
        if pieza_matches and info["precio_pieza"] is not None:
            try:
                cantidad = float(Fraction(pieza_matches[0])) if '/' in pieza_matches[0] else float(pieza_matches[0])
                compras.append((fruta_original, cantidad, "pieza"))
            except ValueError:
                pass

    return compras



def calcular_total(compras):
    """Calcula el total de la compra"""
    total = 0
    desglose = []

    for fruta, cantidad, unidad in compras:
        if fruta in costos_frutas:
            precio = costos_frutas[fruta][f"precio_{unidad}"]
            if precio is None:
                continue  # Saltar si no hay precio para la unidad
            subtotal = precio * cantidad
            total += subtotal

            desglose.append({
                "fruta": fruta,
                "cantidad": cantidad,
                "unidad": unidad,
                "precio_unitario": precio,
                "subtotal": subtotal
            })

    return total, desglose

def procesar_texto_compra(texto):
    """Función principal que procesa el texto de compra , quitar comentarios de print para probar en consola"""
    #print(f"Texto de compra: \"{texto}\"\n")
    #print("=" * 70)

    # Extraer compras del texto
    compras = extraer_compras(texto)

    if not compras:
        print("No se detectaron frutas en el texto.")
        return None

    # Calcular total
    total, desglose = calcular_total(compras)
    # print(type(total))
    # print(type(desglose))
    return total, desglose
    # # Mostrar desglose
    # print("\nDESGLOSE DE COMPRA:")
    # print("-" * 70)
    # for item in desglose:
    #     print(f"{item['fruta']:12} → {item['cantidad']:6.2f} {item['unidad']:6} × ${item['precio_unitario']:5} = ${item['subtotal']:7.2f}")

    # print("-" * 70)
    # print(f"{'TOTAL':12}                                    ${total:7.2f}")
    # print("=" * 70)

# if __name__ == "__main__":
#     # Ejemplo 1
#     #texto = input("Ingrese el texto de compra: ")
#     texto = "Compré 2 kg de naranjas, 3 piezas de mango y 1.5 kg de uvas."
#     print(type(procesar_texto_compra(texto)))
#     print(procesar_texto_compra(texto)) # [0] es el total, [1] es el desglose
