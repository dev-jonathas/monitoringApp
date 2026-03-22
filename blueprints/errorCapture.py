import azure.functions as func
import json
from services.request_gpt import chamarOpenAi
import logging
from services.send_message_telegram import send_message

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
    
    mensagem_retorno = ""
    if(send_message(resultado) == 200):
        mensagem_retorno="Mensagem enviada com sucesso ao telegram"
    else:
        mensagem_retorno="Problema no envio da mensagem ao telegram"

    return func.HttpResponse(
        mensagem_retorno,
        status_code=200
    )