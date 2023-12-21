from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
def ir_paginas_amarillas_web(cadena, city):
  driver = webdriver.Firefox(executable_path=r'./webdriver/')
  lista_datos = []
  try:
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "whatInput")))
    input_nombre = driver.find_element_by_id("whatInput")
    input_nombre.send_keys(cadena)
    input2_nombre = driver.find_element_by_id("whereInput")
    input2_nombre.send_keys(city)
    boton = driver.find_element_by_id("submitBtn")
    boton.click()
  except:
    print ("El elemento no está presente")
  try:
    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "listado-item")))
  except:
    print ('Elementos no encontrados')
  resultados = driver.find_elements_by_class_name("listado-item")
  for resultado in resultados:
    try:
      datos = resultado.find_element_by_class_name("box")
      print ('datos=', datos.text)
    except:
      datos='-'
      print('datos=0')
    print ("==============================\n")
 
  driver.close()
  return lista_datos
 
def main():
  print (ir_paginas_amarillas_web('talleres de coches','Barcelona'))
main()