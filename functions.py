def bad_language(imput_text, api_key):
  
    import openai
    import os
    from collections import Counter
    #Validar mensaje
    # Carga las variables de entorno
    openai.api_key = api_key

    answers = []
    # Obtener el texto para verificar
    text = imput_text

    completion = openai.Completion.create(  engine="text-davinci-003",
                                            prompt=f"toma como referencia las vulgaridades españolas y clasifica el siguiente texto con solo una de las siguientes opciones: vulgar,discriminatorio,violento, texto aceptable: {text}",
                                            n=5,
                                            max_tokens=2048)
                        
    for i  in range(0,5):
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
    
    return answers

def vectorizer (data):
    data.fillna(value='', inplace=True)
    data = data.loc[:,['_id','nationality','profession','hobby','hobby2','prefLocation']]
    vectorizer = CountVectorizer()
    location_vectorizer = vectorizer.fit_transform(data['prefLocation'])
    nationality_vectorizer = vectorizer.fit_transform(data['nationality'])
    profession_vectorizer = vectorizer.fit_transform(data['profession'])
    hobby_vectorizer = vectorizer.fit_transform(data['hobby'])
    hobby2_vectorizer = vectorizer.fit_transform(data['hobby2'])
    caracteristicas = hstack([location_vectorizer,nationality_vectorizer,profession_vectorizer,hobby_vectorizer,hobby2_vectorizer])
    caracteristicas_df = pd.DataFrame.sparse.from_spmatrix(caracteristicas)
    return caracteristicas_df
  
def serialize_objectid(obj):
    if isinstance(obj, bson.ObjectId):
        return str(obj)
    return obj
