from flask import Flask, request, jsonify
import os
import requests
import openai

app = Flask(__name__)

@app.route('/image', methods=['POST'])
def generate_image():
    
    # Carga la variable de entorno 
    openai.api_key = os.getenv('OPENAI_API_KEY')
    api_key_1 = os.environ.get('OPENAI_API_KEY')

    # Obtener la descripción de la imagen desde el cuerpo de la solicitud
    prompt = request.json['prompt']
    
    text = request.json['text']
    
    completion = openai.Completion.create(  engine="text-davinci-003",
                                            prompt=f"clasifica el siguiente texto con solo una de las siguientes opciones: vulgar,discriminatorio,violento, texto aceptable: {text}",
                                            max_tokens=2048)
                        
    response = completion.choices[0].text
    
    if 'vulgar' in response.lower():
        response=1
    elif 'discriminatorio' in response.lower():
        response=2
    elif 'violento' in response.lower():
        response=3
    else:
        response=4
    if (response<4):
        return jsonify({'Error':text ' tiene lenguaje ofensivo del tipo ' response})
    else:
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
            'Authorization': f'Bearer {api_key_1}',
        }

        # Envía la solicitud HTTP POST con el encabezado de autorización y los datos de entrada
        response = requests.post(url, json=data, headers=headers)

        # Obtener la URL de la imagen generada desde la respuesta de la API
        image_url = response.json()['data']

        # Mostrar la URL de la imagen en la plantilla
        return jsonify(image_url)

@app.route('/bad-language', methods=['POST'])
def detect_bad_language():

    # Carga las variables de entorno
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Obtener el texto para verificar
    text = request.json['text']

    completion = openai.Completion.create(  engine="text-davinci-003",
                                            prompt=f"clasifica el siguiente texto con solo una de las siguientes opciones: vulgar,discriminatorio,violento, texto aceptable: {text}",
                                            max_tokens=2048)
                        
    response = completion.choices[0].text
    
    if 'vulgar' in response.lower():
        response=1
    elif 'discriminatorio' in response.lower():
        response=2
    elif 'violento' in response.lower():
        response=3
    else:
        response=4
        

    return jsonify({'classification':response})

@app.route('/sentiment', methods=['POST'])
def detect_snetiment():

    # Carga las variables de entorno
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Obtener el texto para verificar
    text = request.json['text']

    completion = openai.Completion.create(  engine="text-davinci-003",
                                            prompt=f"clasifica el siguiente texto con solo uno de los siguientes sentimientos: miedo, enfadado, triste, feliz o neutro: {text}",
                                            max_tokens=2048)
                        
    response = completion.choices[0].text
    
    if 'miedo' in response.lower():
        response=1
    elif 'enfadado' in response.lower():
        response=2
    elif 'triste' in response.lower():
        response=3
    elif 'feliz' in response.lower():
        response=4
    else:
        response=5
        
    return jsonify({'sentiment':response})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
