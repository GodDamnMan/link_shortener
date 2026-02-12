from fastapi import FastAPI
from fastapi.responses import RedirectResponse 
from fastapi import HTTPException
from .crud import get_original_url


app = FastAPI(title="Link Shortener")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/{code}")
def read_root(code: str):
    original_url = get_original_url(code)
    if not original_url:
        raise HTTPException(status_code=404, detail="Shorten URL not found")
    
    return RedirectResponse(original_url, status_code=302)