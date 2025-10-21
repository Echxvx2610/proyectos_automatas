# Proyecto: Editor de textos con Facturación (PySide6)

Aplicación GUI en Python con PySide6 que permite:
- Abrir, editar y guardar archivos `.txt`.
- Analizar texto (en construcción).
- Crear facturas capturando datos del cliente.

## Estructura del Proyecto

```
src/
├── main.py          # Punto de entrada de la aplicación
└── ui/
    ├── gui.py       # Clase principal de la interfaz (TextEditorGUI)
    └── dialogs.py   # Diálogos secundarios (ClientDataDialog)
```

## Requisitos
- Python 3.8+
- Dependencias en `requirements.txt`

## Instalación y Uso

1. Crear un entorno virtual (opcional pero recomendado):
   ```
   python -m venv venv
   venv\Scripts\activate  # En Windows
   ```

2. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

3. Ejecutar la aplicación:
   ```
   python src/main.py
   ```

## Funcionalidades

- **Archivo**: Abrir, guardar y salir.
- **Herramientas**:
  - Analizar: Lógica de análisis (en construcción).
  - Crear Factura: Abre un diálogo para capturar datos del cliente y generar factura (en construcción).

## Notas
- Los iconos están en `assets/icons/`.
- Estilo oscuro aplicado por defecto.
