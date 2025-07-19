from pydantic import BaseModel

class ProductReport(BaseModel):
    product_name: str
    mention_count: int

class ChannelActivity(BaseModel):
    channel_name: str
    daily_post_count: int
    weekly_post_count: int

class MessageSearch(BaseModel):
    message_id: str
    message: str
    channel_name: str
    date: str


