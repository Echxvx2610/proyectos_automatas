from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import io
load_dotenv()

app = Flask(__name__)
CORS(app)

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("ERROR: GEMINI_API_KEY no encontrada en el archivo .env")
else:
    print(f"API Key cargada: {api_key[:10]}...")
    genai.configure(api_key=api_key)

@app.route('/api/models', methods=['GET'])
def list_models():
    """Endpoint para diagnosticar qué modelos están disponibles"""
    try:
        models = list(genai.list_models())
        available = []
        for m in models:
            available.append({
                'name': m.name,
                'display_name': getattr(m, 'display_name', 'N/A'),
                'supported_methods': getattr(m, 'supported_generation_methods', [])
            })
        return jsonify({
            'success': True,
            'count': len(available),
            'models': available
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        if not os.getenv('GEMINI_API_KEY'):
            return jsonify({
                'error': 'API key no configurada. Verifica tu archivo .env',
                'success': False
            }), 500
        
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        print(f"Recibiendo mensaje: {message[:50]}...")
        
        # Listar modelos disponibles y seleccionar el primero con generateContent
        models = list(genai.list_models())
        selected_model = None
        
        # Buscar modelos en orden de preferencia
        preferred_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        
        for pref in preferred_names:
            for m in models:
                if pref in m.name.lower() and 'generateContent' in getattr(m, 'supported_generation_methods', []):
                    selected_model = m.name
                    break
            if selected_model:
                break
        
        # Si no encuentra ninguno preferido, usa el primero disponible
        if not selected_model:
            for m in models:
                if 'generateContent' in getattr(m, 'supported_generation_methods', []):
                    selected_model = m.name
                    break
        
        if not selected_model:
            return jsonify({
                'error': 'No se encontró ningún modelo disponible que soporte generateContent',
                'success': False
            }), 500
        
        print(f"Usando modelo: {selected_model}")
        
        # Crear modelo y generar respuesta
        model = genai.GenerativeModel(selected_model)
        response = model.generate_content(message)
        
        print(f"Respuesta generada exitosamente")
        
        return jsonify({
            'response': response.text,
            'model_used': selected_model,
            'success': True
        })
    
    except Exception as e:
        print(f"Error en /api/chat: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    api_configured = bool(os.getenv('GEMINI_API_KEY'))
    return jsonify({
        'status': 'ok', 
        'message': 'Backend is running',
        'api_key_configured': api_configured
    })

if __name__ == '__main__':
    print("Iniciando servidor Flask en http://localhost:5000")
    print("\n=== Modelos disponibles ===")
    try:
        models = list(genai.list_models())
        for m in models:
            methods = getattr(m, 'supported_generation_methods', [])
            if 'generateContent' in methods:
                print(f"{m.name}")
    except Exception as e:
        print(f"Error listando modelos: {e}")
    print("===========================\n")
    app.run(debug=True, port=5000)
@app.route('/api/vision', methods=['POST'])
def vision():
     try:
         if 'image' not in request.files:
             return jsonify({'error': 'No se envió ninguna imagen'}), 400

         image_file = request.files['image']
        
         # Leer imagen en memoria
         image_bytes = image_file.read()
         image = Image.open(io.BytesIO(image_bytes))

         # Pregunta opcional
         question = request.form.get('question', 'Describe la imagen detalladamente.')

         # Seleccionar modelo con visión
         model_name = "gemini-1.5-flash"  # Puedes cambiar por uno de mayor capacidad
         model = genai.GenerativeModel(model_name)

         response = model.generate_content([question, image])

         return jsonify({
             'success': True,
             'response': response.text,
             'model_used': model_name
         })

     except Exception as e:
         print(f"Error en /api/vision: {e}")
         return jsonify({'success': False, 'error': str(e)}), 500