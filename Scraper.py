from selenium import webdriver


def obtener_tarifas(tarifas):
    




if __name__ == "__main__":
    #le podemos agregar opciones a nuestra busqueda
    option = webdriver.ChromeOptions()
    #en este caso vams a abrir el navegador en modo incognito
    option.add_argument('--incognito')
    #instanciar el driver del navegador
    driver = webdriver.Chrome(executable_path='C:/chrome_driver/chromedriver', options=option)

    #hacer que el navegador carge la pagina
    driver.get(link)