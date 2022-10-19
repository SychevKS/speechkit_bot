import random
import json
import urllib.request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neural_network import MLPClassifier

# Загрузка диалогов для обучалки
url = "https://drive.google.com/uc?export=view&id=1u4sNekGHaDzgkOVzCOAbyWpFTEMfu95Z"
filename = "intents_dataset.json"
urllib.request.urlretrieve(url, filename)

# файл в словарь
with open(filename, 'r', encoding='UTF-8') as file:
    data = json.load(file)

# массивы фраз и интентов
x = []
y = []

for name in data:
    for phrase in data[name]['examples']:
        x.append(phrase)
        y.append(name)
    for phrase in data[name]['responses']:
        x.append(phrase)
        y.append(name)

# векторизуем фразы х
vectorizer = CountVectorizer()
vectorizer.fit(x)
x_vec = vectorizer.transform(x)

# создает модель и обучаем
model = MLPClassifier()
model.fit(x_vec, y)

def get_intent(text):
    text_vec = vectorizer.transform([text])
    return model.predict(text_vec)[0]

def get_response(intent):
    return random.choice(data[intent]['responses'])