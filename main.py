from flask import Flask, request, render_template, jsonify
import os
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def generate_image():
    
    # Carga las variables de entorno desde el archivo key.env
    from dotenv import load_dotenv
    load_dotenv('key.env')
    api_key = os.getenv('OPENAI_API_KEY')

    # Obtener la descripción de la imagen desde el cuerpo de la solicitud
    prompt = request.args['prompt']
    print(request.__dict__)
    # Define la URL de la API y los datos de entrada
    url = 'https://api.openai.com/v1/images/generations'
    data = {
        'prompt': prompt,
        'n': 4,
        'size': '1024x1024',
        'response_format': 'url',
        'user': 'my-unique-user-id'
    }

    # Define el encabezado de autorización que incluye su clave API
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    # Envía la solicitud HTTP POST con el encabezado de autorización y los datos de entrada
    response = requests.post(url, json=data, headers=headers)

    # Obtener la URL de la imagen generada desde la respuesta de la API
    image_url = response.json()['data']

    # Mostrar la URL de la imagen en la plantilla
    return jsonify(image_url)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
