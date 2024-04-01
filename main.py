import time
import threading
from searchTools import *
from scrapingTools import pesquisa_inicial, salva_em_excel


DEEP = 25 #vezes em que ele da pagedown na pagina, basicamente o quanto ele procura
RAIO = 15   #raio de pesquisa
NUMTHREADS = 8
NAO_MOSTRAR_BROWSER = True
MINIMO_REGISTROS = 1
MAXIMO_TENTATIVAS_DEEP = 2

def process_municipio(lista, pesquisa, municipio, semaphore, counter_lock, counter, lista_municipios):
    #print(municipio)
    #print(retorna_nome_regiao(municipio['uf']))
    with semaphore:
        start_time_now = time.time()
        lista[municipio['name']] = {'data': pesquisa_inicial(f"{pesquisa}+{municipio['name']}+{retorna_nome_regiao(municipio['uf']).replace(' ','+')}",DEEP,NAO_MOSTRAR_BROWSER,num_min_registros=MINIMO_REGISTROS,max_try=MAXIMO_TENTATIVAS_DEEP),
                                    'times': {}}
        lista[municipio['name']]['times'][f"{pesquisa}+{municipio['name']}+{municipio['uf']}"] = time.time() - start_time_now
        with counter_lock:
            counter[0] += 1
            #print(f"Pesquisas concluídas: {counter[0]} de {len(lista_municipios)}")


def data_return(pesquisa="padarias+perto+de",raio=RAIO, cidade="Piracicaba", deep=DEEP,minimum_register_return=MINIMO_REGISTROS,max_deep_trys=MAXIMO_TENTATIVAS_DEEP,filename=None):
    json_gigante = unificar_arquivos()
    pesquisa = "padarias+perto+de"
    lista_municipios = retorna_lista_municios_raio(json_busca(cidade, json_gigante), json_gigante, raio)
    lista = {'timeOfSearch': 0}
    start_time = time.time()

    semaphore = threading.Semaphore(NUMTHREADS)  # Criando um semáforo com limite de 4 threads simultâneas
    counter_lock = threading.Lock()  # Lock para garantir a integridade do contador
    counter = [0]  # Contador compartilhado entre as threads

    threads = []
    for municipio in lista_municipios:
        thread = threading.Thread(target=process_municipio, args=(lista, pesquisa, municipio, semaphore, counter_lock, counter, lista_municipios))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    lista['timeOfSearch'] = str(time.time() - start_time)
    if filename:
        salva_em_excel(lista, filename)
    return lista


#if __name__ == "__main__":
#    main()