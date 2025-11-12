from fastapi import FastAPI, HTTPException, Request, Header
from contextlib import asynccontextmanager
from typing import Any
from .catalog import FactorCatalog
from pipeline import normalize_event, enrich_event, score_event
import json
from jsonschema import validate as jsonschema_validate, ValidationError
from pathlib import Path
from storage.sqlite_adapter import insert_event, get_event
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

@asynccontextmanager
async def lifespan(app: FastAPI):
    # create and load catalog once on app startup
    catalog = FactorCatalog()
    try:
        catalog.load()
    except Exception as e:
        print('Catalog load error:', e)
    # attach catalog to app state for handlers to use if needed
    app.state.catalog = catalog
    yield
    # teardown (none for now)


app = FastAPI(title='SultryTAI (demo)', lifespan=lifespan)
catalog = getattr(app.state, 'catalog', FactorCatalog())

# Simple API key auth for MVP
API_KEYS = {"demo-key-123": "demo"}


@app.get('/health')
def health() -> Any:
    return {'status': 'ok'}


def check_api_key(x_api_key: str = Header(None)):
    if not x_api_key or x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail='invalid api key')


# Prometheus metrics
REQUEST_COUNT = Counter('sultry_request_count', 'Total HTTP requests', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('sultry_request_latency_seconds', 'Request latency seconds', ['method', 'endpoint'])


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    try:
        response = await call_next(request)
        status = response.status_code
    except Exception as e:
        status = 500
        raise
    finally:
        elapsed = time.time() - start
        endpoint = request.url.path
        method = request.method
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(elapsed)
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=str(status)).inc()
    return response


@app.get('/metrics')
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


@app.post('/ingest/event')
async def ingest_event(request: Request, x_api_key: str = Header(None)):
    check_api_key(x_api_key)
    payload = await request.json()
    # validate incoming payload against event schema
    try:
        schema_path = Path(__file__).resolve().parent.parent / "schemas" / "event.schema.json"
        with open(schema_path, "r", encoding="utf-8") as f:
            event_schema = json.load(f)
        jsonschema_validate(instance=payload, schema=event_schema)
    except ValidationError as e:
        # include the path to the failing element when available
        path = "".join([f"/{p}" for p in e.path]) if getattr(e, 'path', None) else ""
        detail = f"event schema validation error: {e.message}"
        if path:
            detail += f" (path: {path})"
        raise HTTPException(status_code=400, detail=detail)
    except FileNotFoundError:
        # schema missing — treat as server error
        raise HTTPException(status_code=500, detail="event schema not found on server")

    # pipeline: normalize -> enrich -> score -> persist
    ev = normalize_event(payload)
    ev = enrich_event(ev)
    ev = score_event(ev)
    insert_event(ev)
    return {'status':'accepted','event_id': ev.get('event_id'), 'score': ev.get('score')}


@app.get('/verdict/{event_id}')
def verdict(event_id: str):
    ev = get_event(event_id)
    if not ev:
        raise HTTPException(status_code=404, detail='event not found')
    return ev
