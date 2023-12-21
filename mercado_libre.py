import requests
from lxml import html

def scrape_mercado_libre(search_query):
    url = f'https://listado.mercadolibre.com.mx/{search_query}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200: 
        tree = html.fromstring(response.text)

        # Obtener nombres de productos, precios y enlaces
        product_names = tree.xpath('//h2[@class="item__title"]/a/text()')
        prices = tree.xpath('//span[@class="price__fraction"]/text()')
        decimals = tree.xpath('//span[@class="price__decimals"]/text()')
        links = tree.xpath('//h2[@class="item__title"]/a/@href')

        formatted_prices = [f"${price}.{decimal}" if decimal else f"${price}" for price, decimal in zip(prices, decimals)]

        results = [{'Nombre': name, 'Precio': price, 'Enlace': link} for name, price, link in zip(product_names, formatted_prices, links)]

        return results
    else:
        print(f'Error al hacer la solicitud. Código de estado: {response.status_code}')
        return None

search_query = 'laptop'
results = scrape_mercado_libre(search_query)

if results:
    print(f'Resultados de la búsqueda "{search_query}":')
    for idx, product in enumerate(results, start=1):
        print(f'{idx}. Nombre: {product["Nombre"]}, Precio: {product["Precio"]}, Enlace: {product["Enlace"]}')
