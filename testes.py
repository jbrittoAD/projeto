from sanic import Sanic, Request, text, json
from sanic.response import file
from main import data_return


app = Sanic(__name__)

@app.route("/")
async def index(request: Request):
    return text("O estado é uma gangue, imposto e inflação são roubo!")

@app.route("/pesquisa/<raio:int>/<pesquisa:str>/<cidade:str>/<deep:int>/<minimum_register_return:int>/<max_deep_trys:int>/<filename:str>")
async def get_dicionario(request: Request, raio: int, pesquisa: str, cidade: str,deep:int, minimum_register_return:int,max_deep_trys:int,filename:str ):
    return json(data_return(pesquisa=pesquisa,raio=raio, cidade=cidade,deep=deep,minimum_register_return=minimum_register_return,max_deep_trys=max_deep_trys,filename=filename))
#data_return(pesquisa="padarias+perto+de",raio=RAIO, cidade="Piracicaba", deep=DEEP,minimum_register_return=MINIMO_REGISTROS,max_deep_trys=MAXIMO_TENTATIVAS_DEEP)
@app.route("/arquivo/<nome_arquivo>")
async def get_arquivo(request: Request, nome_arquivo: str):
    file_path = f"files/{nome_arquivo}"
    try:
        return await file(file_path)
    except FileNotFoundError:
        return text("Arquivo não encontrado", status=404)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
