"""
Módulo que cria dinamicamente as classes BaseModel
que referenciam os campos das tabelas do banco de
dados.
"""
from datetime import datetime
from datetime import date
import logging as logger
from typing import Dict, Optional

from pydantic import BaseModel
from pydantic import create_model
from pydantic import BaseConfig

from core.database import database

_cached_table_fields = {}

class UnidentifiedBaseModel(BaseModel):
    not_found_model: Optional[str]

def get_pydatatype_from_dbdatatype(data_type: str):
    
    choices = (
        (lambda x: x in ['integer','bigint','smallint'], Optional[int]),
        (lambda x: x == 'character varying', Optional[str]),
        (lambda x: x == 'timestamp with time zone', Optional[datetime]),
        (lambda x: x == 'timestamp without time zone', Optional[datetime]),
        (lambda x: x == 'date', Optional[date]),
        (lambda x: x in ['numeric','double precision'], Optional[float]),
        (lambda x: x == 'boolean', Optional[bool]),
        (lambda x: x == 'text', Optional[str]),
        (lambda x: x == 'uuid', Optional[str]),
    )
    
    founds = [item[1] for item in choices if item[0](data_type)]
    if founds:
        return founds[0]
    else:
        # Por padrao retorna string ..
        # logger.warning(f"Python datatype not mapped for the database type: {data_type}")
        return str


async def get_db_table_informations() -> Dict:
    global _cached_table_fields
    if _cached_table_fields:
        return _cached_table_fields

    print("Getting table_models informations...")
    sql = (
        "select cc.table_catalog, cc.table_schema, tt.table_type, cc.table_name, cc.column_name,  "
        "       cc.data_type, cc.column_default, cc.is_nullable, cc.character_maximum_length, cc.is_updatable "
        "from information_schema.columns as cc "
        "inner join information_schema.tables as tt on tt.table_name = cc.table_name and tt.table_schema = cc.table_schema "
        "where cc.table_schema = 'public' "
        "order by cc.table_schema, cc.table_name, cc.ordinal_position "
    )
    columns = await database.fetch_all(sql)
    
    db_tables_mapping = {}
    for column in columns:

        table_name = column['table_name'] 

        if table_name not in db_tables_mapping.keys():
            db_tables_mapping[table_name] = {}

        c_name = column['column_name']
        db_datatype = column['data_type']
        nullable = column['is_nullable'] == 'YES'
        max_length = column['character_maximum_length']

        db_tables_mapping[table_name][c_name] = (get_pydatatype_from_dbdatatype(db_datatype), ...)

    print(f"  -> Obtivemos dados de {len(db_tables_mapping.keys())} tabelas neste banco de dados.")
    _cached_table_fields = db_tables_mapping
    return _cached_table_fields

"""
A variavel table_fields vai ter seu conteúdo no formato abaixo:
    table_fields = {
        'api_animal': {
            'id': (int,...),
            'tagNumber': (str,...),
            'deleted': (bool,...)
        },
        'api_herd': {
            'id': (int,...),
            'deleted': (bool,...),
            'name': (str,...),
        }
    }
"""

# https://pydantic-docs.helpmanual.io/usage/models/#dynamic-model-creation
async def get_table_model(table_name:str):
    table_fields = await get_db_table_informations()

    print(f"Getting '{table_name}' model ", end="")
    
    if table_name in table_fields.keys():
        table_model_class_name = ''.join([x.capitalize() for x in table_name.split("_")]) + 'Model'
        current_table_fields = table_fields[table_name]
        print(f"- Found '{table_model_class_name}'")

        class CustomConfig(BaseConfig):
            schema_extra = {
                'table_name':table_name
            }
        T = create_model(
            __model_name=table_model_class_name,
            __config__=CustomConfig,
            **current_table_fields)

        return T
    else:
        print(f"- Not Found")
        return UnidentifiedBaseModel
