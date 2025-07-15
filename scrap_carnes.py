import requests
from bs4 import BeautifulSoup
import csv

url = "https://losjardinesonline.com.py/catalogo/carnes-c48"
headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')
botones = soup.find_all('a', class_='button add_to_cart_button')

with open('productos_los_jardines.txt', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter='\t')  # tab separado
    writer.writerow(['Nombre', 'Precio', 'Categoría'])

    for boton in botones:
        nombre = boton.attrs.get('data-product_name', 'N/A')
        precio = boton.attrs.get('data-product_price', 'N/A')
        categoria = boton.attrs.get('data-product_category', 'N/A')

        writer.writerow([nombre, precio, categoria])

print("Archivo TXT (tab separado) guardado.")
