from fastapi import FastAPI

__all__ = ['app']

app = FastAPI(title='PG-AutoAPI', version=0.1, redoc_url=None)
