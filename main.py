from fastapi import FastAPI
from pydantic import BaseModel
from bs4 import BeautifulSoup
import requests
from google.cloud import bigquery

app = FastAPI()

# Modelo de dados para a API
class Article(BaseModel):
    title: str
    content: str

# Função para obter o conteúdo limpo de um URL
def get_clean_content(url):
    # Obtendo o conteúdo da resposta
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')

    # Encontrando todos os elementos que têm a div <div data-testid="edinburgh-card">
    elements = soup.find_all("div", {"data-testid": "edinburgh-card"})

    result = []
    for element in elements:
        # Obtendo o texto do <h2> presente na div
        h2_text = element.find("h2").get_text()
        
        # Encontrando a tag de parágrafo (<p>) presente na div
        p_tag = element.find("p")
        
        # Verificando se há uma tag de parágrafo encontrada
        if p_tag:
            p_text = p_tag.get_text()
        else:
            p_text = None

        # Encontrando o elemento <span> com o último update
        last_updated_element = element.find("span", {"data-testid": "card-metadata-lastupdated"})
        
        # Verificando se o elemento <span> com o último update foi encontrado
        if last_updated_element:
            last_updated_text = last_updated_element.get_text()
        else:
            last_updated_text = None
        
        # Encontrando o elemento <span> com o tópico da notícia
        topic_element = element.find("span", {"data-testid": "card-metadata-tag"})
        
        # Verificando se o elemento <span> com o tópico da notícia foi encontrado
        if topic_element:
            topic_text = topic_element.get_text()
        else:
            topic_text = None
        
        result.append({"title": h2_text, "description": p_text, "last_Update": last_updated_text, "topic": topic_text})
    
    return result

# Rota Raiz
@app.get("/")
def raiz():
    clean_content = get_clean_content('https://www.bbc.com/')
    return clean_content
