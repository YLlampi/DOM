from selenium import webdriver
from selenium.webdriver.common.by import By

# Iniciar el navegador
driver = webdriver.Chrome()

# Abrir la página de Mercado Libre
driver.get("https://www.mercadolibre.com")

# Encontrar el campo de búsqueda y enviar una consulta
search_box = driver.find_element(By.XPATH, '//input[@name="as_word"]')
search_box.send_keys("laptop")
search_box.submit()

# Esperar a que se cargue la página de resultados
driver.implicitly_wait(10)

# Extraer información de los primeros resultados
results = driver.find_elements(By.XPATH, '//li[@class="results-item"]')

for result in results:
    title = result.find_element(By.XPATH, './/h2').text
    price = result.find_element(By.XPATH, './/span[@class="price__fraction"]').text
    print(f'Título: {title}, Precio: {price}')

# Cerrar el navegador
driver.quit()
