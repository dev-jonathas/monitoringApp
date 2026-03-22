import os
import uuid
from datetime import datetime, timezone

from azure.core.exceptions import ResourceExistsError
from azure.data.tables import TableServiceClient

TABLE_NAME = "alertas"

connection_string = os.getenv("AzureWebJobsStorage")

service_client = TableServiceClient.from_connection_string(connection_string)
table_client = service_client.get_table_client(table_name=TABLE_NAME)


#def save_alerta(alert)

now = datetime.now()


entity = {
    "PartitionKey": now.strftime("%Y%m%d"), #todos os alertas do mesmo dia ficam juntos
    "RowKey": str(uuid.uuid4()),
    "error_id": "OPS1234",
    "description": "descricao do erro",
    "action": "lerta do erro",
    "overview": "loren ipsun",
    "timestamp": now.isoformat()
}

print(table_client.create_entity(entity))