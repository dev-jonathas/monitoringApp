from models.alerta import Alerta

def message_constructor(novo_erro: Alerta) -> str:
    msg = f"""
    <b>🚨 Alerta do Sentinela!</b>

    ⚠️ <b>Erro:</b> <code>{novo_erro.error_id}</code>

    <b> Overview da IA:</b>
    {novo_erro.overview}
    <blockquote><i>Este texto foi gerado por uma inteligência artificial e pode conter erros.</i></blockquote>

    <b>📊 Dados complementares:</b>
    <b>Action:</b> {novo_erro.action}
   
    <b>Description:</b> {novo_erro.description}
    """

    return msg