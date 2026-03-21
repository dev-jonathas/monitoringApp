import azure.functions as func
import json
from services.request_gpt import chamarOpenAi
import logging

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
    
    
    return func.HttpResponse(
        json.dumps(resultado),
        status_code=200
    )