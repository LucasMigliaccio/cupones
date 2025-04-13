import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Lista de artículos (podés cargarlo desde Excel/CSV también)
articulos = [
    "LOA0024418WB02",
    "LOA0024418WM10",
    "LOA0024618MB02",
    "LOA0024618MM10",
    "LOI00242614MN01",
    "LOI00243210MA11",
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

def buscar_imagen(codigo):
    url = f"https://www.dexter.com.ar/buscar?q={codigo}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Buscar la primera imagen de producto
    img_tag = soup.find("img", class_="tile-image second-image")
    
    if img_tag and "src" in img_tag.attrs:
        return img_tag["src"]
    else:
        return "No encontrada"

# Armar resultados
resultados = []
for codigo in articulos:
    imagen_url = buscar_imagen(codigo)
    resultados.append({"Código": codigo, "Imagen": imagen_url})

# Convertimos a DataFrame y mostramos
df = pd.DataFrame(resultados)
print(df)

with open(f"{codigo}.jpg", "wb") as f:
    f.write(requests.get(imagen_url).content)