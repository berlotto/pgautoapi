import re

from pydantic import BaseModel

__all__ = ['get_sql_for_model']

hasupper = re.compile(r'[A-Z]+')

def _namequote(fieldname:str):
    return f"\"{fieldname}\"" if hasupper.search(fieldname) else fieldname


def get_projection(tablemodel: BaseModel) -> str:
    modelschema = tablemodel.schema()
    return ", ".join(
        [_namequote(field) for field 
         in modelschema.get('properties',{}).keys()]
    )

def get_tablename(tablemodel: BaseModel) -> str:
    modelschema = tablemodel.schema()
    table_name = tablemodel.Config.schema_extra.get('table_name',None)
    if not table_name:
        table_name = tablemodel.schema()['title']
    return table_name


def get_orderbyclause(tablemodel, request) -> str:
    return ""


def get_limitclause(tablename, request) -> str:
    return " LIMIT 10 "


def get_offsetclause(tablename, request) -> str:
    return "OFFSET 0"


def get_sql_for_model(tablemodel: BaseModel, request):
    return (
        "SELECT " + \
        get_projection(tablemodel) + \
        " FROM " + \
        get_tablename(tablemodel)  + \
        get_orderbyclause(tablemodel, request)  + \
        get_limitclause(tablemodel, request)  + \
        get_offsetclause(tablemodel, request)
    )
