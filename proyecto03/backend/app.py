from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import io
from PyPDF2 import PdfReader
import json
import time
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

# @app.route('/api/chat', methods=['POST'])
# def chat():
#     try:
#         if not os.getenv('GEMINI_API_KEY'):
#             return jsonify({
#                 'error': 'API key no configurada. Verifica tu archivo .env',
#                 'success': False
#             }), 500
        
#         data = request.json
#         message = data.get('message', '')
        
#         if not message:
#             return jsonify({'error': 'No message provided'}), 400
        
#         print(f"Recibiendo mensaje: {message[:50]}...")
        
#         # Listar modelos disponibles y seleccionar el primero con generateContent
#         models = list(genai.list_models())
#         selected_model = None
        
#         # Buscar modelos en orden de preferencia
#         preferred_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        
#         for pref in preferred_names:
#             for m in models:
#                 if pref in m.name.lower() and 'generateContent' in getattr(m, 'supported_generation_methods', []):
#                     selected_model = m.name
#                     break
#             if selected_model:
#                 break
        
#         # Si no encuentra ninguno preferido, usa el primero disponible
#         if not selected_model:
#             for m in models:
#                 if 'generateContent' in getattr(m, 'supported_generation_methods', []):
#                     selected_model = m.name
#                     break
        
#         if not selected_model:
#             return jsonify({
#                 'error': 'No se encontró ningún modelo disponible que soporte generateContent',
#                 'success': False
#             }), 500
        
#         print(f"Usando modelo: {selected_model}")
        
#         # Crear modelo y generar respuesta
#         model = genai.GenerativeModel(selected_model)
#         response = model.generate_content(message)
        
#         print(f"Respuesta generada exitosamente")
        
#         return jsonify({
#             'response': response.text,
#             'model_used': selected_model,
#             'success': True
#         })
    
#     except Exception as e:
#         print(f"Error en /api/chat: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({
#             'error': str(e),
#             'success': False
#         }), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        if not os.getenv('GEMINI_API_KEY'):
            return jsonify({
                'error': 'API key no configurada. Verifica tu archivo .env',
                'success': False
            }), 500
        
        # Manejar tanto JSON como form-data
        if request.content_type and 'multipart/form-data' in request.content_type:
            message = request.form.get('message', '')
            images = request.files.getlist('images')  # Múltiples imágenes
            pdf_file = request.files.get('pdf')  # Un solo PDF
        else:
            data = request.json
            message = data.get('message', '')
            images = []
            pdf_file = None
        
        # Validación: Si hay PDF sin mensaje
        if pdf_file and not message:
            return jsonify({
                'error': 'Por favor, incluye una pregunta sobre el PDF que subiste.',
                'success': False
            }), 400
        
        # Validación: Si hay mensaje que parece requerir PDF pero no hay PDF
        pdf_keywords = ['pdf', 'documento', 'archivo', 'documento adjunto']
        if message and any(keyword in message.lower() for keyword in pdf_keywords) and not pdf_file:
            return jsonify({
                'error': 'Por favor, adjunta el PDF para poder responder tu pregunta.',
                'success': False
            }), 400
        
        if not message and not images and not pdf_file:
            return jsonify({'error': 'No message, images, or PDF provided'}), 400
        
        print(f"Recibiendo mensaje: {message[:50] if message else '(solo archivos)'}...")
        if images:
            print(f"Con {len(images)} imagen(es)")
        if pdf_file:
            print(f"Con PDF: {pdf_file.filename}")
        
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
        
        # Crear modelo
        model = genai.GenerativeModel(selected_model)
        
        # Preparar contenido
        content = []
        
        # Procesar PDF si existe
        if pdf_file:
            try:
                pdf_bytes = pdf_file.read()
                pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
                
                # Extraer texto de todas las páginas
                pdf_text = ""
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    page_text = page.extract_text()
                    pdf_text += f"\n--- Página {page_num} ---\n{page_text}"
                
                # Crear prompt con el texto del PDF
                pdf_context = f"A continuación se encuentra el contenido completo del PDF '{pdf_file.filename}':\n\n{pdf_text}\n\n"
                content.append(pdf_context)
                print(f"PDF procesado: {len(pdf_reader.pages)} páginas, {len(pdf_text)} caracteres")
                
            except Exception as pdf_error:
                print(f"Error procesando PDF: {str(pdf_error)}")
                return jsonify({
                    'error': f'Error al procesar el PDF: {str(pdf_error)}',
                    'success': False
                }), 400
        
        # Agregar imágenes si existen
        for image_file in images:
            image_bytes = image_file.read()
            image = Image.open(io.BytesIO(image_bytes))
            content.append(image)
        
        # Agregar mensaje de texto
        if message:
            content.append(message)
        
        # Si solo hay texto sin archivos, enviar directamente como string
        if not images and not pdf_file and message:
            content = message
        
        # Generar respuesta con streaming
        def generate():
            try:
                response = model.generate_content(content, stream=True)
                
                for chunk in response:
                    if chunk.text:
                        # Enviar cada chunk como JSON
                        data = json.dumps({
                            'chunk': chunk.text,
                            'done': False
                        })
                        yield f"data: {data}\n\n"
                        time.sleep(0.01)  # Pequeña pausa para efecto de escritura
                
                # Enviar señal de finalización
                final_data = json.dumps({
                    'chunk': '',
                    'done': True,
                    'model_used': selected_model
                })
                yield f"data: {final_data}\n\n"
                
            except Exception as e:
                error_data = json.dumps({
                    'error': str(e),
                    'done': True
                })
                yield f"data: {error_data}\n\n"
        
        print(f"Iniciando streaming de respuesta")
        
        return Response(
            stream_with_context(generate()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no'
            }
        )
    
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