import azure.functions as func
from blueprints.errorCapture import bp as errorCapture_bp

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

app.register_functions(errorCapture_bp)

