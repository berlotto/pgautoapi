from fastapi import FastAPI

__all__ = ['app']

app = FastAPI(title='Jetapi-Auto', version=0.1, redoc_url=None)
