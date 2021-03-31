from typing import Callable, List, Optional

from core.application import app
from core.database import database
from core.exceptions import (AlreadyConfiguredTableException,
                             TableNotConfiguredYetException,
                             MethodNotAllowedException)
from core.modelling import get_table_model
from core.routing.reading import (async_view_get_data,
                                  async_view_get_data_unique)
from fastapi import FastAPI, Request, status
from pydantic import BaseModel

# List of (table_name, rounting_url)
_routing_mapping = []

__all__ = ["expose_table","get_used_tables_info"]

def get_used_tables_info():
    return _routing_mapping

async def expose_table(
    table_name: str, 
    alias: Optional[str] = None,
    read_only: bool = False
):
    global _routing_mapping
    base_table_url = f"/{alias or table_name}".lower()

    alread_configured = \
        any([x for x in _routing_mapping 
             if x[0] == table_name or x[1] == base_table_url])
    if alread_configured:
        raise AlreadyConfiguredTableException(table_name, base_table_url)

    _routing_mapping.append((table_name, base_table_url))

    TableResponseModel = await get_table_model(table_name)

    @app.get(base_table_url, response_model=List[TableResponseModel])
    async def get_list(
        request: Request,  # https://www.starlette.io/requests/
    ):
        return await async_view_get_data(request, TableResponseModel)

    @app.get(base_table_url + "/{pk}", response_model=TableResponseModel)
    async def get_unique(
        request: Request,  # https://www.starlette.io/requests/
        pk: str
    ):
        return await async_view_get_data_unique(request, pk, TableResponseModel)

    
    if not read_only:

        @app.post(base_table_url, 
            response_model=TableResponseModel,
            status_code=status.HTTP_201_CREATED)
        async def create(request: Request):
            return {"hi_from": table_name}

        @app.put(base_table_url + "/{pk}", 
            response_model=TableResponseModel)
        async def update(pk):
            return {"pk":pk, "updated": table_name}

        @app.delete(base_table_url + "/{pk}", 
            status_code=status.HTTP_204_NO_CONTENT)
        async def delete(pk):
            return None
        

async def expose_method(
    table_name: str,
    callable: Callable,
    alias: str,
    method: str,
    **kwargs
):
    allowedmethods = ['post','put','delete','get','patch']
    if not method in allowedmethods:
        raise MethodNotAllowedException()
    
    base_table_url = [x[1] for x in _routing_mapping if x[0] == table_name]
    if not base_table_url:
        raise TableNotConfiguredYetException(table_name)
    
    base_table_url = base_table_url[0] + "/" + (alias or method.__qualname__)
    # 
    # app.[post,get,...] basically is a decorator for this method linked here
    # https://github.com/tiangolo/fastapi/blob/5614b94ccc9f72f1de2f63aae63f5fe90b86c8b5/fastapi/routing.py#L451
    #
    app.router.add_api_route(base_table_url, callable, methods=[method], **kwargs)
