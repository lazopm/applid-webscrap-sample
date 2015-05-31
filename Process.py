from bs4 import BeautifulSoup

def validate(response):
    if "Por favor reingrese Captcha" in response:
        return 1
    else:
        return 2
def process(data):
    if "no existe en las Bases de Datos del Servicio" in data:
        return 1
    else:
        array={'nombre': '', 'monedaex': '', 'pyme': '', 'actividades': [], 'documentos': []}
        soup=BeautifulSoup(data)
        array['nombre']=findName(soup)
        array['monedaex']=findCurrency(soup)
        array['pyme']=findPYME(soup)
        array['actividades']=findActivities(soup)
        array['documentos']=findDocs(soup)
        return array

def findName(soup):
    found=0
    for div in soup.find(id='contenedor').find_all('div'):
        if found==1:
            return div.text.strip()
        else:
            if "Nombre o Razón Social :" in div.text:
                found=1
def findCurrency(soup):
    for div in soup.find(id='contenedor').find_all('span'):
        if "Contribuyente autorizado para declarar y pagar sus impuestos en moneda extranjera:" in div.text:
            return div.text.strip()[83:]
def findPYME(soup):
    for div in soup.find(id='contenedor').find_all('span'):
        if "Contribuyente es EMPRESA DE MENOR TAMAÑO PRO-PYME:" in div.text:
            return div.text.strip()[51:]
def findActivities(soup):
    acts = []
    for table in soup.find_all('table'):
        if "Actividades" in table.find('td').text:
            keys = ['act', 'cod', 'cat', 'iva']
            for row in table.find_all('tr')[1:]:
                values = []
                for cell in row.find_all('td'):
                    values.append(cell.text.strip())
                acts.append(dict(zip(keys,values)))
    return acts

def findDocs(soup):
    docs = []
    for table in soup.find_all('table'):
        if "Documento" in table.find('td').text:
            keys = ['doc', 'tim']
            for row in table.find_all('tr')[1:]:
                values = []
                for cell in row.find_all('td'):
                    values.append(cell.text.strip())
                docs.append(dict(zip(keys,values)))
    return docs
