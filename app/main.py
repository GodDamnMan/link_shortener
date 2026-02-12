from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse 
from fastapi import HTTPException
from pydantic import BaseModel, HttpUrl
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from .crud import get_original_url, create_shorten_url
from .database import init_db



@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    init_db()
    yield


app = FastAPI(title="Link Shortener", lifespan=lifespan)



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/{code}")
def read_root(code: str):
    original_url = get_original_url(code)
    if not original_url:
        raise HTTPException(status_code=404, detail="Shorten URL not found")
    
    return RedirectResponse(original_url, status_code=302)




class ShortenRequest(BaseModel):
    original_url: HttpUrl
    custom_code: str | None = None

@app.post("/shorten", status_code=201)
async def shorten(request: ShortenRequest, req: Request):
    try:
        custom_code = create_shorten_url(str(request.original_url), request.custom_code)
        if not custom_code:
            raise HTTPException(status_code=409, detail=f"Code already exists: {request.custom_code}")

        short_url = f"{req.url.scheme}://{req.url.netloc}/{custom_code}"

        return {"shorten_url": short_url}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")
