from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import RedirectResponse 
from fastapi import HTTPException
from pydantic import BaseModel, HttpUrl
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from .crud import get_original_url, create_shorten_url
from .database import init_db

import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class ShortenRequest(BaseModel):
    original_url: HttpUrl
    custom_code: str | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    init_db()
    logger.info("App is up, database initialized")
    yield





# ================================== API ==================================

app = FastAPI(title="Link Shortener", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/shorten", status_code=201)
async def shorten(request: ShortenRequest, req: Request):
    try:
        custom_code = create_shorten_url(str(request.original_url), request.custom_code)
        short_url = f"{req.url.scheme}://{req.url.netloc}/{custom_code}"

        logger.info(f"url shortend: {short_url} -> {request.original_url}")
        return {"shorten_url": short_url}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Exception from : {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)


@app.get("/{custom_code}")
def read_root(custom_code: str):
    original_url = get_original_url(custom_code)
    if not original_url:
        logger.warning(f"Custom code not found: {custom_code}")
        raise HTTPException(status_code=404, detail="Shorten url not found")
    
    logger.info(f"Redirect: {custom_code} -> {original_url}")
    return RedirectResponse(original_url, status_code=302)


