import azure.functions as func
import json

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
    
    return func.HttpResponse(
        json.dumps(newError),
        status_code=200
    )