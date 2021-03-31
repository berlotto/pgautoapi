import databases
from pydantic.main import BaseModel

from core.application import app

DATABASE_URL = "postgresql://asyncapi:dbpasswd@localhost/mypgdatabase"

database = databases.Database(DATABASE_URL)

__all__ = ["database"]

@app.on_event("startup")
async def startup():
    print("Conectando à base...")
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    print("Fechando a conexão da base...")
    await database.disconnect()

