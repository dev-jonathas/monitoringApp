import azure.functions as func
import json
from services.request_gpt import chamarOpenAi
import logging
from services.send_message_telegram import send_message
from models.alerta import Alerta
from services.table_storage import save_alerta

bp = func.Blueprint()



#Como o método é só POST, então se der um GET vai dar um 404    
@bp.route(route="receiver", methods=["POST"])
def get_error(req: func.HttpRequest) -> func.HttpResponse:
    try:
        newError = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Your body isn't a valid JSON. Get better loser", status_code=400
        )

    resultado = chamarOpenAi(newError)

    novo_erro = Alerta(
        error_id=newError['error'],
        description=newError['description'],
        action=newError['action'],
        overview=resultado
    )
    
    mensagem_retorno = ""
    
    #logging.info(novo_erro)
    resultadoDoSalvamento = save_alerta(novo_erro)
    
    resultadoDoEnvioTelegram = send_message(novo_erro)

    return func.HttpResponse(
        f"{resultadoDoSalvamento}\n{resultadoDoEnvioTelegram}",
        status_code=200
    )