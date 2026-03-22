import os
import uuid
from datetime import datetime, timezone
from models.alerta import Alerta


from azure.core.exceptions import ResourceExistsError
from azure.data.tables import TableServiceClient

TABLE_NAME = "alertas"

connection_string = os.getenv("AzureWebJobsStorage")

service_client = TableServiceClient.from_connection_string(connection_string)
table_client = service_client.get_table_client(table_name=TABLE_NAME)


def save_alerta(novoErro: Alerta) -> str:

    now = datetime.now()


    entity = {
        "PartitionKey": now.strftime("%Y%m%d"), #todos os alertas do mesmo dia ficam juntos
        "RowKey": str(uuid.uuid4()),
        "error_id": novoErro.error_id,
        "description": novoErro.description,
        "action": novoErro.action,
        "overview": novoErro.overview,
        "timestamp": now.isoformat()
    }
    try:
        table_client.create_entity(entity)
    except:
        return "Não foi possível salvar no Storage Table"
    
    return "Salvo no Storage Table com sucesso!"