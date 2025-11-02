# OpenChad

## Cómo instalar el proyecto

El proyecto se compone de dos partes:
- **Backend** (Python/Flask)
- **Frontend** (Node.js/React)

---

## Requisitos previos

- **Python 3.8 o superior**
- **Node.js 22 o superior**
- Una **API Key de Google Gemini** (instrucciones abajo)

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd proyecto03
```

La estructura del proyecto debería verse así:
```
proyecto03/
├── backend/
├── frontend/
└── (aquí crearemos la carpeta env)
```

---

## Configuración del Backend

### 2. Crear el entorno virtual

Desde la raíz del proyecto (`proyecto03/`), crea el entorno virtual:

```bash
# Opción 1: usando venv
py -m venv env

# Opción 2: usando virtualenv
virtualenv env
```

### 3. Activar el entorno virtual

**Windows:**
```bash
env\Scripts\activate.bat
```
> [!NOTE]
> Sabrás que el entorno está activado cuando veas `(env)` al inicio de tu línea de comandos, o puedes verificarlo en VS Code con `Ctrl + Shift + P` → `Python: Select Interpreter`.


Para desactivar el entorno virtual:
```bash
deactivate
```

### 4. Instalar dependencias del backend

Con el entorno virtual activado, navega a la carpeta backend e instala los requisitos:

```bash
cd backend
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

Crea un archivo `.env` **dentro de la carpeta `backend/`** (no confundir con la carpeta `env` del entorno virtual):

```bash
# backend/.env
GEMINI_API_KEY=tu_api_key_aquí
```

#### Cómo obtener una API Key de Gemini

1. Visita [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google
3. Haz clic en **"Get API Key"** o **"Create API Key"**
4. Selecciona un proyecto existente o crea uno nuevo
5. Copia la API Key generada
6. Pégala en tu archivo `.env`

> [!IMPORTANT]
> Nunca compartas tu API Key públicamente ni la subas a GitHub. Asegúrate de que el archivo `.env` esté incluido en tu `.gitignore`.

### 6. Lanzar el servidor backend

Con todo configurado, inicia el servidor:

```bash
py app.py
# o
python app.py
```

Deberías ver en consola algo similar a:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```
---
## Configuración del Frontend

### 7. Instalar Node.js

Asegúrate de tener instalado **Node.js versión 22 o superior**. Verifica tu versión:

```bash
node --version
```

Si necesitas instalar o actualizar Node.js, descárgalo desde [nodejs.org](https://nodejs.org/).

### 8. Instalar dependencias del frontend

Abre una **nueva terminal** (para mantener el backend corriendo), navega a la carpeta frontend e instala los paquetes:

```bash
cd frontend
npm install
```

### 9. Instalar Lucide React

```bash
npm install lucide-react
```

### 10. Lanzar la aplicación frontend

```bash
npm run dev
```

La interfaz se abrirá automáticamente en tu navegador, generalmente en:
```
http://localhost:5173
```

o

```
http://localhost:3000
```

---

## Verificación

Si todo está correctamente instalado, deberías tener:

- Servidor backend corriendo en `http://127.0.0.1:5000`
- Aplicación frontend corriendo en `http://localhost:5173` (o el puerto indicado)
- Ambos servicios comunicándose correctamente

---

## Comandos útiles

### Backend
```bash
# Activar entorno virtual
env\Scripts\activate.bat  # Windows
source env/bin/activate    # Linux/Mac

# Desactivar entorno virtual
deactivate

# Iniciar servidor
python app.py
```

### Frontend
```bash
# Instalar dependencias
npm install

# Iniciar aplicación
npm run dev
```

---

## Troubleshooting

> [!WARNING]
> **Problema:** "El comando `py` no se reconoce"  
> **Solución:** Usa `python` en lugar de `py`, o verifica que Python esté en tu PATH.  
>
> **Problema:** "Module not found" al ejecutar el backend  
> **Solución:** Asegúrate de que el entorno virtual esté activado y que hayas instalado todos los requisitos.  
>
> **Problema:** El frontend no se conecta con el backend  
> **Solución:** Verifica que ambos servidores estén corriendo y que las URLs de conexión sean correctas.

---

## Notas adicionales

- Mantén dos terminales abiertas: una para el backend y otra para el frontend
- No olvides activar el entorno virtual cada vez que trabajes en el backend
- Revisa la consola de ambos servicios para detectar posibles errores

---
