import requests
import json
import time
import os

import fnmatch

def listar_arquivos_json(pasta):
    arquivos_json = []
    for root, dirs, files in os.walk(pasta):
        for filename in files:
            if fnmatch.fnmatch(filename, '*.json'):
                arquivos_json.append(os.path.join(root, filename))
    return arquivos_json


def obter_estados():
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao obter estados:", response.status_code)
        return None


def obter_cidades(estado_id):
    url = f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{estado_id}/municipios'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao obter cidades:", response.status_code)
        return None


def listar_estados():
    estados = obter_estados()
    ufs = {}
    if estados:
        for estado in estados:
            ufs[estado['id']]= estado['nome']
        return ufs
    return None


def listar_cidades(estado_id):
    cidades = obter_cidades(estado_id)
    if cidades:
        return cidades
    return None

def obter_dados_cidade_por_nome(nome_cidade, estado):
    while 1:
        url_base = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": f"{nome_cidade}, {estado}, Brazil",
            "format": "json",
            "limit": 1
        }

        response = requests.get(url_base, params=params)
        if response.status_code == 200:
            data = response.json()
            if data:
                cidade = data[0]
                nome = cidade.get('display_name', 'Nome não disponível')
                latitude = cidade.get('lat', 'Latitude não disponível')
                longitude = cidade.get('lon', 'Longitude não disponível')
                endereco = cidade.get('display_name', 'Endereço não disponível')
                return {
                    'nome': nome,
                    'latitude': latitude,
                    'longitude': longitude,
                    'endereco': endereco
                }
            else:
                print(f'erro Cidade não encontrada')
        else:
            print (f"erro: Erro ao fazer requisição HTTP: {response.status_code}")
            time.sleep(5)


# Função para percorrer recursivamente os dados e extrair chaves e valores
def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
    

def salva_data(data, name):
    result = {}
    # Percorrer o JSON e adicionar os dados ao dicionário de resultados
    for state, state_data in data.items():
        flat_state_data = flatten_dict(state_data)
        result.update(flat_state_data)
    # Imprimir o resultado
    with open(name, "w", encoding="utf-8") as arquivo_json:
        json.dump(result, arquivo_json, ensure_ascii=False, indent=4)


def create_db():
    states_list = listar_estados()
    dict_brazil = {}
    pasta = 'dbFiles'  # Substitua pelo caminho da sua pasta
    arquivos_json = listar_arquivos_json(pasta)
    if not states_list:
        return "Error in retrive state list, server offline test('https://servicodados.ibge.gov.br/api/v1/localidades/estados')"
    for nn,uf in enumerate(states_list):
        print('---------------------------------------------------------------------------------------------------------')
        city_list = listar_cidades(uf)
        dict_state={}
        if not city_list:
            return "Error in retrive state list, server offline test('https://servicodados.ibge.gov.br/api/v1/localidades/estados/{estado_id}/municipios')"
        for nnn, city in enumerate(city_list):
            file_name = 'dbFiles/'+str(uf)+'_'+city['nome']+".json"
            if file_name not in arquivos_json:
                print(nn, ' de ', len(states_list), '----- ',nnn, len(city_list))
                extraData=obter_dados_cidade_por_nome(city['nome'], uf)
                dict_state[city['nome']]={'name':city['nome'],'uf':uf,'dict':city,'extra':extraData}
                salva_data(dict_state, file_name)
            
        dict_brazil[states_list[uf]] = {'uf':uf,
                                    'stateName':states_list[uf],
                                    'cityes':dict_state}
    return 

def main():
    print(create_db())

if __name__ == "__main__":
   main()
    
