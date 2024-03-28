from math import sin, cos, sqrt, pi, asin
import requests
import os
import json
# Raio da Terra (aproximadamente)
EARTH_RADIUS = 6378.1370   # quilômetros

def retorna_nome_regiao(num_uf_regiao):
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
    resposta = requests.get(url)

    # Verifique se a requisição foi bem-sucedida
    if resposta.status_code == 200:
        # Extraia o nome do município da resposta JSON
        ufs = resposta.json()
        #print(ufs)
        uf_dict={}
        for i in ufs:
            uf_dict[i['id']]=i['nome']
            if int(i['id']) == int(num_uf_regiao):
                return i['nome']
    return ''

#abrir os arquivos e unificar os dados
def unificar_arquivos():
    json_gigante = {}
    for i in os.listdir('dbFiles'):
        with open(i, 'r') as arquivo_json:
            data = json.load(arquivo_json)
        break
    return json_gigante


def retorna_cidades(json_gigante):
    citys=[]
    return citys


def json_busca(name, json_gigante):
    for i in json_gigante:
        if json_gigante[i]['name'] == name:
            return json_gigante[i]
    return None


def unificar_arquivos():
    json_gigante = {}
    for i in os.listdir('dbFiles'):
        json_simplificado={}
        with open('dbFiles/'+i, 'r') as arquivo_json:
            data = json.load(arquivo_json)
        if data['dict_id'] not in json_gigante:
            json_gigante[data['dict_id']] = {
                'name':data['name'],
                'uf':data['uf'],
                'lat':float(data['extra_latitude']),
                'lon':float(data['extra_longitude'])}
        else:
            print('json existe, verificar ',data['dict_id'])
    return json_gigante


def distancia_haversine(lat1, lon1, lat2, lon2):
  """
  Calcula a distância entre dois pontos usando a fórmula de Haversine.

  Args:
    lat1 (float): Latitude do primeiro ponto em graus.
    lon1 (float): Longitude do primeiro ponto em graus.
    lat2 (float): Latitude do segundo ponto em graus.
    lon2 (float): Longitude do segundo ponto em graus.

  Returns:
    float: Distância entre os dois pontos em quilômetros.
  """

  # Converter graus para radianos
  lat1_rad = lat1 * pi / 180
  lon1_rad = lon1 * pi / 180
  lat2_rad = lat2 * pi / 180
  lon2_rad = lon2 * pi / 180

  # Calcular a diferença de latitude e longitude
  dlat = lat2_rad - lat1_rad
  dlon = lon2_rad - lon1_rad

  # Fórmula de Haversine
  a = sin(dlat/2) * sin(dlat/2) + cos(lat1_rad) * cos(lat2_rad) * sin(dlon/2) * sin(dlon/2)
  c = 2 * asin(sqrt(a))

  # Distância em quilômetros
  distance = c * EARTH_RADIUS

  return distance


def calcular_distancia(cidade1, cidade2):
    lat1, lon1 = float(cidade1['lat']), float(cidade1['lon'])
    lat2, lon2 = float(cidade2['lat']), float(cidade2['lon'])
    return distancia_haversine(lat1, lon1, lat2, lon2)


def retorna_lista_municios_raio(json_municipio, json_gigante, raio):
    json_retorna=[]
    for municipio in json_gigante:
        if json_gigante[municipio] not in json_retorna:
            if calcular_distancia(json_municipio, json_gigante[municipio])<=raio:
                if json_gigante[municipio]['uf'] == json_municipio['uf']:
                    _ = json_gigante[municipio]
                    _['distance'] = calcular_distancia(json_municipio, json_gigante[municipio])
                    json_retorna.append(_)
    return json_retorna


