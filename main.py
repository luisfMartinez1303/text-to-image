from flask import Flask, request, jsonify
import os
import requests
import openai
from collections import Counter
from flask_cors import CORS
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://frontend-nomad-list.vercel.app", "https://frontend-nomad-list.vercel.app/"]}})

@app.route('/image', methods=['POST'])
def generate_image():
    
    # Carga la variable de entorno 
    api_key = os.environ.get('OPENAI_API_KEY')
    
    # Obtener la descripción de la imagen desde el cuerpo de la solicitud
    prompt = request.json['prompt']

    url = 'https://api.openai.com/v1/images/generations'
    data = {
        'prompt': prompt,
        'n': 2,
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
        
@app.route('/bad-language', methods=['POST'])
def detect_bad_language():

    # Carga las variables de entorno
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    answers = []
    # Obtener el texto para verificar
    text = request.json['text']

    completion = openai.Completion.create(  engine="text-davinci-003",
                                            prompt=f"teniendo en las vulgaridades españolas, clasifica el siguiente texto con solo una de las siguientes opciones: vulgar,discriminatorio,violento, texto aceptable: {text}",
                                            n=5,  
                                            max_tokens=2048)
                        
    for i  in range(0,4):
        response = completion.choices[i].text

        if 'vulgar' in response.lower():
            response=1
        elif 'discriminatorio' in response.lower():
            response=2
        elif 'violento' in response.lower():
            response=3
        else:
            response=4
        answers.append(response)

    def valor_mas_comun(lista):
        contador = Counter(lista)
        valor, frecuencia = contador.most_common(1)[0]
        return valor

    answers = valor_mas_comun(answers)

    return jsonify({'classification':answers})

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

#1. Ruta para obtener todos los barrios sin argumentos

@app.route('/country_features/all', methods=['GET'])
def features_all():
    # Create an engine instance
    alchemyEngine   = create_engine("postgresql://postgres:kuM9CV4u5ItI8JlcDNLB@containers-us-west-102.railway.app:7684/railway", pool_recycle=3600);

    # Connect to PostgreSQL server
    dbConnection  = alchemyEngine.connect()

    # Read data from PostgreSQL database table and load into a DataFrame instance
    dataFrame = pd.read_sql("select * from country_features", dbConnection)

    pd.set_option('display.expand_frame_repr', False)

    # Close the database connection
    dbConnection.close()

    #Creamos un json
    json = dataFrame.to_json(orient = "records")
    json

    return jsonify(json)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
