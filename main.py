from core.application import app
from core.routing import expose_table
from core.routing import expose_method
from core.routing import internal

from custom.animal import kill_animal

@app.on_event("startup")
async def startup():
    await expose_table(table_name="api_animal", alias="animal")
    await expose_table(table_name="api_herd", alias="herd")
    await expose_table(table_name="api_farm", alias="farm")
    await expose_table(table_name="view_clientes_ativos_pagantes", alias="clientes", read_only=True)

    await expose_method(
        table_name='api_animal', callable=kill_animal, 
        alias='setdead', method='post',
        summary="Mata um animal")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)