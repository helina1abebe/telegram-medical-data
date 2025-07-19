import logging
import traceback

from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends
from ethio_api.database import session_local
from ethio_api.crud import get_top_products, get_channel_activity, search_messages
from ethio_api.schemas import ProductReport, ChannelActivity, MessageSearch

app = FastAPI()
logging.basicConfig(level=logging.INFO, filename="api_log.log")
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/reports/top-products", response_model=list[ProductReport])
def top_products(limit: int = 10, db=Depends(get_db)):
    return get_top_products(db, limit)

@app.get("/api/channels/{channel_name}/activity", response_model=ChannelActivity)
def channel_activity(channel_name: str, db=Depends(get_db)):
    return get_channel_activity(db, channel_name)

@app.get("/api/search/messages", response_model=list[MessageSearch])
def search(query: str, db=Depends(get_db)):
    return search_messages(db, query)


