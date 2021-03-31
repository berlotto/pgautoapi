from core.database import database
from core.sql.sql_utils import get_sql_for_model
from fastapi import Request
from pydantic import BaseModel


async def async_view_get_data_unique(
    request: Request, 
    reg_pk, 
    table_model: BaseModel):
    return {
        "user_id": 9898,
        "email": "meu@email.com",
        "name": "Flux",
        "id": reg_pk
       }


async def async_view_get_data(request: Request, table_model: BaseModel):
    query = get_sql_for_model(table_model, request)
    return await database.fetch_all(query)
