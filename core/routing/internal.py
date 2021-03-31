from typing import List

from fastapi import Request
from pydantic.main import BaseModel
from core.application import app
from core.modelling import get_db_table_informations
from core.routing import get_used_tables_info

class TablesInfoResponse(BaseModel):
    total: int
    used: List[str]
    disponible: List[str]
    
    class Config:
        schema_extra = {
            "example": {
                "count": 3,
                "used": [
                    "table_three"
                ],
                "disponible": [
                    "table_one",
                    "table_two"
                ]
            }
        }


@app.get('/')
async def status(request: Request):
    return {"status":"ok"}


@app.get('/_tables', response_model=TablesInfoResponse)
async def show_tables():
    used_tables_info = get_used_tables_info()
    table_data = await get_db_table_informations()
    
    used_tables = {x[0] for x in used_tables_info}
    all_tables = {table for table in table_data.keys()}

    tables_info = TablesInfoResponse(
        total=len(all_tables), 
        used=sorted(used_tables),
        disponible=sorted(all_tables - used_tables)
    )
    return tables_info
