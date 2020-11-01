from selenium import webdriver
import pprint
import time


def obtener_precios(vuelo):
    precios = []
    tarifas = vuelo.find_elements_by_xpath('//div[@class = "fares-table-wrapper"]')
    for tarifa in tarifas:
        nombre = tarifa.find_element_by_xpath('.//div[@class = "attribute-header-wrapper"]/span').text
        moneda = tarifa.find_element_by_xpath('.//span[@class = "price"]/span[@class = "currency-symbol"]').text
        valor = tarifa.find_element_by_xpath('.//span[@class = "price"]/span[@class = "value"]').text
        dict_tarifa = {nombre:{'moneda':moneda,'valor':valor}}
        precios.append(dict_tarifa)
    return precios

def obtener_datos_escalas(vuelo):
    segmentos = vuelo.find_elements_by_xpath('//div[@class = "sc-hZSUBg gfeULV"]/div[@class = "sc-cLQEGU hyoued"]')
    escalas = vuelo.find_elements_by_xpath('//div[@class = "sc-hZSUBg gfeULV"]/div[@class = "sc-cLQEGU dnKRNG"]')
    info_escalas = []
    for i,segmento in enumerate(segmentos):
        horas = segmento.find_elements_by_xpath('.//time[@class = "sc-RefOD libzvk"]')
        hora_de_salida = horas[0].get_attribute('datetime')
        hora_de_llegada = horas[1].get_attribute('datetime')
        ciudades = segmento.find_elements_by_xpath('.//abbr[@class = "sc-hrWEMg hlCkST"]')
        ciudad_origen = ciudades[0].get_attribute('title')
        ciudad_destino = ciudades[1].get_attribute('title')
        duracion_del_vuelo = segmento.find_element_by_xpath('.//span[@class = "sc-esjQYD dMquDU"]/time').get_attribute('datetime')
        numero_de_vuelo = segmento.find_element_by_xpath('.//div[@class = "airline-flight-details"]//b').text
        modelo_del_avion = segmento.find_element_by_xpath('.//div[@class = "airline-flight-details"]/span[@class = "sc-gzOgki uTyOl"]').text
        if i != len(segmentos)-1:
            duracion_de_escala = escalas[i].find_element_by_xpath('.//span[@class = "sc-esjQYD dMquDU"]/time').get_attribute('datetime')
        else:
            duracion_de_escala = ''
            
        data_dict = {
            'origen':ciudad_origen,
            'hora de salida':hora_de_salida,
            'destino':ciudad_destino,
            'hora de llegada':hora_de_llegada,
            'duracion:':duracion_del_vuelo,
            'numero de vuelo':numero_de_vuelo,
            'modelo de avion':modelo_del_avion,
            'duracion de escala':duracion_de_escala
        }
        info_escalas.append(data_dict)
    return info_escalas

def obtener_tiempos(vuelo):
    hora_salida = vuelo.find_element_by_xpath('.//div[@class = "departure"]/time').get_attribute('datetime')
    hora_llegada = vuelo.find_element_by_xpath('.//div[@class = "arrival"]/time').get_attribute('datetime')
    tiempo_vuelo = vuelo.find_element_by_xpath('.//span[@class = "duration"]/time').text
    tiempos = {
        'hora de salida':hora_salida,
        'hora de llegada':hora_llegada,
        'tiempo de vuelo':tiempo_vuelo
    }
    return tiempos

def obtener_info(driver):
    #cerrar ventana emergente
    driver.find_element_by_xpath('//div[@class = "slidedown-footer"]/button[@class = "align-right secondary slidedown-button"]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//div[@class = "lightbox-top"]/span[@class = "close"]').click()
    time.sleep(0.5)
    #extraer los vuelos
    vuelos = driver.find_elements_by_xpath('//li[@class = "flight"]')
    print(f'Se encontraron {len(vuelos)} vuelos')
    print('Iniciando scraping...')
    info = []
    for vuelo in  vuelos:
        #extraer los tiempos generales
        tiempos = obtener_tiempos(vuelo)
        #abrir la ventana de escalas
        vuelo.find_element_by_xpath('.//div[@class = "flight-summary-stops-description"]/button').click()
        time.sleep(1)
        #extraer escalas
        escalas = obtener_datos_escalas(vuelo)
        #cerrar la ventana
        vuelo.find_element_by_xpath('//div[@class = "modal-header sc-dnqmqq cGfTsx"]/button').click()
        time.sleep(0.5)
        #abrir los detalles de las tarifas
        vuelo.click()
        time.sleep(1.5)
        #extraer los precios
        precios = obtener_precios(vuelo)
        #cerramos los detalles de las tarifas
        vuelo.click()
        time.sleep(0.5)
        info.append({'precios':precios,
                     'tiempos':tiempos,
                     'escalas':escalas})
    return info




if __name__ == "__main__":
    link = 'https://www.latam.com/es_co/apps/personas/booking?fecha1_dia=04&fecha1_anomes=2020-11&fecha2_dia=28&fecha2_anomes=2020-11&from_city2=MEX&to_city2=BGA&auAvailability=1&ida_vuelta=ida&vuelos_origen=Bucaramanga&from_city1=BGA&vuelos_destino=Ciudad%20de%20M%C3%A9xico&to_city1=MDE&flex=1&vuelos_fecha_salida_ddmmaaaa=29/10/2020&vuelos_fecha_regreso_ddmmaaaa=28/11/2020&cabina=Y&nadults=1&nchildren=0&ninfants=0&cod_promo=&stopover_outbound_days=0&stopover_inbound_days=0&application=#/'
    #le podemos agregar opciones a nuestra busqueda
    option = webdriver.ChromeOptions()
    #en este caso vams a abrir el navegador en modo incognito
    option.add_argument('--incognito')
    #option.add_argument('--headless')
    option.add_argument('--disable-dev-shm-usage')
    #instanciar el driver del navegador
    driver = webdriver.Chrome(executable_path='C:/chrome_driver/chromedriver', options=option)

    #hacer que el navegador carge la pagina
    driver.get(link)
    time.sleep(70)
    pp = pprint.PrettyPrinter()
    info = obtener_info(driver)
    driver.close()
    pp.pprint(info)