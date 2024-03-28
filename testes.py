from sanic import Sanic, Request, text, json
from sanic.response import file
from main import data_return


app = Sanic(__name__)

@app.route("/")
async def index(request: Request):
    return text("O estado é uma gangue, imposto e inflação são roubo!")

@app.route("/pesquisa/<raio:int>/<pesquisa:str>/<cidade:str>")
async def get_dicionario(request: Request, raio: int, pesquisa: str, cidade: str):
    return json(data_return(pesquisa=pesquisa,raio=raio, cidade=cidade))

@app.route("/arquivo/<nome_arquivo>")
async def get_arquivo(request: Request, nome_arquivo: str):
    file_path = f"files/{nome_arquivo}"
    try:
        return await file(file_path)
    except FileNotFoundError:
        return text("Arquivo não encontrado", status=404)

if __name__ == "__main__":
    app.run()
