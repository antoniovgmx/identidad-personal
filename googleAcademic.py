from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import os

def findGoogle(search_param):
    #Ignorar los certificados:
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--disable-deb-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument('ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.headless = True

    #Chrome drivers
    driver = Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=options)

    #Navegar a google academico
    driver.get('https://scholar.google.com/citations?view_op=search_authors&mauthors=&hl=en&oi=ao')

    #Esperar 10 segundos para el buscador
    search = WebDriverWait(driver, timeout = 10).until(lambda d: d.find_element_by_class_name('gs_in_txt'))

    #Buscar un resultado
    search.send_keys(search_param)
    search.send_keys(Keys.RETURN)

    #Verificar si existen resultados por 5 segundos
    try:
        WebDriverWait(driver, timeout = 10).until(lambda d : d.find_elements_by_class_name("gsc_1usr"))
        print("se encontraton resultado")
    except:
        return [{ "error" : "Sin resultados" }]

    #Entrar a los articulos 
    driver.find_element_by_class_name('gs_ai_pho').click()

    #Esperar a que la pagina cargue por 5 segundos
    try:
        WebDriverWait(driver, timeout = 10).until(lambda d: d.find_element_by_id('gsc_a_b')) 

        #Cargar todos los articulos
        driver.find_element_by_id('gsc_bpf_more').click()
        time.sleep(1) #TODO Mejorar esta linea
    except:
        pass

    #Esperar a que los articulos se carguen por 10 segundos
    articles = WebDriverWait(driver, timeout = 10).until(lambda d: d.find_elements_by_class_name('gsc_a_tr'))
    print(len(articles))

    #Ciclando articulos
    for article in articles:

        #Obtener datos
        title = article.find_element_by_class_name('gsc_a_at').text
        autors = article.find_element_by_class_name('gs_gray').text
        year = article.find_element_by_class_name('gsc_a_y').text
        
        #manejo de expecion si no existe fecha
        #TODO

        #Objeto de articulos
        data = {
            "title" : title,
            "autors" : autors,
            "year" : year
        }

        #Agregar datos a lista
        articlesData.append(data)

    return articlesData
# print(findGoogle("escudero-nahon"))

