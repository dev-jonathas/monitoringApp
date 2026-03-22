

def message_constructor(error:str, description:str, action:str, overview:str) -> str:
    msg = f"""
    <b>🚨 Alerta do Sentinela!</b>

    ⚠️ <b>Erro:</b> <code>{error}</code>

    <b>🧠 Overview da IA:</b>
    {overview}

    <blockquote><i>Este texto foi gerado por uma inteligência artificial e pode conter erros.</i></blockquote>

    <b>📊 Dados complementares:</b>
    <b>Action:</b> {action}
    <b>Description:</b> {description}
    """