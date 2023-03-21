from flask import Flask, request, jsonify
import os
import requests
import openai

app = Flask(__name__)

@app.route('/image', methods=['POST'])
def generate_image():
    
    # Carga la variable de entorno 
    api_key = os.environ.get('OPENAI_API_KEY')

    # Obtener la descripción de la imagen desde el cuerpo de la solicitud
    prompt = request.json['prompt']
   
    # Define la URL de la API y los datos de entrada
    url = 'https://api.openai.com/v1/images/generations'
    data = {
        'prompt': prompt,
        'n': 2,
        'size': '512x512',
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

@app.route('/bad-lenguage', methods=['POST'])
def generate_bad_text():

    # Carga las variables de entorno
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Obtener el texto para verificar
    text = request.json['text']

    completion = openai.Completion.create(  engine="text-davinci-003",
                                            prompt=f"clacifica el siguiente texto como vulgar, discriminatorio,violento o de acoso: {text}",
                                            max_tokens=2048)
                        
    response = completion.choices[0].text

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
