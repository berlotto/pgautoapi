from core.application import app
from core.routing import expose_table
from core.routing import expose_method
from core.routing import internal

from custom.animal import kill_animal

@app.on_event("startup")
async def startup():
    await expose_table(table_name="tabela_1", alias="tab1")
    await expose_table(table_name="tabela_2", alias="tab2")
    await expose_table(table_name="tabela_3", alias="tab3")
    await expose_table(table_name="view_dados_1", alias="visao1", read_only=True)

    await expose_method(
        table_name='tabela_1', callable=kill_animal, 
        alias='method_alias', method='post',
        summary="Um método a mais")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
