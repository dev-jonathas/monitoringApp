import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

#Primeira função para receber um json e trabalhar em cima dele
@app.route(route="receiver")    
def error_receiver(req: func.HttpRequest) -> func.HttpResponse:

    try:
        erro = req.get_json()
    except:
        return func.HttpResponse(
            status_code=333
        )

    error = erro['error']
    action = erro['action']

    return func.HttpResponse(
        f"seu erro foi {error}",
        status_code=200
    )


