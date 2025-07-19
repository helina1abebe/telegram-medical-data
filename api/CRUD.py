from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from ethio_api.schemas import ProductReport, ChannelActivity, MessageSearch

def get_top_products(db: Session, limit: int = 10):
    rows = db.execute(text("""
        SELECT message AS product_name, COUNT(*) AS mention_count
        FROM analytics_analytics.fct_messages
        GROUP BY message
        ORDER BY mention_count DESC
        LIMIT :limit
    """), {"limit": limit}).fetchall()
    
    return [ProductReport(product_name=row[0], mention_count=row[1]) for row in rows]

def get_channel_activity(db: Session, channel_name: str):
    row = db.execute(text(f"""
        SELECT channel_id, 
                      COUNT(*) FILTER (WHERE message_date >= CURRENT_DATE - INTERVAL '1 day') AS daily_post_count,
                      COUNT(*) FILTER (WHERE message_date >= CURRENT_DATE - INTERVAL '7 day') AS weekly_post_count
        FROM analytics_analytics.fct_messages
        WHERE channel_id = '{channel_name}'
        GROUP BY channel_id
    """)).fetchone()
    return ChannelActivity(channel_name=row[0], daily_post_count=row[1], weekly_post_count=row[2])

def search_messages(db: Session, query: str):
    rows = db.execute(text("""
        SELECT message_id, message, channel_name, message_date
        FROM analytics_analytics.fct_messages
        WHERE message ILIKE :query
        LIMIT 50
    """), {"query": f"%{query}%"}).fetchall()

    return [
        MessageSearch(
            message_id=row[0],
            message=row[1],
            channel_name=row[2],
            date=row[3].strftime("%Y-%m-%d %H:%M:%S") if row[3] else None
        )
        for row in rows
    ]

